import urllib.request
import urllib.error
import ssl
import json
import re
import time
import concurrent.futures
import sys

sys.stdout.reconfigure(encoding='utf-8')

# SSL context that doesn't fail on self-signed certs
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def parse_m3u(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    channels = []
    curr = None
    for line in lines:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            curr = {
                'raw_extinf': line,
                'user_agent': None,
                'referrer': None
            }
            m_group = re.search(r'group-title="([^"]*)"', line)
            m_id = re.search(r'tvg-id="([^"]*)"', line)
            m_name = re.search(r'tvg-name="([^"]*)"', line)
            name_idx = line.rfind(',')
            name = line[name_idx+1:].strip() if name_idx != -1 else ''
            curr['group'] = m_group.group(1) if m_group else 'Uncategorized'
            curr['tvg_id'] = m_id.group(1) if m_id else ''
            curr['tvg_name'] = m_name.group(1) if m_name else name
            curr['name'] = name
        elif line.startswith('#EXTGRP:'):
            if curr:
                curr['extgrp'] = line.replace('#EXTGRP:', '').strip()
        elif line.startswith('#EXTVLCOPT:http-user-agent='):
            if curr:
                curr['user_agent'] = line.split('=', 1)[1].strip()
        elif line.startswith('#EXTVLCOPT:http-referrer='):
            if curr:
                curr['referrer'] = line.split('=', 1)[1].strip()
        elif line.startswith('#EXTHTTP:'):
            try:
                data = json.loads(line.replace('#EXTHTTP:', ''))
                if curr:
                    curr['user_agent'] = data.get('User-Agent')
                    curr['referrer'] = data.get('Referer')
            except Exception:
                pass
        elif line and not line.startswith('#') and curr:
            curr['url'] = line
            channels.append(curr)
            curr = None
    return channels

def test_single_channel(ch, timeout=10):
    url = ch['url']
    ua = ch.get('user_agent') or DEFAULT_UA
    headers = {
        'User-Agent': ua,
        'Accept': '*/*'
    }
    if ch.get('referrer'):
        headers['Referer'] = ch['referrer']
        
    req = urllib.request.Request(url, headers=headers)
    start = time.time()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            code = resp.status
            content_type = resp.headers.get('Content-Type', '')
            sample = resp.read(512)
            duration = round(time.time() - start, 2)
            
            # Verify valid stream payload
            is_valid_stream = (
                b'#EXTM3U' in sample or
                b'#EXTINF' in sample or
                b'#EXT-X' in sample or
                'mpegurl' in content_type.lower() or
                'apple' in content_type.lower() or
                'video' in content_type.lower() or
                'octet-stream' in content_type.lower() or
                sample.startswith(b'\x47') # MPEG-TS sync byte
            )
            
            return {
                **ch,
                'status': 'ONLINE',
                'http_code': code,
                'content_type': content_type,
                'is_valid_stream': is_valid_stream,
                'response_time': duration,
                'error': None
            }
    except urllib.error.HTTPError as e:
        duration = round(time.time() - start, 2)
        return {
            **ch,
            'status': 'HTTP_ERROR',
            'http_code': e.code,
            'content_type': '',
            'is_valid_stream': False,
            'response_time': duration,
            'error': f"HTTP {e.code}: {e.reason}"
        }
    except urllib.error.URLError as e:
        duration = round(time.time() - start, 2)
        return {
            **ch,
            'status': 'OFFLINE',
            'http_code': 0,
            'content_type': '',
            'is_valid_stream': False,
            'response_time': duration,
            'error': str(e.reason)
        }
    except Exception as e:
        duration = round(time.time() - start, 2)
        return {
            **ch,
            'status': 'ERROR',
            'http_code': 0,
            'content_type': '',
            'is_valid_stream': False,
            'response_time': duration,
            'error': str(e)
        }

def main():
    channels = parse_m3u('pakistan-iptv.m3u')
    print(f"Loaded {len(channels)} channels from pakistan-iptv.m3u.")
    print("Initiating concurrent live network validation probe across all channels...\n")
    
    results = []
    # Test concurrently with 16 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        future_to_ch = {executor.submit(test_single_channel, ch): ch for ch in channels}
        for future in concurrent.futures.as_completed(future_to_ch):
            res = future.result()
            results.append(res)
            code_str = str(res['http_code']) if res['http_code'] else 'ERR'
            status_tag = f"[{res['status']} {code_str}]"
            print(f"{status_tag:16s} | {res['group'][:24]:24s} | {res['name'][:28]:28s} ({res['response_time']}s)")

    # Sort results by group and name for clean reporting
    results.sort(key=lambda x: (x['group'], x['name']))

    # Statistics
    total = len(results)
    online = [r for r in results if r['status'] == 'ONLINE']
    http_errors = [r for r in results if r['status'] == 'HTTP_ERROR']
    offline = [r for r in results if r['status'] in ('OFFLINE', 'ERROR')]
    
    print("\n" + "="*80)
    print("LIVE VALIDATION SUMMARY REPORT")
    print("="*80)
    print(f"Total Channels in Playlist: {total}")
    print(f"Total Confirmed ONLINE:     {len(online)} ({len(online)/total*100:.1f}%)")
    print(f"Total HTTP Errors:          {len(http_errors)}")
    print(f"Total Connection Timeouts:  {len(offline)}")
    print("="*80)

    # Breakdown by category
    categories = {}
    for r in results:
        g = r['group']
        if g not in categories:
            categories[g] = {'total': 0, 'online': 0, 'errors': []}
        categories[g]['total'] += 1
        if r['status'] == 'ONLINE':
            categories[g]['online'] += 1
        else:
            categories[g]['errors'].append(f"{r['name']}: {r['error']}")

    print("\nCATEGORY-BY-CATEGORY BREAKDOWN:")
    print(f"{'Category':<28} | {'Total':<6} | {'Online':<8} | {'Pass Rate':<10}")
    print("-" * 60)
    for g, data in sorted(categories.items()):
        pass_rate = (data['online'] / data['total']) * 100
        print(f"{g:<28} | {data['total']:<6} | {data['online']:<8} | {pass_rate:.1f}%")

    if http_errors or offline:
        print("\nCHANNELS WITH ISSUES / GEO-RESTRICTIONS:")
        for r in http_errors + offline:
            print(f" - [{r['group']}] {r['name']}: {r['error']} -> {r['url']}")

    with open('live_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nDetailed output saved to live_verification_report.json.")

if __name__ == '__main__':
    main()
