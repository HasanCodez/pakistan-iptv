import json
import re

CATEGORY_ORDER = [
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
]

def add_shia():
    with open('verified_shia_channels.json', 'r', encoding='utf-8') as f:
        shia_channels = json.load(f)

    # Format each shia channel entry
    formatted_shia = []
    for s in shia_channels:
        name = s['name']
        cid = s.get('tvg_id', '')
        logo = s.get('tvg_logo', '')
        if not logo and 'Zainabia' in name:
            logo = 'https://i.imgur.com/qE4JkP2.png'
            
        clean_name = re.sub(r'\s*\([^)]*\)', '', name).strip()
        formatted_shia.append({
            "group": "Islamic | Shia",
            "name": name,
            "clean_name": clean_name,
            "tvg_id": cid,
            "tvg_name": clean_name,
            "tvg_logo": logo,
            "url": s['url'],
            "headers": []
        })

    for fname in ['final_inventory.json', 'final_inventory_validated.json']:
        with open(fname, 'r', encoding='utf-8') as f:
            existing = json.load(f)

        existing_urls = set(c['url'] for c in existing)
        channels_by_group = {cat: [] for cat in CATEGORY_ORDER}

        for c in existing:
            g = c.get('group', 'Sports | Other')
            if g in channels_by_group:
                channels_by_group[g].append(c)
            else:
                channels_by_group.setdefault('Sports | Other', []).append(c)

        added = 0
        for sc in formatted_shia:
            if sc['url'] not in existing_urls:
                channels_by_group['Islamic | Shia'].append(sc)
                existing_urls.add(sc['url'])
                added += 1

        merged = []
        for cat in CATEGORY_ORDER:
            merged.extend(channels_by_group[cat])

        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        print(f"Updated {fname}: added {added} Shia channels (Total: {len(merged)})")

if __name__ == '__main__':
    add_shia()
