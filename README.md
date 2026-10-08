# Pakistan & International IPTV Playlist

A curated, balanced, and verified Pakistan-focused IPTV playlist created exclusively from current public stream entries in the official [iptv-org/iptv](https://github.com/iptv-org/iptv) project.

## 📺 Single Online M3U URL (HotPlayer / IPTV Apps)

Once hosted on GitHub Pages:
```text
https://<YOUR-GITHUB-USERNAME>.github.io/pakistan-iptv/pakistan-iptv.m3u
```

Direct raw GitHub fallback URL:
```text
https://raw.githubusercontent.com/<YOUR-GITHUB-USERNAME>/pakistan-iptv/main/pakistan-iptv.m3u
```

---

## 🎯 Playlist Scope & Structure

The playlist is organized into four main sections and 14 organized groups:

### 1. Pakistan (25 Channels)
- **Pakistan | News**: Dunya News (720p), Samaa TV (576p), 92 News HD (720p), 24 News HD, Neo News (1080p), ABN News (360p), Capital TV, Lahore News (720p), News One (720p), 7 News (720p), Aik News, Such TV, KTN News, M News (1080p).
- **Pakistan | Entertainment**: Hum TV (720p), Bol Entertainment (HD), A-Plus TV, Masala TV (576p), Filmax (576p), 8XM (HD), Jalwa TV.
- **Pakistan | General**: Discover Pakistan (1080p), aurLife (614p).
- **Pakistan | Sports**: PK Sports (720p), M Sports (1080p).

### 2. Iran (24 Channels)
- **Iran | News**: IRINN (576p), Press TV (720p), Press TV French (1080p), Al Alam (360p), Iran Press, Iran International (1080p).
- **Iran | Entertainment**: iFilm English, iFilm Persian, iFilm Arabic, iFilm 2, FX 1, FX 2, Persiana Iranian, Bravo Farsi TV (360p), Cafe Film, Gold Star, NewFlix.
- **Iran | General**: IRIB 1, IRIB 2, IRIB 4, IRIB Mostanad, IRIB UHD (4K / 2160p).
- **Iran | Sports**: IRIB 3, Varzesh TV.

### 3. Major English-Language News (24 Channels)
- **English News**: Al Jazeera English (1080p), BBC News North America (1080p), BBC News South Asia (720p), DW English (1080p), France 24 English (1080p), Euronews English (720p), TRT World (720p), CGTN (1080p), NHK World-Japan (1080p), ABC News Live (720p), CBS News 24/7 (720p), NBC News NOW (1080p), Bloomberg TV Europe (720p), Bloomberg TV Asia (720p), Bloomberg Originals (1080p), Bloomberg TV+ (4K / 2160p), CNBC UK (1080p), CNBC TV18 (1080p), CNBC Arabiya (1080p), Reuters TV (1080p), CNA International (576p), CNA Originals (1080p), WION (1080p), Sky News Extra (1080p).

### 4. Sports (39 Channels)
- **Sports | Cricket (11 channels)**: Willow Sports (1080p), Willow (720p), Cricket Gold (1080p), Ten Cricket (576p), Sony Sports Ten 1 HD (1080p), Sony Sports Ten 2 HD (1080p), Sony Sports Ten 3 Hindi HD (1080p), Sony Sports Ten 5 (1080p), Star Sports Select 1 HD (1080p), Star Sports Select 2 HD (1080p), Star Sports 2 HD (720p).
- **Sports | Football (14 channels)**: beIN SPORTS XTRA (1080p), beIN SPORTS XTRA en Español (1080p), FIFA+ English (720p), CCTV-Storm Football (1080p), ESPN (1080p), ESPN 3 (1080p), ESPN 4 (1080p), Fox Sports 1 (720p), Setanta Sports 1 HD (1080p), Setanta Sports 2 Eurasia (1080p), Canal+ Sport 2 SK (1080p), Digi Sport 1 HD (576i), Digi Sport 2 HD (1080i), Fubo Sports Network (1080p).
- **Sports | F1 & Motorsport (4 channels)**: Motorvision (1080p), Sky Racing 1 (720p), FloRacing (1080p), F1 Channel (1080p).
- **Sports | UFC & Combat (7 channels)**: Bellator MMA (720p), FightBox HD (1080p), FightBox (720p), Persiana Fight (1080p), Swerve Combat (1080p), WWE Network (1080p), Fight Network (720p).
- **Sports | Other (3 channels)**: Eurosport 4K Czechia (2160p), NBC Sports NOW (1080p), MLB (720p).

---

## ⚙️ How to Regenerate the Playlist

Run the Python generator anytime to refresh or validate the playlist:
```bash
python generate_playlist.py
```

The GitHub Actions workflow (`.github/workflows/update-playlist.yml`) will also automatically run every week and deploy the updated playlist to GitHub Pages.

---

## 📱 How to Use in HotPlayer

1. Open your browser and navigate to the HotPlayer portal (e.g. `https://hotplayer.app/` or `https://hotplayer.org/`).
2. Enter your TV / Device MAC address and Device Key.
3. In **Add Playlist**, name it `Pakistan IPTV`.
4. Enter the online URL:
   `https://<YOUR-GITHUB-USERNAME>.github.io/pakistan-iptv/pakistan-iptv.m3u`
5. Save and reload HotPlayer on your TV.
