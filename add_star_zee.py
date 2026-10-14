import json

CHANNELS_TO_ADD = [
    {
        "group": "Sports | Cricket",
        "name": "Star Sports 2 (576p)",
        "clean_name": "Star Sports 2",
        "tvg_id": "StarSports2.in@SD",
        "tvg_name": "Star Sports 2",
        "tvg_logo": "https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_STAR_SPORTS_2/images/LOGO_HD/image.png",
        "url": "http://103.151.60.162:2122/play/a00v/index.m3u8?hls",
        "headers": []
    },
    {
        "group": "Sports | Cricket",
        "name": "Star Sports 2 Telugu HD (576p)",
        "clean_name": "Star Sports 2 Telugu HD",
        "tvg_id": "StarSports2Telugu.in@HD",
        "tvg_name": "Star Sports 2 Telugu HD",
        "tvg_logo": "https://i.imgur.com/m7DvvqF.png",
        "url": "https://real-vk.proxy.nellaiiptv.com/SDMEDIA/index.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "Trace Sport Stars HD (1080p)",
        "clean_name": "Trace Sport Stars",
        "tvg_id": "TraceSportStars.fr@HD",
        "tvg_name": "Trace Sport Stars",
        "tvg_logo": "https://i.imgur.com/8Qj8m0k.png",
        "url": "https://lightning-tracesport-samsungau.amagi.tv/playlist.m3u8",
        "headers": []
    }
]

CATEGORY_ORDER = [
    "Pakistan | News",
    "Pakistan | Entertainment",
    "Pakistan | General",
    "Pakistan | Sports",
    "Iran | News",
    "Iran | Entertainment",
    "Iran | General",
    "Iran | Sports",
    "English | News",
    "Sports | Football",
    "Sports | Cricket",
    "Sports | F1 & Motorsport",
    "Sports | UFC & Combat",
    "Sports | Other"
]

def update_inventory():
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
        for new_c in CHANNELS_TO_ADD:
            if new_c['url'] not in existing_urls:
                channels_by_group[new_c['group']].append(new_c)
                existing_urls.add(new_c['url'])
                added += 1

        merged = []
        for cat in CATEGORY_ORDER:
            merged.extend(channels_by_group[cat])

        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        print(f"Updated {fname}: added {added} channels (Total: {len(merged)})")

if __name__ == '__main__':
    update_inventory()
