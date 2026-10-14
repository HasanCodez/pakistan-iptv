import json
import re

ALLOWED_CATEGORIES = {
    "Pakistan | News",
    "Pakistan | Entertainment",
    "Pakistan | General",
    "Pakistan | Sports",
    "Iran | News",
    "Iran | Entertainment",
    "Iran | General",
    "Iran | Sports",
    "Islamic | Shia",
    "English | News",
    "Sports | Football",
    "Sports | Cricket",
    "Sports | F1 & Motorsport",
    "Sports | UFC & Combat",
    "Sports | Other"
}

with open('inspected_channels.json', 'r', encoding='utf-8') as f:
    before_channels = json.load(f)

with open('pakistan-iptv.m3u', 'r', encoding='utf-8') as f:
    lines = f.readlines()

after_channels = []
curr = None
for line in lines:
    line = line.strip()
    if line.startswith('#EXTINF:'):
        curr = {'extinf': line, 'headers': []}
        m_group = re.search(r'group-title="([^"]*)"', line)
        m_id = re.search(r'tvg-id="([^"]*)"', line)
        m_logo = re.search(r'tvg-logo="([^"]*)"', line)
        m_name = re.search(r'tvg-name="([^"]*)"', line)
        name_idx = line.rfind(',')
        name = line[name_idx+1:].strip() if name_idx != -1 else ''
        curr['group'] = m_group.group(1) if m_group else ''
        curr['tvg_id'] = m_id.group(1) if m_id else ''
        curr['tvg_name'] = m_name.group(1) if m_name else ''
        curr['tvg_logo'] = m_logo.group(1) if m_logo else ''
        curr['name'] = name
    elif line.startswith('#EXTGRP:'):
        if curr:
            curr['extgrp'] = line.replace('#EXTGRP:', '').strip()
    elif line.startswith('#EXTVLCOPT:') or line.startswith('#EXTHTTP:'):
        if curr:
            curr['headers'].append(line)
    elif line and not line.startswith('#') and curr:
        curr['url'] = line
        after_channels.append(curr)
        curr = None

print(f"Total channels BEFORE: {len(before_channels)}")
print(f"Total channels AFTER:  {len(after_channels)}")

# Check category counts
group_counts = {}
for c in after_channels:
    g = c['group']
    group_counts[g] = group_counts.get(g, 0) + 1

print("\n--- CATEGORY BREAKDOWN IN UPDATED M3U ---")
for g, count in sorted(group_counts.items()):
    is_valid = g in ALLOWED_CATEGORIES
    print(f"  {g:25s}: {count:2d} channels (Valid: {is_valid})")

# Check all categories are strictly in allowed set
unallowed = set(group_counts.keys()) - ALLOWED_CATEGORIES
if unallowed:
    print(f"\nWARNING: Found unallowed categories: {unallowed}")
else:
    print("\nSUCCESS: All categories match the exact required specification 100%!")

# Check every channel has valid URL and #EXTGRP
missing_url = [c for c in after_channels if not c['url'] or not c['url'].startswith('http')]
missing_grp = [c for c in after_channels if not c.get('extgrp')]
mismatched_grp = [c for c in after_channels if c.get('extgrp') != c['group']]

print(f"Missing URL count: {len(missing_url)}")
print(f"Missing EXTGRP count: {len(missing_grp)}")
print(f"Mismatched EXTGRP count: {len(mismatched_grp)}")

# Check URL preservation
before_urls = set(c['url'] for c in before_channels)
after_urls = set(c['url'] for c in after_channels)
diff_urls = before_urls - after_urls
if not diff_urls:
    print("SUCCESS: 100% of stream URLs were strictly preserved without accidental modification!")
else:
    print(f"URL differences: {len(diff_urls)}")
