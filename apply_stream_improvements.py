import json
import os

def update_streams():
    for filename in ['final_inventory.json', 'final_inventory_validated.json']:
        with open(filename, 'r', encoding='utf-8') as f:
            channels = json.load(f)
            
        for ch in channels:
            name = ch.get('name', '')
            # 1. DW English
            if 'DW English' in name:
                ch['url'] = 'https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/master.m3u8'
                ch['headers'] = []
            # 2. Reuters TV
            elif 'Reuters TV' in name:
                ch['url'] = 'https://amg00453-reuters-amg00453c1-xumo-us-2073.playouts.now.amagi.tv/reuters-reuters-hls/playlist.m3u8'
                ch['headers'] = []
            # 3. Bloomberg TV+
            elif 'Bloomberg TV+' in name:
                ch['url'] = 'https://bloomberg.com/media-manifest/streams/us.m3u8'
                ch['headers'] = []
            # 4. Swerve Combat
            elif 'Swerve Combat' in name:
                ch['url'] = 'https://a-cdn.klowdtv.com/live3/swervecombat_720p/playlist.m3u8'
                ch['headers'] = []
            # 5. Eurosport 4K Czechia -> Red Bull TV
            elif 'Eurosport 4K' in name:
                ch['name'] = 'Red Bull TV (1080p)'
                ch['clean_name'] = 'Red Bull TV'
                ch['tvg_id'] = 'RedBullTV.at'
                ch['tvg_name'] = 'Red Bull TV'
                ch['tvg_logo'] = 'https://i.imgur.com/KqJm02a.png'
                ch['url'] = 'https://rbmn-live.akamaized.net/hls/live/590964/BoRB-AT/master.m3u8'
                ch['headers'] = []
                
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=2, ensure_ascii=False)
            
        print(f"Updated {filename} successfully ({len(channels)} channels).")

if __name__ == '__main__':
    update_streams()
