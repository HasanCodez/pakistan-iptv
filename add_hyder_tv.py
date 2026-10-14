import json

def add_hyder():
    hyder_entry = {
        "group": "Islamic | Shia",
        "name": "Hyder TV (720p)",
        "clean_name": "Hyder TV",
        "tvg_id": "HyderTV.ca",
        "tvg_name": "Hyder TV",
        "tvg_logo": "https://i.imgur.com/8Qj8m0k.png",
        "url": "https://cdn.live247stream.com/hyder/tv/playlist.m3u8",
        "headers": []
    }

    for fname in ['final_inventory.json', 'final_inventory_validated.json']:
        with open(fname, 'r', encoding='utf-8') as f:
            channels = json.load(f)

        existing_urls = set(c['url'] for c in channels)
        if hyder_entry['url'] not in existing_urls:
            # insert into Islamic | Shia group
            inserted = False
            for i, c in enumerate(channels):
                if c.get('group') == 'Islamic | Shia':
                    channels.insert(i + 1, hyder_entry)
                    inserted = True
                    break
            if not inserted:
                channels.append(hyder_entry)

            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(channels, f, indent=2, ensure_ascii=False)
            print(f"Added Hyder TV to {fname} (Total: {len(channels)})")
        else:
            print(f"Hyder TV already in {fname}")

if __name__ == '__main__':
    add_hyder()
