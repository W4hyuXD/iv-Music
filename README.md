# Music-Downloader
> Music Downloader With iv.

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
  iv -a 128 "url audio" -p
  iv "link audio/video" (default mp3 128 kbps)
────────────────────────────────────────────
(📁 hasil download otomatis disimpan di /sdcard/Download/iv-Download)

📜 Source: https://github.com/w4hyuXD/iv-Music
```
