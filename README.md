#  iv-Music Player & Downloader
> A modern, interactive music player and downloader built for Termux.
Fully supports playlists, audio extraction, and interactive controls. 
Supported platforms: YouTube, Instagram, TikTok, Facebook, and others.

Powered by [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), [`ffmpeg`](https://ffmpeg.org), and [`mpv`](https://mpv.io).

---

##  Features

- Download **audio** (MP3, M4A, OPUS, AAC, WAV)
- Download **video** (MP4, MKV, etc.)
- **Interactive search** mode
- Convert Mp4 to Mp3
- **Playlist mode** (play/download all or choose individual items)
- Auto-update `yt-dlp` each run
- Output saved to `/sdcard/Download/iv-Download/`
- Auto-create folders for playlists

---

##  Installation

```bash
pkg install python ffmpeg mpv -y
pip install yt-dlp colorama
```

Clone this repo:
```bash
git clone https://github.com/W4hyuXD/iv-Music.git
cd iv-Music
```

Run:
```bash
python3 iv.py -h
```
---

##  Usage

### Basic commands

| Command | Description |
|----------|--------------|
| `iv -a <url>` | Download single video/audio (default: mp3 128kbps) |
| `iv -v "<url>"` | Download Video (Selected Best Resolution)|
| `iv -p <url>` | Play audio directly (no download) |
| `iv -sr "query"` | Search interactively on YouTube |
| `iv -f mp4 -q 720p <url>` | Download specific format/resolution |
| `iv <playlist_url>` | Enter playlist interactive mode |


## Interactive Playlist Mode

When you open a playlist URL, you can choose:
```
1. Play all audio
2. Download all audio (.mp3)
3. Download all videos (.mp4)
4. View list & pick one item
5. Exit
```

---

## Examples

```bash
# Search and play directly
python3 iv.py -sr "cigarettes after sex" --max-results 5

# Download a video at 720p
python3 iv.py -f mp4 -q 720p "https://youtu.be/example"

# Play a YouTube playlist
python3 iv.py -a "https://www.youtube.com/playlist?list=PLabc123xyz"
```

---

## Output

```
/sdcard/Download/iv-Download/
├── my-song.mp3
├── my-video.mp4
└── <playlist name>/
    ├── 001 - first track.mp3
    ├── 002 - second track.mp3
```

---

## Dependencies

- Python 3.12.11
- ffmpeg
- mpv
- yt-dlp (auto-updated)

---

## 🪶 Credits

- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [`ffmpeg`](https://ffmpeg.org)
- [`mpv`](https://mpv.io)
- [`colorama`](https://pypi.org/project/colorama/)

---

## 📜 License

MIT License © 2025 [@WahyuDin Ambia](https://github.com/w4hyuXD)
