import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load official iptv-org data
with open('all_index_entries.json', 'r', encoding='utf-8') as f:
    all_index = json.load(f)

with open('streams.json', 'r', encoding='utf-8') as f:
    all_streams = json.load(f)

# Quick lookup dicts
index_by_id = {e['tvg_id']: e for e in all_index}

# Master curated catalog definition:
# List of (Group, ChannelName, tvg_id, prefer_url, country, resolution_override, notes)
channels_catalog = [
    # ================= PAKISTAN | NEWS =================
    ("Pakistan | News", "Dunya News", "DunyaNews.pk@SD", "https://imob.dunyanews.tv/livehd/ngrp:dunyalivehd_2_all/playlist.m3u8", "PK", "720p", "National 24/7 News"),
    ("Pakistan | News", "Samaa TV", "SamaaTV.pk@SD", "https://vodzong.mjunoon.tv:8087/streamtest/SAMAA-173/playlist.m3u8", "PK", "576p", "Major National News"),
    ("Pakistan | News", "92 News HD", "92NewsHD.pk@SD", "http://92news.vdn.dstreamone.net/92newshd/92hd/playlist.m3u8", "PK", "720p", "Major Urdu News Channel"),
    ("Pakistan | News", "24 News HD", "24NewsHD.pk@SD", "https://cdn4.mjunoon.tv:8087/streamtest/146M/chunks.m3u8", "PK", "HD", "National Current Affairs"),
    ("Pakistan | News", "Neo News", "NeoNews.pk@SD", "https://vodzong.mjunoon.tv:8087/streamtest/Neo-110/playlist.m3u8", "PK", "1080p", "Leading Urdu News Channel"),
    ("Pakistan | News", "ABN News", "ABNNews.pk@SD", "https://vodzong.mjunoon.tv:8087/streamtest/ABN-161/playlist.m3u8", "PK", "360p", "National News Network"),
    ("Pakistan | News", "Capital TV", "CapitalTV.pk@SD", "https://cdn4.mjunoon.tv:8087/streamtest/111M/chunks.m3u8", "PK", "SD", "National News Network"),
    ("Pakistan | News", "Lahore News", "LahoreNews.pk@SD", "https://vcdn.dunyanews.tv/lahorelive/ngrp:lnews_1_all/playlist.m3u8", "PK", "720p", "Metropolitan Regional News"),
    ("Pakistan | News", "News One", "NewsOne.pk@SD", "https://vodzong.mjunoon.tv:8087/streamtest/NEWS1-128/playlist.m3u8", "PK", "720p", "News & Current Affairs"),
    ("Pakistan | News", "7 News", "7News.pk@SD", "https://sscsott.com/7news/live/index.m3u8", "PK", "720p", "National News Channel"),
    ("Pakistan | News", "Aik News", "AikNews.pk@SD", "https://s2.ideationtec.live/Pnn/Pnn.m3u8?token=KsR3k27_sH3n-2", "PK", "SD", "Urdu News Network"),
    ("Pakistan | News", "Such TV", "SuchTV.pk@SD", "https://video.primexsports.com/suchnews/live/playlist.m3u8", "PK", "SD", "National News Channel"),
    ("Pakistan | News", "KTN News", "KTNNews.pk@SD", "https://vodzong.mjunoon.tv:8087/streamtest/KTNNews-151/playlist.m3u8", "PK", "360p", "Sindhi News Network"),
    ("Pakistan | News", "M News", "MNews.pk@SD", "https://cdn.rabta.stream/M-News/index.m3u8", "PK", "1080p", "Pakistani HD News Feed"),

    # ================= PAKISTAN | ENTERTAINMENT =================
    ("Pakistan | Entertainment", "Hum TV", "HumTV.pk@HD", "https://g4wlkwx8l23a-hls-live.5centscdn.com/HUM/271ddf829afeece44d8732757fba1a66.sdp/playlist_dvr.m3u8", "PK", "720p", "Top Pakistani Drama Network"),
    ("Pakistan | Entertainment", "Bol Entertainment", "BolEntertainment.pk@HD", "https://vodzong.mjunoon.tv:8087/streamtest/Channel5-159-4/playlist.m3u8", "PK", "HD", "Major Entertainment Network"),
    ("Pakistan | Entertainment", "A-Plus TV", "APlusTV.pk@SD", "https://cdn4.mjunoon.tv:8087/streamtest/118M/chunks.m3u8", "PK", "SD", "Urdu Drama & Entertainment"),
    ("Pakistan | Entertainment", "Masala TV", "MasalaTV.pk@SD", "https://cdn4.mjunoon.tv:8087/streamtest/81M/chunks.m3u8", "PK", "576p", "Hum Network Culinary & Food"),
    ("Pakistan | Entertainment", "Filmax", "Filmax.pk@SD", "https://s3.ideationtec.live/Filmax/Filmax.m3u8", "PK", "576p", "Pakistani Movies Channel"),
    ("Pakistan | Entertainment", "8XM", "8XM.pk@HD", "https://cdn4.mjunoon.tv:8087/streamtest/131M/chunks.m3u8", "PK", "HD", "Youth & Music Entertainment"),
    ("Pakistan | Entertainment", "JooMusic", "JooMusic.pk@SD", "https://livecdn.live247stream.com/joomusic/tv/playlist.m3u8", "PK", "720p", "Pakistani Music & Pop Culture Channel"),

    # ================= PAKISTAN | GENERAL =================
    ("Pakistan | General", "Discover Pakistan", "DiscoverPakistan.pk@SD", "https://livecdn.live247stream.com/discoverpakistan/web/playlist.m3u8", "PK", "1080p", "Tourism & Geography of Pakistan"),
    ("Pakistan | General", "aurLife", "aurLifeHD.pk@SD", "http://124.109.47.101/hls/stream1.m3u8", "PK", "614p", "Lifestyle & Infotainment"),

    # ================= PAKISTAN | SPORTS =================
    ("Pakistan | Sports", "PK Sports", "PKSports.pk@SD", "https://lbgo.bozztv.com/ssh101/ssh101/pksportshd/playlist.m3u8", "PK", "720p", "Pakistani Sports Channel"),
    ("Pakistan | Sports", "M Sports", "MSports.pk@SD", "https://cdn.rabta.stream/M-Sports/index.m3u8", "PK", "1080p", "Pakistani Sports Network"),

    # ================= IRAN | NEWS =================
    ("Iran | News", "IRINN", "IRINN.ir@SD", "http://185.9.2.18/chid_926/index.m3u8", "IR", "576p", "Islamic Republic of Iran News Network"),
    ("Iran | News", "Press TV", "PressTV.ir@SD", "https://cloud.odysee.live/content/26bcbcc342a5b143578f27dbfaf0002824df4492/master.m3u8", "IR", "720p", "English International News from Iran"),
    ("Iran | News", "Press TV French", "PressTVFrench.ir@SD", "https://live4.presstv.ir/live/smil:presstvfr.smil/playlist.m3u8", "IR", "1080p", "French International Service"),
    ("Iran | News", "Al Alam", "AlAlam.ir@SD", "https://live2.alalam.ir/alalam.m3u8", "IR", "360p", "Arabic News from Tehran"),
    ("Iran | News", "Iran Press", "IranPress.ir@SD", "https://live.presstv.ir/hls/presstv_5_482/index.m3u8", "IR", "SD", "Iranian News Agency TV"),
    ("Iran | News", "Iran International", "IranInternational.uk@SD", "https://hlspackager.akamaized.net/live/DB/IRAN_INTERNATIONAL/HLS/IRAN_INTERNATIONAL.m3u8", "IR", "1080p", "Persian International News"),

    # ================= IRAN | ENTERTAINMENT =================
    ("Iran | Entertainment", "iFilm English", "iFilmEnglish.ir@SD", "https://live.presstv.ir/hls/ifilmen.m3u8", "IR", "SD", "IRIB Iranian Cinema in English"),
    ("Iran | Entertainment", "iFilm Persian", "iFilmPersian.ir@SD", "https://live.presstv.ir/hls/ifilmfa.m3u8", "IR", "SD", "IRIB Cinema & TV Series"),
    ("Iran | Entertainment", "iFilm Arabic", "iFilmArabic.ir@SD", "https://live.presstv.ir/hls/ifilmar.m3u8", "IR", "SD", "IRIB Movies & Series in Arabic"),
    ("Iran | Entertainment", "iFilm 2", "iFilm2.ir@SD", "https://live.presstv.ir/hls/ifilm2.m3u8", "IR", "SD", "IRIB Dari & Afghan Persian Service"),
    ("Iran | Entertainment", "FX 1", "FX1.ir@SD", "https://fxtvhls.wns.live/hls/stream.m3u8", "IR", "SD", "Persian Movies & Series"),
    ("Iran | Entertainment", "FX 2", "FX2.ir@SD", "https://toonixhls.wns.live/hls/stream.m3u8", "IR", "SD", "Persian Family Entertainment"),
    ("Iran | Entertainment", "Persiana Iranian", "PersianaIranian.fr@SD", "https://irhls.persiana.live/hls/stream.m3u8", "IR", "SD", "Persiana Media Network"),
    ("Iran | Entertainment", "Bravo Farsi TV", "BravoFarsiTV.ir@SD", "https://bravoohls.wns.live/hls/stream.m3u8", "IR", "360p", "Farsi Entertainment Network"),
    ("Iran | Entertainment", "Cafe Film", "CafeFilm.ir@SD", "https://cafefhls.wns.live/hls/stream.m3u8", "IR", "SD", "Persian Movies Channel"),
    ("Iran | Entertainment", "Gold Star", "GoldStar.ir@SD", "https://moviethls.wns.live/hls/stream.m3u8", "IR", "SD", "Persian Movies & Shows"),
    ("Iran | Entertainment", "NewFlix", "NewFlix.ir@SD", "https://newfhls.wns.live/hls/stream.m3u8", "IR", "SD", "Persian Drama & Series"),

    # ================= IRAN | GENERAL =================
    ("Iran | General", "IRIB 1", "IRIB1.ir@SD", "https://ncdn.telewebion.ir/tv1/live/playlist.m3u8", "IR", "SD", "IRIB National Channel 1 (Domestic CDN)"),
    ("Iran | General", "IRIB 2", "IRIB2.ir@SD", "https://ncdn.telewebion.ir/tv2/live/playlist.m3u8", "IR", "SD", "IRIB National Channel 2 (Domestic CDN)"),
    ("Iran | General", "IRIB 4", "IRIB4.ir@SD", "https://ncdn.telewebion.ir/tv4/live/playlist.m3u8", "IR", "SD", "IRIB Scientific & Cultural (Domestic CDN)"),
    ("Iran | General", "IRIB Mostanad", "IRIBMostanad.ir@SD", "https://ncdn.telewebion.ir/mostanad/live/playlist.m3u8", "IR", "SD", "IRIB Documentary Channel (Domestic CDN)"),
    ("Iran | General", "IRIB UHD", "IRIBUHD.ir@4K", "https://ncdn.telewebion.ir/faratar/live/playlist.m3u8", "IR", "2160p", "IRIB 4K HDR Channel Faratar"),

    # ================= IRAN | SPORTS =================
    ("Iran | Sports", "IRIB 3", "IRIB3.ir@SD", "https://ncdn.telewebion.ir/tv3/live/playlist.m3u8", "IR", "SD", "IRIB Sports & Youth (Domestic CDN)"),
    ("Iran | Sports", "Varzesh TV", "VarzeshTV.ir@SD", "https://ncdn.telewebion.ir/varzesh/live/playlist.m3u8", "IR", "SD", "IRIB Dedicated Sports Channel"),

    # ================= ENGLISH NEWS =================
    ("English | News", "Al Jazeera English", "AlJazeera.qa@English", "https://live-hls-apps-aje-fa.getaj.net/AJE/index.m3u8", "QA", "1080p", "Global News Broadcaster"),
    ("English | News", "BBC News North America", "BBCNews.uk@NorthAmerica", "http://23.237.104.106:8080/USA_BBC_NEWS/index.m3u8", "UK", "1080p", "BBC World News Service"),
    ("English | News", "BBC News South Asia", "BBCNews.uk@SouthAsia", "https://mumbai-edge.smartplaytv.in/BBCNews/index.m3u8", "UK", "720p", "BBC Regional News Feed"),
    ("English | News", "DW English", "DW.de@English", "https://amg01644-amg01644c1-amgplt0343.playout.now3.amagi.tv/ts-eu-w1-pl-live-amgplt0343/playlist.m3u8", "DE", "1080p", "Deutsche Welle International"),
    ("English | News", "France 24 English", "France24.fr@English", "https://live.france24.com/hls/live/2037218-b/F24_EN_HI_HLS/master_5000.m3u8", "FR", "1080p", "France 24 Global 1080p Feed"),
    ("English | News", "Euronews English", "EuronewsEnglish.fr@SD", "https://dash4.antik.sk/live/test_euronews/playlist.m3u8", "FR", "720p", "Pan-European News Network"),
    ("English | News", "TRT World", "TRTWorld.tr@SD", "https://mumbai-edge.smartplaytv.in/TRTWorld/index.m3u8", "TR", "720p", "Turkish Global News Network"),
    ("English | News", "CGTN", "CGTN.cn@SD", "https://amg00405-rakutentv-cgtn-rakuten-i9tar.amagi.tv/master.m3u8", "CN", "1080p", "China Global Television Network"),
    ("English | News", "NHK World-Japan", "NHKWorldJapan.jp@SD", "https://masterpl.hls.nhkworld.jp/hls/w/live/smarttv.m3u8", "JP", "1080p", "Japan Public Broadcaster English"),
    ("English | News", "ABC News Live", "ABCNewsLive.us@SD", "https://aegis-cloudfront-1.tubi.video/d6cbb0de-68e4-4f3b-82f9-bf5d526e0bde/index.m3u8", "US", "720p", "American ABC News Live Network"),
    ("English | News", "CBS News 24/7", "CBSNews247.us@SD", "https://cbsn-us.cbsnstream.cbsnews.com/out/v1/55a8648e8f134e82a470f83d562deeca/master.m3u8", "US", "720p", "CBS 24/7 Streaming News"),
    ("English | News", "NBC News NOW", "NBCNewsNOW.us@SD", "https://xumo-drct-nbcnn-ir8ze.fast.nbcuni.com/live/master.m3u8", "US", "1080p", "NBC News Global Streaming"),
    ("English | News", "Bloomberg TV Europe", "BloombergTV.us@Europe", "https://bloomberg.com/media-manifest/streams/eu.m3u8", "US", "720p", "Global Financial & Business News"),
    ("English | News", "Bloomberg TV Asia", "BloombergTV.us@Asia", "https://bloomberg.com/media-manifest/streams/asia.m3u8", "US", "720p", "Asia-Pacific Financial News"),
    ("English | News", "Bloomberg Originals", "BloombergOriginals.us@US", "https://bloomberg.com/media-manifest/streams/qt.m3u8", "US", "1080p", "Bloomberg Investigative & Business"),
    ("English | News", "Bloomberg TV+", "BloombergTV.us@Plus", "https://d8975dc3.wurl.com/master/f36d25e7e52f1ba8d7e56eb859c636563214f4e5/Bloomberg_live.m3u8", "US", "2160p", "Bloomberg 4K UHD Financial Feed"),
    ("English | News", "CNBC UK", "CNBCUK.uk@SD", "https://amg01079-nbcuuk-amg01079c2-samsung-gb-1258.playouts.now.amagi.tv/playlist/amg01079-nbcunationalcha-cnbcuk-samsunggb/playlist.m3u8", "UK", "1080p", "NBCUniversal CNBC Business UK"),
    ("English | News", "CNBC TV18", "CNBCTV18.in@SD", "https://n18syndication.akamaized.net/bpk-tv/CNBC_TV18_NW18_MOB/output01/master.m3u8", "IN", "1080p", "South Asia Financial & Market News"),
    ("English | News", "CNBC Arabiya", "CNBCArabiya.ae@SD", "https://cnbc-live.akamaized.net/cnbc/master.m3u8", "AE", "1080p", "Middle East Business & Finance"),
    ("English | News", "Reuters TV", "ReutersTV.us@SD", "https://amg00453-reuters-amg00453c1-rakuten-uk-2110.playouts.now.amagi.tv/playlist.m3u8", "US", "1080p", "Global Reuters Video Wire"),
    ("English | News", "CNA International", "CNAInternational.sg@SD", "https://mumt05.tangotv.in/87NeALx2CNA/index.m3u8", "SG", "576p", "Channel NewsAsia Singapore"),
    ("English | News", "CNA Originals", "CNAOriginals.sg@SD", "https://amg01082-cna-amg01082c1-rlaxx-us-11304.playouts.now.amagi.tv/playlist.m3u8", "SG", "1080p", "CNA Feature & Documentary News"),
    ("English | News", "WION", "WION.in@SD", "https://d7x8z4yuq42qn.cloudfront.net/index_7.m3u8", "IN", "1080p", "World Is One News International 1080p"),
    ("English | News", "Sky News Arabia", "SkyNewsArabia.ae@HD", "https://stream.skynewsarabia.com/hls/sna.m3u8", "AE", "1080p", "Sky News International Network"),

    # ================= SPORTS | FOOTBALL =================
    ("Sports | Football", "beIN SPORTS XTRA", "beINSPORTSXTRA.us@SD", "https://bein-xtra-bein.amagi.tv/playlist.m3u8", "US", "1080p", "beIN Sports Major Live Football & Highlights"),
    ("Sports | Football", "beIN SPORTS XTRA en Espanol", "beINSPORTSXTRAenEspanol.us@SD", "https://dc1644a9jazgj.cloudfront.net/beIN_Sports_Xtra_Espanol.m3u8", "US", "1080p", "beIN Sports Spanish Coverage (La Liga/Ligue 1)"),
    ("Sports | Football", "FIFA+ English", "FIFAPlus.uk@English", "https://ba3e2e93.wurl.com/master/f36d25e7e52f1ba8d7e56eb859c636563214f541/U2Ftc3VuZy1nYl9GSUZBUGx1c0VuZ2xpc2hfSExT/playlist.m3u8", "INT", "720p", "Official FIFA Matches, Archive & Documentaries"),
    ("Sports | Football", "CCTV-Storm Football", "CCTVStormFootball.cn@HD", "http://38.75.136.137:98/gslb/dsdqpub/fyzq.m3u8?auth=testpub", "CN", "1080p", "Dedicated Football Broadcaster"),
    ("Sports | Football", "ESPN", "ESPN.br@SD", "http://181.78.197.59:8000/play/a07z/index.m3u8", "BR", "1080p", "ESPN Major Football & Sports"),
    ("Sports | Football", "ESPN 3", "ESPN3.br@SD", "http://181.78.197.59:8000/play/a081/index.m3u8", "BR", "1080p", "ESPN European Football & Cups"),
    ("Sports | Football", "ESPN 4", "ESPN4.br@SD", "http://181.78.197.59:8000/play/a07n/index.m3u8", "BR", "1080p", "ESPN Premier League / UEFA Coverage"),
    ("Sports | Football", "Fox Sports 1", "FoxSports1.us@HD", "http://85.237.89.160:9590/usa-s/FOX-SPORTS-1/index.m3u8", "US", "720p", "Fox Sports International Football & Tournaments"),
    ("Sports | Football", "Setanta Sports 1 HD", "SetantaSports1.ru@HD", "https://fs.uplink.kz/setanta_sports_1_hd/mono.m3u8?token=onlinetv", "RU", "1080p", "Premier League & European Football Broadcaster"),
    ("Sports | Football", "Setanta Sports 2 Eurasia", "SetantaSports2Eurasia.ie@SD", "http://stream.mcquack.net/235/index.m3u8", "IE", "1080p", "La Liga, Serie A & Bundesliga"),
    ("Sports | Football", "Digi Sport 1 HD", "DigiSport1.ro@HD", "https://dokagents.site/live/digisport1/mono.m3u8", "RO", "576i", "Champions League, La Liga & Serie A"),
    ("Sports | Football", "Digi Sport 2 HD", "DigiSport2.ro@HD", "https://dokagents.site/live/digisport2/mono.m3u8", "RO", "1080i", "European Top-tier Football Broadcaster"),
    ("Sports | Football", "Fubo Sports Network", "FuboSportsNetwork.us@SD", "https://dnf08l6u6uxnz.cloudfront.net/master.m3u8", "US", "1080p", "Fubo TV Football & Sports Playout"),

    # ================= SPORTS | CRICKET =================
    ("Sports | Cricket", "Willow Sports", "WillowSports.us@SD", "https://d36r8jifhgsk5j.cloudfront.net/Willow_TV.m3u8", "US", "1080p", "Premier Dedicated Cricket Channel (ICC / PSL / IPL)"),
    ("Sports | Cricket", "Willow", "Willow.us@SD", "http://tvsen5.aynascope.net/willowhd/index.m3u8", "US", "720p", "Live International & T20 Cricket Network"),
    ("Sports | Cricket", "Ten Cricket", "TenCricket.in@SD", "http://103.151.60.162:2122/play/a0fj/index.m3u8?hls", "IN", "576p", "International Cricket & Archive"),
    ("Sports | Cricket", "Sony Sports Ten 1 HD", "SonySportsTen1.in@HD", "http://103.151.60.162:2122/play/a01c/index.m3u8?hls", "IN", "1080p", "Major Cricket & Bilateral Tours (ECB/CA/PCB)"),
    ("Sports | Cricket", "Sony Sports Ten 2 HD", "SonySportsTen2.in@HD", "http://103.151.60.162:2122/play/a01b/index.m3u8?hls", "IN", "1080p", "Cricket & International Sports Network"),
    ("Sports | Cricket", "Sony Sports Ten 3 Hindi HD", "SonySportsTen3Hindi.in@HD", "http://103.151.60.162:2122/play/a01t/index.m3u8?hls", "IN", "1080p", "Hindi Commentary Cricket Broadcaster"),
    ("Sports | Cricket", "Sony Sports Ten 5", "SonySportsTen5.in@SD", "http://103.151.60.162:2122/play/a028/index.m3u8?hls", "IN", "1080p", "Sony Pictures International Cricket Network"),
    ("Sports | Cricket", "Star Sports Select 1 HD", "StarSportsSelect1.in@HD", "http://103.151.60.162:2122/play/a026/index.m3u8?hls", "IN", "1080p", "Star Sports Premium Cricket & Global Sports"),
    ("Sports | Cricket", "Star Sports Select 2 HD", "StarSportsSelect2.in@HD", "http://103.151.60.162:2122/play/a027/index.m3u8?hls", "IN", "1080p", "Star Sports Live Cricket & Global Athletics"),
    ("Sports | Cricket", "Star Sports 2 HD", "StarSports2.in@HD", "http://103.151.60.162:2122/play/a00v/index.m3u8?hls", "IN", "720p", "Star Sports Cricket & Premier Tournaments"),

    # ================= SPORTS | F1 & MOTORSPORT =================
    ("Sports | F1 & Motorsport", "Motorvision", "Motorvision.de@SD", "https://mvg-mv-xumo.otteravision.com/mvg/mv/mv.m3u8", "DE", "1080p", "24/7 Motorsport, Car Racing & Documentaries"),
    ("Sports | F1 & Motorsport", "Sky Racing 1", "SkyRacing1.au@SD", "https://636ffd31f0e12.streamlock.net/RacingStream1/RacingStream1/playlist.m3u8", "AU", "720p", "Live Sky Racing Broadcast Network"),
    ("Sports | F1 & Motorsport", "FloRacing", "FloRacing.us@HD", "https://amg02278-amg02278c1-flosports-worldwide-7592.playouts.now.amagi.tv/playlist.m3u8", "US", "1080p", "Live Track Racing, Speed & Motorsport"),
    ("Sports | F1 & Motorsport", "F1 Channel", "F1Channel.ie@US", "https://amg12058-c15studio-amg12058c1-lg-us-5787.playouts.now.amagi.tv/playlist/amg12058-formulaone-f1channellg-us/playlist.m3u8", "INT", "1080p", "Official Formula 1 FAST Playout Channel"),

    # ================= SPORTS | UFC & COMBAT =================
    ("Sports | UFC & Combat", "Bellator MMA", "BellatorMMA.us@SD", "https://jmp2.uk/plu-5ebc8688f3697d00072f7cf8.m3u8", "US", "720p", "Live & Classic Bellator Mixed Martial Arts"),
    ("Sports | UFC & Combat", "FightBox HD", "FightBox.nl@HD", "https://nosignal1.antenaplay.ro/hls/fightbox-hd/index.m3u8", "NL", "1080p", "MMA, Kickboxing, Boxing & Combat Championships"),
    ("Sports | UFC & Combat", "FightBox", "FightBox.nl@SD", "https://webtvstream.bhtelecom.ba/fightbox.m3u8", "NL", "720p", "Combat Sports & Martial Arts Alternative Feed"),
    ("Sports | UFC & Combat", "Persiana Fight", "PersianaFight.fr@HD", "https://fighthls.persiana.live/hls/stream.m3u8", "FR", "1080p", "Combat Sports, UFC Highlights & MMA"),
    ("Sports | UFC & Combat", "Swerve Combat", "SwerveCombat.us@SD", "https://linear-253.frequency.stream/mt/roku/253/hls/master.m3u8", "US", "1080p", "MMA, Boxing & Combat Sports Channel"),
    ("Sports | UFC & Combat", "WWE Network", "WWENetwork.us@SD", "http://103.151.60.162:2122/play/a00p/index.m3u8?hls", "US", "1080p", "Professional Wrestling, PPV & Specials"),
    ("Sports | UFC & Combat", "Fight Network", "FightNetwork.ca@SD", "https://a-cdn.klowdtv.com/live2/fight_720p/playlist.m3u8", "CA", "720p", "Dedicated Combat Sports & Mixed Martial Arts"),

    # ================= SPORTS | OTHER =================
    ("Sports | Other", "Eurosport 4K Czechia", "Eurosport4KCzechia.cz@UHD", "http://88.212.15.19/live/esp_4k_atk/playlist.m3u8", "CZ", "2160p", "Eurosport 4K Multi-sport Broadcaster"),
    ("Sports | Other", "MLB", "MLB.us@SD", "https://aegis-cloudfront-1.tubi.video/36ef2f9d-7100-4c4d-b41a-dbf41ab7e461/playlist.m3u8", "US", "720p", "Major League Baseball Network"),
]

print(f"Total curated entries in updated catalog: {len(channels_catalog)}")

inventory = []
for group, name, tvg_id, url, country, resolution, notes in channels_catalog:
    orig = index_by_id.get(tvg_id, {})
    logo = orig.get('tvg_logo', '')
    if not logo:
        ch_id = tvg_id.split('@')[0]
        for e in all_index:
            if e['tvg_id'].startswith(ch_id) and e.get('tvg_logo'):
                logo = e['tvg_logo']
                break

    headers = orig.get('headers', [])
    
    item = {
        'group': group,
        'name': f"{name} ({resolution})" if resolution and f"({resolution})" not in name else name,
        'clean_name': name,
        'tvg_id': tvg_id,
        'tvg_name': name,
        'tvg_logo': logo,
        'url': url,
        'country': country,
        'resolution': resolution,
        'notes': notes,
        'source': 'iptv-org official streams',
        'headers': headers
    }
    inventory.append(item)

with open('final_inventory.json', 'w', encoding='utf-8') as f:
    json.dump(inventory, f, indent=2)

print(f"Updated final_inventory.json saved with {len(inventory)} channels.")
