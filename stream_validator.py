import urllib.request
import urllib.error
import ssl
import json
import re
import concurrent.futures
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

# SSL context that doesn't fail on self-signed certs
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def test_stream_url(url, user_agent=None, referrer=None, timeout=8):
    ua = user_agent if user_agent else DEFAULT_UA
    headers = {'User-Agent': ua}
    if referrer:
        headers['Referer'] = referrer
        
    req = urllib.request.Request(url, headers=headers)
    
    # Try GET with range or small read
    try:
        start = time.time()
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            code = resp.status
            content_type = resp.headers.get('Content-Type', '')
            # Read first 512 bytes to verify it's an m3u8 or video stream
            sample = resp.read(512)
            duration = round(time.time() - start, 2)
            is_m3u8 = b'#EXTM3U' in sample or 'mpegurl' in content_type.lower() or 'apple' in content_type.lower() or 'video' in content_type.lower()
            return {
                'status': 'ONLINE',
                'http_code': code,
                'content_type': content_type,
                'is_m3u8': is_m3u8,
                'response_time': duration,
                'error': None
            }
    except urllib.error.HTTPError as e:
        return {
            'status': 'HTTP_ERROR',
            'http_code': e.code,
            'content_type': '',
            'is_m3u8': False,
            'response_time': 0,
            'error': f"HTTP {e.code}: {e.reason}"
        }
    except urllib.error.URLError as e:
        return {
            'status': 'OFFLINE',
            'http_code': 0,
            'content_type': '',
            'is_m3u8': False,
            'response_time': 0,
            'error': str(e.reason)
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'http_code': 0,
            'content_type': '',
            'is_m3u8': False,
            'response_time': 0,
            'error': str(e)
        }

print("Validator utility ready.")
