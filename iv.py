#!/usr/bin/env python3
# Created Saturday, 25 October 2025
# Copyright © WahyuDin Ambia XD

import sys, rich
import shutil
import subprocess
import os
import re
import threading
from rich import print as cetak
from colorama import Fore, Style, init
from lyrics_module import start_lyrics_animation

init(autoreset=True)
VERSION = "2.1.0"

# warna
A2 = "[#6a6a6a]" # ABU-ABU
M2, H2, K2, P2, B2, U2, O2 = ["[#FF0000]", "[#00FF00]", "[#FFFF00]", "[#FFFFFF]", "[#00C8FF]", "[#AF00FF]", "[#00FFFF]"]

_ansi_re = re.compile(r'\x1b\[[0-9;]*m')
def strip_ansi(s: str) -> str:
    if not s:
        return s
    return _ansi_re.sub('', s)

   # <!-- otomatis update library --->
def ensure_latest_ytdlp():
    try:
        import yt_dlp
        from yt_dlp import version as yv
        print(f"{Fore.LIGHTBLACK_EX}🔎 yt-dlp version: {yv.__version__}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception:
        cetak(f"[{M2}![/]] yt-dlp belum terinstall, menginstal sekarang...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    import yt_dlp
    return yt_dlp
yt_dlp = ensure_latest_ytdlp()

   # <!-- banner --->
def banner():
    logo = ''' _         .-..-.             _                               
:_;        : `' :            :_;                              
.-..-..-.  : .. :.-..-. .--. .-. .--.                         
: :: `; :  : :; :: :; :`._-.': :'  ..'                        
:_;`.__.'  :_;:_;`.__.'`.__.':_;`.__.'                      
.---.                      .-.                  .-.           
: .  :                     : :                  : :           
: :: : .--. .-..-..-.,-.,-.: :   .--.  .--.   .-' : .--. .--. 
: :; :' .; :: `; `; :: ,. :: :_ ' .; :' .; ; ' .; :' '_.': ..'
:___.'`.__.'`.__.__.':_;:_;`.__;`.__.'`.__,_;`.__.'`.__.':_;     '''
    cetak(logo)
    cetak(f"iv-downloader {H2}v{VERSION}[/] | powered by yt-dlp\n")

   # <!-- bantuan --->
def show_help():
    banner()
    print(f"""{Fore.CYAN}📘 IV Downloader — Command Reference{Style.RESET_ALL}
{Fore.LIGHTBLACK_EX}────────────────────────────────────────────────────────────────────────────────────────{Style.RESET_ALL}
Pemutar musik dan pengunduh interaktif modern yang dibuat untuk Termux,
dengan dukungan lengkap untuk daftar putar, ekstraksi audio, dan kontrol interaktif.
Platform yang didukung: {Fore.CYAN}YouTube, Instagram, TikTok, Facebook, dan lainnya.
{Fore.LIGHTBLACK_EX}────────────────────────────────────────────────────────────────────────────────────────{Style.RESET_ALL}
{Fore.LIGHTWHITE_EX}USAGE:
  python3 iv.py {Fore.CYAN}[options] {Fore.YELLOW}<url / search query>

{Fore.LIGHTWHITE_EX}OPTIONS:
{Fore.CYAN}  -h,  --help{Style.RESET_ALL}            tampilkan bantuan ini
{Fore.CYAN}  -f,  --format{Style.RESET_ALL}          format output {Fore.YELLOW}(audio/video)
{Fore.CYAN}  -a,  --abr{Style.RESET_ALL}             kualitas audio {Fore.CYAN}[64,128,192 kbps] {Fore.YELLOW}(default: 128)
{Fore.CYAN}  -q,  --quality{Style.RESET_ALL}         kualitas video{Fore.CYAN} [144p–1080p]
{Fore.CYAN}  -p,  --play{Style.RESET_ALL}            putar audio langsung tanpa download
{Fore.CYAN}  -v,  --video{Style.RESET_ALL}           download video
{Fore.CYAN}  -sr, --search{Style.RESET_ALL}          cari audio/video secara interaktif
{Fore.CYAN}  -l,  --list-formats{Style.RESET_ALL}    tampilkan semua format video
{Fore.CYAN}      --min-duration{Style.RESET_ALL}     filter durasi minimal {Fore.YELLOW}(detik)
{Fore.CYAN}      --max-duration{Style.RESET_ALL}     filter durasi maksimal {Fore.YELLOW}(detik)
{Fore.CYAN}      --max-results{Style.RESET_ALL}      jumlah hasil pencarian {Fore.YELLOW}[1–20] {Fore.CYAN}(default: 10)

{Fore.LIGHTWHITE_EX}INTERAKTIF MODE:
  • Saat menggunakan {Fore.CYAN}-sr {Style.RESET_ALL}/ {Fore.CYAN}--search{Style.RESET_ALL}, pilih hasil dari daftar:
      1 = Putar langsung
      2 = Download audio {Fore.CYAN}(.mp3){Style.RESET_ALL}
  • Saat membuka URL playlist, pilih opsi:
      1 = Putar semua audio
      2 = Download semua audio {Fore.CYAN}(.mp3){Style.RESET_ALL}
      3 = Download semua video {Fore.CYAN}(.mp4){Style.RESET_ALL}
      4 = Convert Video to Audio
      5 = Lihat daftar & pilih satu item
      6 = Keluar

{Fore.LIGHTWHITE_EX}EXAMPLES:{Style.RESET_ALL}
  iv {Fore.CYAN}-sr {Fore.YELLOW}"cigarettes after sex" {Fore.CYAN}--max-results 10 --min-duration 3600{Style.RESET_ALL}
  iv {Fore.CYAN}-f mp4 -q 240p {Fore.YELLOW}"url video"{Style.RESET_ALL}
  iv {Fore.CYAN}-a 64 {Fore.YELLOW}"url audio" {Fore.CYAN}-p{Style.RESET_ALL}
  iv {Fore.YELLOW}"link video/audio"        {Fore.CYAN}(default: mp3 128 kbps){Style.RESET_ALL}
  iv {Fore.CYAN}"https://www.youtube.com/playlist?list=..."  {Fore.YELLOW}(playlist mode){Style.RESET_ALL}
{Fore.LIGHTBLACK_EX}────────────────────────────────────────────────────────────────────────────────────────{Style.RESET_ALL}
📁 Semua hasil disimpan otomatis ke: {Fore.CYAN}/sdcard/Download/iv-Download/{Style.RESET_ALL}
  (Playlist akan dibuatkan folder terpisah)

{Style.RESET_ALL}📦 Module: yt-dlp + ffmpeg + mpv
{Style.RESET_ALL}📜 Source: {Fore.CYAN}https://github.com/W4hyuXD/iv-Music{Style.RESET_ALL}
""")

   # <!-- cek dependenci --->
def check_ffmpeg_mpv():
    if shutil.which("ffmpeg") is None:
        cetak(f"[{M2}x[/]]ffmpeg tidak ditemukan! Install: {H2}pkg install ffmpeg -y")
        sys.exit(1)
    if shutil.which("mpv") is None:
        cetak(f"[{M2}x[/]]mpv tidak ditemukan! Install: {H2}pkg install mpv -y")
        sys.exit(1)

   # <!-- Download Progress --->
def progress_hook(d):
    status = d.get('status')
    if status == 'downloading':
        percent = strip_ansi(d.get('_percent_str', '0%')).strip()
        speed = strip_ansi(d.get('_speed_str', '0 KiB/s'))
        eta = strip_ansi(d.get('_eta_str', '??:??'))
        cetak(f"[{H2}↓[/]] {H2}{percent}[/] | {H2}{speed}[/] | ETA {H2}{eta}[/]   ", end="\r")
    elif status == 'finished':
        cetak(f"\n[{H2}✓[/]]Selesai: {H2}{d.get('filename')}")

   # <!-- Subprocess MPV Quiet --->
def _run_mpv_quiet(url, abr="128"):
    cmd = [
        "mpv",
        "--no-video",
        "--really-quiet",
        "--demuxer-max-bytes=10M",
        "--demuxer-max-back-bytes=5M",
        f"--ytdl-format=bestaudio[abr>={abr}]",
        url
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

   # <!-- puter musik --->
def play_audio(url, title="", abr="128", is_playlist=False):
    song_title = title
    artist = ""
    if not song_title or song_title == "Streaming":
        cetak(f"[🔎] Mengambil info lagu...")
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}}
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                song_title = info.get("title", "")
        except Exception:
            pass
    cetak(f"[▶️] Memutar audio langsung ({H2}{abr} kbps[/])...")
    t = threading.Thread(target=_run_mpv_quiet, args=(url, abr), daemon=True)
    t.start()
    if "-" in song_title:
        parts = song_title.split("-", 1)
        artist = parts[0].strip()
        song_title = parts[1].strip()
    if song_title:
        start_lyrics_animation(song_title=song_title, artist=artist, delay_offset=4.8)
    t.join()

   # <!-- pilih format url --->
def pick_format(info, quality):
    formats = [f for f in info.get('formats', []) if f.get('height')]
    if not formats:
        return None
    available = sorted(set(int(f['height']) for f in formats))
    try:
        target = int(quality)
    except Exception:
        target = max(available)
    if target in available:
        chosen = max([f for f in formats if int(f['height']) == target], key=lambda x: x.get('tbr') or 0)
        return chosen['format_id']
    fallback = max(available)
    chosen = max([f for f in formats if int(f['height']) == fallback], key=lambda x: x.get('tbr') or 0)
    cetak(f"[{M2}![/]] {H2}{target}p [/]tidak tersedia, fallback {H2}{fallback}p")
    return chosen['format_id']

def prompt_convert_to_mp3(video_path, abr="128"):
    try:
        ans = input(f"\n[?] Convert video ke MP3? (y/n): ").strip().lower()
        if ans != "y":
            return
        mp3_path = os.path.splitext(video_path)[0] + ".mp3"
        cetak(f"[•] Mengkonversi ke MP3 ({H2}{abr} kbps[/])...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",
            "-ab", f"{abr}k",
            mp3_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cetak(f"[{H2}✓[/]] Berhasil: {mp3_path}")
    except Exception as e:
        cetak(f"[{M2}x[/]] Gagal convert: {M2}{e}")

   # <!-- Download audio/video tunggal --->
def download(url, ext="mp3", quality="720", abr="128", is_playlist=False, playlist_title=None, video_mode=False):
    audio_formats = ["mp3", "m4a", "opus", "aac", "wav"]
    base_output = "/sdcard/Download/iv-Download"
    if is_playlist and playlist_title:
        safe_title = re.sub(r'[\\/:"*?<>|]+', '_', playlist_title).strip() or "playlist"
        output_dir = os.path.join(base_output, safe_title)
        os.makedirs(output_dir, exist_ok=True)
        outtmpl = os.path.join(output_dir, "%(playlist_index)03d - %(title)s.%(ext)s")
    else:
        output_dir = base_output
        os.makedirs(output_dir, exist_ok=True)
        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")
    common_opts = {
        "outtmpl": outtmpl,
        "noplaylist": False if is_playlist else True,
        "progress_hooks": [progress_hook],
        "continuedl": True,
        "retries": 20,
        "fragment_retries": 20,
        "socket_timeout": 60,
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
    }
    try:
        with yt_dlp.YoutubeDL(common_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if ext in audio_formats:
                opts = {
                    **common_opts,
                    "format": "bestaudio[ext=m4a]/bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": ext,
                        "preferredquality": abr,
                    }],
                }
            else:
                fmt = pick_format(info, quality)
                if not fmt:
                    cetak(f"[{M2}x[/]] Tidak ada format video valid")
                    return
                opts = {
                    **common_opts,
                    "format": f"{fmt}+bestaudio/best",
                    "merge_output_format": ext,
                }
            with yt_dlp.YoutubeDL(opts) as y:
                info = y.extract_info(url, download=True)
        cetak(f"\n[{H2}✓[/]] File disimpan ke: {H2}{output_dir}")
        if video_mode and ext not in audio_formats:
            try:
                filename = y.prepare_filename(info)
                prompt_convert_to_mp3(filename, abr)
            except Exception:
                pass
    except Exception as e:
        cetak(f"[{M2}x[/]] Error: {M2}{str(e)}")

   # <!-- Fitur Searching Music --->
def search_youtube(query, max_results=10, min_duration=0, max_duration=None, force_web=False):
    cetak(f"[🔍] Mencari: {H2}{query}[/] ...")
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "noplaylist": True,
        "default_search": "ytsearch",
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
    }
    if force_web:
        ydl_opts["extractor_args"] = {"youtube": {"player_client": ["web"]}}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
        if not info or "entries" not in info or not info["entries"]:
            ydl_opts["default_search"] = "ytsearchddg"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearchddg{max_results}:{query}", download=False)
        entries = info.get("entries", [])
        if not entries:
            cetak(f"[{M2}x[/]] Tidak ditemukan hasil untuk '{query}'")
            return
        filtered = []
        for e in entries:
            dur = int(e.get("duration") or 0)
            if dur < int(min_duration):
                continue
            if max_duration and dur > int(max_duration):
                continue
            filtered.append(e)
        if not filtered:
            cetak(f"[{M2}![/]] Tidak ada hasil yang sesuai durasi filter")
            return
        cetak(f"[{H2}✓{P2}] Menemukan {H2}{len(filtered)}[/] hasil:\n")
        for i, e in enumerate(filtered[:max_results], start=1):
            dur = int(e.get("duration") or 0)
            dur_min, dur_sec = divmod(dur, 60)
            title = e.get("title", "Tidak ada judul")
            url = e.get("webpage_url") or e.get("url") or ""
            if url and not url.startswith("http"):
                url = f"https://www.youtube.com/watch?v={url}"
            cetak(f"[{i}] {title} ({dur_min}:{dur_sec:02d}) [{A2}{url}[/]]")
        cetak(f"\n[•] Pilih URL yang ingin anda Putar/Download:")
        choice = input(f"[•] Masukkan nomor [1-{len(filtered)}]: ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if idx < 0 or idx >= len(filtered):
            return
        picked = filtered[idx]
        url = picked.get("webpage_url") or picked.get("url")
        if url and not url.startswith("http"):
            url = f"https://www.youtube.com/watch?v={url}"
        action = input(f"\n[?] Mau Putar Langsung / Download [1/2]: ").strip()
        if action == "1":
            cetak(f"[▶️] Memutar: [#00e83e]{picked.get('title')}")
            play_audio(url, title=picked.get("title", ""), abr="128", is_playlist=False)
        elif action == "2":
            cetak(f"[[#19e800]↓[/]] Mengunduh: {H2}{picked.get('title')}")
            download(url, "mp3", "720", "128", is_playlist=False)
        else:
            cetak(f"[[#e80000]![/]] Pilihan tidak valid.")
    except Exception as e:
        cetak(f"[[#e80000]![/]] Error: {str(e)}")

# <!-- Playlist Handler --->
def handle_playlist_interactive(url):
    try:
        ydl_opts = {"quiet": True, "skip_download": True, "extract_flat": True,
                    "extractor_args": {"youtube": {"player_client": ["web", "android"]}}}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        pl_title = info.get("title", "playlist")
        entries = info.get("entries") or []
        if not entries:
            cetak(f"[[#e80000]x[/]] Playlist kosong atau tidak dapat dibaca.")
            return
        cetak(f"{Fore.LIGHTCYAN_EX}[🎶] Playlist terdeteksi: {pl_title}")
        cetak(f"[•] Jumlah item: {H2}{len(entries)}[/]\n")
        cetak(f"[?] Mau yang mana nih?")
        cetak(" [1] Putar langsung seluruh playlist (audio only)")
        cetak(" [2] Download seluruh playlist (audio .mp3)")
        cetak(" [3] Download seluruh playlist (video .mp4)")
        cetak(" [4] Lihat daftar Playlist")
        cetak(" [5] Keluar")
        sel = input("[•] Pilih : ").strip()
        if sel == "1":
            b = input("[•] Gunakan bitrate audio [64/128/192] (default 128): ").strip()
            if b not in ["64","128","192"]:
                b = "128"
            cetak(f"[▶️] Memutar seluruh playlist (audio {b} kbps)...")
            play_audio(url, title=pl_title, abr=b, is_playlist=True)
            return
        if sel == "2":
            b = input("[•] Kualitas audio untuk download [64/128/192] (default 128): ").strip()
            if b not in ["64","128","192"]:
                b = "128"
            cetak(f"[{H2}↓[/]] Mengunduh seluruh playlist sebagai .mp3 (bitrate {b}) ...")
            download(url, ext="mp3", quality="720", abr=b, is_playlist=True, playlist_title=pl_title)
            return
        if sel == "3":
            q = input("[•] Kualitas video untuk download [144/240/360/480/720/1080] (default 720): ").strip()
            if q not in ["144","240","360","480","720","1080"]:
                q = "720"
            cetak(f"[{H2}↓[/]] Mengunduh seluruh playlist sebagai .mp4 (res {q}p) ...")
            download(url, ext="mp4", quality=q, abr="128", is_playlist=True, playlist_title=pl_title)
            return
        if sel == "4":
            cetak(f"\n[•] Daftar item:")
            for i, e in enumerate(entries, start=1):
                title = e.get("title", "Tidak ada judul")
                dur = int(e.get("duration") or 0)
                dur_min, dur_sec = divmod(dur, 60)
                vid = e.get("id") or e.get("url") or ""
                if vid and not vid.startswith("http"):
                    display_vid = f"https://www.youtube.com/watch?v={vid}"
                else:
                    display_vid = vid
                cetak(f"[{i}] {title} ({dur_min}:{dur_sec:02d}) — {display_vid}")
            pick = input(f"\n[•] Pilih  [1-{len(entries)}]: ").strip()
            if not pick.isdigit():
                return
            idx = int(pick) - 1
            if idx < 0 or idx >= len(entries):
                return
            chosen = entries[idx]
            vid = chosen.get("id") or chosen.get("url")
            if vid and not vid.startswith("http"):
                vid = f"https://www.youtube.com/watch?v={vid}"
            action = input("\n[?] Mau Putar / Download (mp3) / Download (mp4) [1-3]: ").strip()
            if action == "1":
                cetak(f"[▶️] Memutar: {H2}{chosen.get('title')}")
                play_audio(vid, title=chosen.get("title", ""), abr="128", is_playlist=False)
            elif action == "2":
                b = input("[•] Kualitas audio [64/128/192] (default 128): ").strip()
                if b not in ["64","128","192"]:
                    b = "128"
                cetak(f"[{H2}↓[/]] Mengunduh: {H2}{chosen.get('title')} (mp3, {b} kbps)")
                download(vid, ext="mp3", quality="720", abr=b, is_playlist=False)
            elif action == "3":
                q = input("[•] Kualitas video [144/240/360/480/720/1080] (default 720): ").strip()
                if q not in ["144","240","360","480","720","1080"]:
                    q = "720"
                cetak(f"[{H2}↓[/]] Mengunduh: {H2}{chosen.get('title')} (mp4, {q}p)")
                download(vid, ext="mp4", quality=q, abr="128", is_playlist=False)
            else:
                cetak(f"[{M2}x[/]]Pilihan tidak valid.")
            return
        if sel == "5":
            cetak(f"[•] See you again...!")
            return
        cetak(f"[{M2}x[!]]Pilihan tidak valid.")
    except Exception as e:
        cetak(f"[{M2}x[/]]Error: {M2}{str(e)}")

   # <!-- Url Playlist Detector --->
def is_playlist_url(url: str) -> bool:
    if not url:
        return False
    u = url.lower()
    return ("playlist?list=" in u) or ("&list=" in u) or ("?list=" in u)

   # <!-- CLI --->
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 or "-h" in args or "--help" in args:
        show_help()
        sys.exit(0)
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    check_ffmpeg_mpv()
    ext, quality, abr = "mp3", "720", "128"
    force_web = "--force-web" in args
    video_mode = "-v" in args
    if "-f" in args or "--format" in args:
        try:
            idx = args.index("-f") if "-f" in args else args.index("--format")
            ext = args[idx + 1].replace(".", "").lower()
        except Exception:
            pass
    if "-q" in args or "--quality" in args:
        try:
            idx = args.index("-q") if "-q" in args else args.index("--quality")
            quality = args[idx + 1].replace("p", "")
        except Exception:
            pass
    if "-a" in args or "--abr" in args:
        try:
            idx = args.index("-a") if "-a" in args else args.index("--abr")
            abr = args[idx + 1]
        except Exception:
            pass
    # <!-- search --->
    if "-sr" in args or "--search" in args:
        try:
            idx = args.index("-sr") if "-sr" in args else args.index("--search")
            query = args[idx + 1]
        except Exception:
            cetak(f"{Fore.RED}[x]Gunakan: -sr \"query\"")
            sys.exit(1)
        max_results = 10
        min_duration = 0
        max_duration = None
        if "--max-results" in args:
            try:
                max_results = int(args[args.index("--max-results") + 1])
            except Exception:
                pass
        if "--min-duration" in args:
            try:
                min_duration = int(args[args.index("--min-duration") + 1])
            except Exception:
                pass
        if "--max-duration" in args:
            try:
                max_duration = int(args[args.index("--max-duration") + 1])
            except Exception:
                pass
        search_youtube(query, max_results=max_results, min_duration=min_duration, max_duration=max_duration, force_web=force_web)
        sys.exit(0)
    # <!-- Pemutaran URL Tunggal / Playlist --->
    target_url = args[-1]
    if is_playlist_url(target_url):
        handle_playlist_interactive(target_url)
    elif "-p" in args or "--play" in args:
        play_audio(target_url, abr=abr)
    else:
        download(target_url, ext=ext, quality=quality, abr=abr, video_mode=video_mode)

