import json

NEW_SPORTS_CHANNELS = [
    # Pakistan | Sports
    {
        "group": "Pakistan | Sports",
        "name": "M Sports (1080p)",
        "clean_name": "M Sports",
        "tvg_id": "MSports.pk",
        "tvg_name": "M Sports",
        "tvg_logo": "https://msports.pk/wp-content/uploads/2023/10/cropped-logo-white-transparent-192x192.png",
        "url": "https://cdn.rabta.stream/M-Sports/index.m3u8",
        "headers": []
    },
    {
        "group": "Pakistan | Sports",
        "name": "PK Sports (720p)",
        "clean_name": "PK Sports",
        "tvg_id": "PKSports.pk",
        "tvg_name": "PK Sports",
        "tvg_logo": "https://i.imgur.com/x06r8Q2.png",
        "url": "https://lbgo.bozztv.com/ssh101/ssh101/pksportshd/playlist.m3u8",
        "headers": []
    },
    # Sports | Football
    {
        "group": "Sports | Football",
        "name": "Real Madrid TV (726p)",
        "clean_name": "Real Madrid TV",
        "tvg_id": "RealMadridTV.es",
        "tvg_name": "Real Madrid TV",
        "tvg_logo": "https://i.imgur.com/gSZeE51.png",
        "url": "https://rmtv.akamaized.net/hls/live/2043153/rmtv-es-web/master.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Football",
        "name": "Sportitalia (1080p)",
        "clean_name": "Sportitalia",
        "tvg_id": "Sportitalia.it",
        "tvg_name": "Sportitalia",
        "tvg_logo": "https://i.imgur.com/MvhvFmH.png",
        "url": "https://edge-001.streamup.eu/sportitalia/sihd_abr/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Football",
        "name": "Digi Sport 3 (576i)",
        "clean_name": "Digi Sport 3",
        "tvg_id": "DigiSport3.ro",
        "tvg_name": "Digi Sport 3",
        "tvg_logo": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Digi_Sport_3_logo.png",
        "url": "https://dokagents.site/live/digisport3/mono.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Football",
        "name": "Digi Sport 4 (576i)",
        "clean_name": "Digi Sport 4",
        "tvg_id": "DigiSport4.ro",
        "tvg_name": "Digi Sport 4",
        "tvg_logo": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Digi_Sport_4_logo.png",
        "url": "https://dokagents.site/live/digisport4/mono.m3u8",
        "headers": []
    },
    # Sports | Cricket
    {
        "group": "Sports | Cricket",
        "name": "Cricket Gold (1080p)",
        "clean_name": "Cricket Gold",
        "tvg_id": "CricketGold.au",
        "tvg_name": "Cricket Gold",
        "tvg_logo": "https://resources.cricket-australia.pulselive.com/cricket-australia/photo/2025/07/25/836eddae-4329-4542-ad17-dcd37e9d951a/Cricket-Gold-1920x1080_noBG.png",
        "url": "https://streams2.sofast.tv/ptnr-yupptv/title-cricketgold/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/b2048bb8-1686-4432-aa50-647245383e0c/manifest.m3u8",
        "headers": []
    },
    # Sports | F1 & Motorsport
    {
        "group": "Sports | F1 & Motorsport",
        "name": "Canal Motor (720p)",
        "clean_name": "Canal Motor",
        "tvg_id": "CanalMotor.no",
        "tvg_name": "Canal Motor",
        "tvg_logo": "https://i.imgur.com/i9109iP.png",
        "url": "https://digicom.hls.iptvdc.com/canalmotor/index.m3u8",
        "headers": []
    },
    # Sports | UFC & Combat
    {
        "group": "Sports | UFC & Combat",
        "name": "PFL MMA (720p)",
        "clean_name": "PFL MMA",
        "tvg_id": "PFL.us",
        "tvg_name": "PFL MMA",
        "tvg_logo": "https://i.imgur.com/J3Zq42e.png",
        "url": "https://jmp2.uk/plu-64f6180130ab3300083d896b.m3u8",
        "headers": []
    },
    {
        "group": "Sports | UFC & Combat",
        "name": "DAZN Combat (684p)",
        "clean_name": "DAZN Combat",
        "tvg_id": "DAZNCombat.us",
        "tvg_name": "DAZN Combat",
        "tvg_logo": "https://i.imgur.com/kS94bdf.png",
        "url": "https://jmp2.uk/plu-64d626ac9b414d000820e2fc.m3u8",
        "headers": []
    },
    {
        "group": "Sports | UFC & Combat",
        "name": "MMA-TV.com (1080p)",
        "clean_name": "MMA-TV.com",
        "tvg_id": "MMATV.us",
        "tvg_name": "MMA-TV.com",
        "tvg_logo": "https://i.imgur.com/j4q4XNf.png",
        "url": "https://streams2.sofast.tv/vglive-sk-462904/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | UFC & Combat",
        "name": "Glory Kickboxing (720p)",
        "clean_name": "Glory Kickboxing",
        "tvg_id": "GloryKickboxing.nl",
        "tvg_name": "Glory Kickboxing",
        "tvg_logo": "https://i.imgur.com/Qk99J58.png",
        "url": "https://6f972d29.wurl.com/master/f36d25e7e52f1ba8d7e56eb859c636563214f541/UmFrdXRlblRWLWV1X0dsb3J5S2lja2JveGluZ19ITFM/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | UFC & Combat",
        "name": "XFC TV (720p)",
        "clean_name": "XFC TV",
        "tvg_id": "XFC.us",
        "tvg_name": "XFC TV",
        "tvg_logo": "https://i.imgur.com/9O0O1kS.png",
        "url": "https://stream-us-east-1.getpublica.com/playlist.m3u8?network_id=2247",
        "headers": []
    },
    # Sports | Other
    {
        "group": "Sports | Other",
        "name": "Tennis Channel 2 (1080p)",
        "clean_name": "Tennis Channel 2",
        "tvg_id": "TennisChannel2.us",
        "tvg_name": "Tennis Channel 2",
        "tvg_logo": "https://i.imgur.com/Z4wJ8kP.png",
        "url": "https://mumbai-edge.smartplaytv.in/Tennis2/index.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "SportsGrid (1080p)",
        "clean_name": "SportsGrid",
        "tvg_id": "SportsGrid.us",
        "tvg_name": "SportsGrid",
        "tvg_logo": "https://i.imgur.com/2U54k9D.png",
        "url": "https://sportsgrid-tribal.amagi.tv/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "Unbeaten (1080p)",
        "clean_name": "Unbeaten",
        "tvg_id": "Unbeaten.us",
        "tvg_name": "Unbeaten",
        "tvg_logo": "https://i.imgur.com/W2d0qF7.png",
        "url": "https://d1t5afz6qed3xk.cloudfront.net/Unbeaten.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "World of Freesports (1080p)",
        "clean_name": "World of Freesports",
        "tvg_id": "WorldOfFreesports.de",
        "tvg_name": "World of Freesports",
        "tvg_logo": "https://i.imgur.com/4lqQp4S.png",
        "url": "https://mainstreammedia-worldoffreesportsintl-rakuten.amagi.tv/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "Strongman Champions League (720p)",
        "clean_name": "Strongman Champions League",
        "tvg_id": "StrongmanChampionsLeague.fi",
        "tvg_name": "Strongman Champions League",
        "tvg_logo": "https://i.imgur.com/fM91MvM.png",
        "url": "https://rightsboosterltd-scl-1-be.samsung.wurl.tv/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "Women's Sports Network (1080p)",
        "clean_name": "Women's Sports Network",
        "tvg_id": "WomensSportsNetwork.us",
        "tvg_name": "Women's Sports Network",
        "tvg_logo": "https://i.imgur.com/3d6H0QO.png",
        "url": "https://d39accvx65hq9o.cloudfront.net/Womens_Sports_Network.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "Swerve Sports (720p)",
        "clean_name": "Swerve Sports",
        "tvg_id": "SwerveSports.us",
        "tvg_name": "Swerve Sports",
        "tvg_logo": "https://i.imgur.com/bQ92w5P.png",
        "url": "https://a-cdn.klowdtv.com/live3/swervewomenssports_720p/playlist.m3u8",
        "headers": []
    },
    {
        "group": "Sports | Other",
        "name": "Right Now TV (720p)",
        "clean_name": "Right Now TV",
        "tvg_id": "RightNowTV.us",
        "tvg_name": "Right Now TV",
        "tvg_logo": "https://i.imgur.com/xO4384o.png",
        "url": "https://a-cdn.klowdtv.com/live2/rightnowtv_720p/playlist.m3u8",
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

def add_channels():
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

        added_count = 0
        for new_c in NEW_SPORTS_CHANNELS:
            if new_c['url'] not in existing_urls:
                channels_by_group[new_c['group']].append(new_c)
                existing_urls.add(new_c['url'])
                added_count += 1

        merged_list = []
        for cat in CATEGORY_ORDER:
            merged_list.extend(channels_by_group[cat])

        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(merged_list, f, indent=2, ensure_ascii=False)

        print(f"Updated {fname}: added {added_count} channels (Total: {len(merged_list)})")

if __name__ == '__main__':
    add_channels()
