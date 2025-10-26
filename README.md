## IV - Music Player & Downloader 
> Music Downloader With iv.

> A tool that functions to play and download music from various platforms such as YouTube, Instagram, Tiktok, Facebook, and others.
## Installation 
```bash
$ pkg update -y && pkg upgrade -y
$ pkg i -y python git
$ git clone https://github.com/W4hyuXD/iv-Music.git
$ cd iv-Music
$ pip install -r requirements.txt
$ python3 iv.py -a "url music" -p
```

```bash
📘 IV Downloader — Command Reference
────────────────────────────────────────────
USAGE:
  python3 iv.py [options] <url / search query>

OPTIONS:
  -h,  --help            tampilkan bantuan ini
  -f,  --format          format output (audio/video)
  -a,  --abr             kualitas audio [64,128,192 kbps] (default: 128)
  -q,  --quality         kualitas video [144p–1080p]
  -p,  --play            putar audio langsung tanpa download
  -sr, --search          cari video/audio di YouTube (interaktif)
  -l,  --list-formats    tampilkan semua format video
      --min-duration     filter durasi minimal (detik)
      --max-duration     filter durasi maksimal (detik)
      --max-results      jumlah hasil pencarian [1–20] (default: 10)

INTERAKTIF MODE:
  Setelah menggunakan opsi -sr / --search, pilih hasil yang ingin
  Anda putar atau unduh langsung:
    • Pilih nomor hasil
    • Pilih mode: 1 = Putar | 2 = Download

ADVANCED:
  --force-web             Gunakan klien YouTube web-only (bypass SABR/403)

EXAMPLES:
  iv -sr "cigarettes after sex" --max-results 10 --min-duration 180
  iv -f mp4 -q 1080p "url video"
  iv -a 128 "url music" -p
  iv "link audio/video" (default mp3 128 kbps)
────────────────────────────────────────────
```
