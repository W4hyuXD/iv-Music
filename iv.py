#!/usr/bin/env python3 | coding=utf-8
# Created Saturday, 25 October 2025
# By WahyuXD
import sys
import shutil
import subprocess
import os, time, re
from colorama import Fore, Style, init

init(autoreset=True)
VERSION = "1.0.0"

# <!-- Auto update yt-dlp --->
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
        print(f"{Fore.YELLOW}⚠️ yt-dlp belum terinstall, menginstal sekarang...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    finally:
        import yt_dlp
        return yt_dlp

yt_dlp = ensure_latest_ytdlp()

def banner():
    logo = f'''{Fore.CYAN} _         .-..-.             _
:_;        : `' :            :_;                              
.-..-..-.  : .. :.-..-. .--. .-. .--.                         
: :: `; :  : :; :: :; :`._-.': :'  ..'                        
:_;`.__.'  :_;:_;`.__.'`.__.':_;`.__.'                      
.---.                      .-.                  .-.           
: .  :                     : :                  : :           
: :: : .--. .-..-..-.,-.,-.: :   .--.  .--.   .-' : .--. .--. 
: :; :' .; :: `; `; :: ,. :: :_ ' .; :' .; ; ' .; :' '_.': ..'
:___.'`.__.'`.__.__.':_;:_;`.__;`.__.'`.__,_;`.__.'`.__.':_;{Style.RESET_ALL}     '''
    print(logo)


def show_help():
    banner()
    print(f"""{Fore.CYAN}📘 IV Downloader — Command Reference{Style.RESET_ALL}
{Fore.LIGHTBLACK_EX}────────────────────────────────────────────
{Fore.YELLOW}USAGE:{Style.RESET_ALL}
  python3 iv.py {Fore.CYAN}[options] {Fore.YELLOW}<url / search query>{Style.RESET_ALL}

{Fore.YELLOW}OPTIONS:{Style.RESET_ALL}
 {Fore.CYAN} -h,  --help{Style.RESET_ALL}            tampilkan bantuan ini
 {Fore.CYAN} -f,  --format{Style.RESET_ALL}          format output {Fore.YELLOW}(audio/video)
 {Fore.CYAN} -a,  --abr{Style.RESET_ALL}             kualitas audio {Fore.CYAN}[64,128,192 kbps] {Fore.YELLOW}(default: 128){Style.RESET_ALL}
 {Fore.CYAN} -q,  --quality{Style.RESET_ALL}         kualitas video {Fore.CYAN}[144p–1080p]{Style.RESET_ALL}
 {Fore.CYAN} -p,  --play{Style.RESET_ALL}            putar audio langsung tanpa download
 {Fore.CYAN} -sr, --search{Style.RESET_ALL}          cari video/audio di YouTube{Fore.YELLOW} (interaktif)
 {Fore.CYAN} -l,  --list-formats{Style.RESET_ALL}    tampilkan semua format video
 {Fore.CYAN}     --min-duration{Style.RESET_ALL}     filter durasi minimal {Fore.YELLOW}(detik)
 {Fore.CYAN}     --max-duration{Style.RESET_ALL}     filter durasi maksimal {Fore.YELLOW}(detik)
 {Fore.CYAN}     --max-results{Style.RESET_ALL}      jumlah hasil pencarian {Fore.CYAN}[1–20] {Fore.YELLOW}(default: 10)

{Fore.YELLOW}INTERAKTIF MODE:{Style.RESET_ALL}
  Setelah menggunakan opsi{Fore.CYAN} -sr / --search{Style.RESET_ALL}, pilih hasil yang ingin
  Anda putar atau unduh langsung:
    • Pilih nomor hasil
    • Pilih mode: 1 = Putar | 2 = Download

{Fore.YELLOW}ADVANCED:{Style.RESET_ALL}
 {Fore.CYAN} --force-web           {Style.RESET_ALL}  Gunakan klien YouTube web-only {Fore.YELLOW}(bypass SABR/403)

{Fore.YELLOW}EXAMPLES:{Style.RESET_ALL}
  iv {Fore.CYAN}-sr {Fore.YELLOW}"cigarettes after sex"{Fore.CYAN} --max-results 10 {Fore.CYAN}--min-duration 180{Style.RESET_ALL}
  iv {Fore.CYAN}-f mp4 -q 1080p {Fore.YELLOW}"url video"{Style.RESET_ALL}
  iv -a 128 "url audio" -p
  iv {Fore.YELLOW}"link audio/video" {Fore.CYAN}(default mp3 128 kbps)
{Fore.LIGHTBLACK_EX}────────────────────────────────────────────
{Fore.LIGHTBLACK_EX}(📁 hasil download otomatis disimpan di /sdcard/Download/iv-Download)

{Fore.LIGHTBLACK_EX}📜 Source: https://github.com/w4hyuXD/Play-Music
""")


def check_ffmpeg_mpv():
    if shutil.which("ffmpeg") is None:
        print(f"{Fore.LIGHTRED_EX}❌ ffmpeg tidak ditemukan! Install: pkg install ffmpeg -y")
        sys.exit(1)
    if shutil.which("mpv") is None:
        print(f"{Fore.LIGHTRED_EX}❌ mpv tidak ditemukan! Install: pkg install mpv -y")
        sys.exit(1)

spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
spinner_index = 0
last_update = 0

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def progress_hook(d):
    global spinner_index, last_update
    if d.get('status') == 'downloading':
        now = time.time()
        if now - last_update < 0.1:
            return
        last_update = now
        percent_str = d.get('_percent_str', '0%')
        percent_clean = ansi_escape.sub('', percent_str).strip('%')  # 🧩 hapus warna ANSI
        try:
            percent = float(percent_clean)
        except:
            percent = 0.0
        speed = ansi_escape.sub('', d.get('_speed_str', '0 KiB/s'))
        eta = d.get('_eta_str', '??:??')
        bar_len = 25
        filled_len = int(bar_len * percent / 100)
        bar = '█' * filled_len + '░' * (bar_len - filled_len)
        spinner = spinner_frames[spinner_index % len(spinner_frames)]
        spinner_index += 1
        sys.stdout.write(
            f"\r{Fore.CYAN}{spinner} [{bar}] {percent:5.1f}% | {speed:>10} | ETA {eta}"
        )
        sys.stdout.flush()
    elif d.get('status') == 'finished':
        sys.stdout.write(f"\r{Fore.GREEN}✅ Download selesai!{ d.get('filename')}\n")
        sys.stdout.flush()
       # print(f"\n{Fore.GREEN}✅ Selesai: {d.get('filename')}")


def play_audio(url, abr="128"):
    print(f"{Fore.LIGHTCYAN_EX}▶️ Memutar audio langsung ({abr} kbps)...")
    cmd = ["mpv", "--no-video", "--no-cache", f"--ytdl-format=bestaudio[abr>={abr}]"]
    cmd.append(url)
    subprocess.run(cmd)


def pick_format(info, quality):
    formats = [f for f in info['formats'] if f.get('height')]
    if not formats:
        return None
    available = sorted(set(f['height'] for f in formats))
    target = int(quality)
    if target in available:
        chosen = max([f for f in formats if f['height'] == target], key=lambda x: x.get('tbr') or 0)
        return chosen['format_id']
    fallback = max(available)
    chosen = max([f for f in formats if f['height'] == fallback], key=lambda x: x.get('tbr') or 0)
    print(f"{Fore.LIGHTYELLOW_EX}⚠️ {target}p tidak tersedia, fallback {fallback}p")
    return chosen['format_id']


def download(url, ext="mp3", quality="720", abr="128"):
    import yt_dlp
    audio_formats = ["mp3", "m4a", "opus", "aac", "wav"]
    output_dir = "/sdcard/Download/iv-Download"
    os.makedirs(output_dir, exist_ok=True)
    common_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "noplaylist": True,
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
                    print(f"{Fore.RED}❌ Tidak ada format video valid")
                    return
                opts = {**common_opts, "format": f"{fmt}+bestaudio/best", "merge_output_format": ext}
            with yt_dlp.YoutubeDL(opts) as y:
                y.download([url])
        print(f"\n{Fore.GREEN}✅ File disimpan ke: {output_dir}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {str(e)}")


# === Search + Interactive ===
def search_youtube(query, max_results=10, min_duration=0, max_duration=None, force_web=False):
    print(f"{Fore.CYAN}🔍 Mencari: {query} ...")
    ydl_opts = {
        "quiet": True, "skip_download": True,
        "extract_flat": True, "noplaylist": True,
        "default_search": "ytsearch",
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
    }
    if force_web:
        ydl_opts["extractor_args"] = {"youtube": {"player_client": ["web"]}}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
        entries = info.get("entries", [])
        if not entries:
            print(f"{Fore.RED}❌ Tidak ditemukan hasil untuk '{query}'")
            return
        filtered = [e for e in entries if int(e.get("duration") or 0) >= int(min_duration)]
        print(f"{Fore.LIGHTCYAN_EX}🔎 Menemukan {len(filtered)} hasil:\n")
        for i, e in enumerate(filtered[:max_results], start=1):
            dur = int(e.get("duration") or 0)
            dur_min, dur_sec = dur // 60, dur % 60
            title = e.get("title", "Tidak ada judul")
            url = e.get("webpage_url") or e.get("url") or ""
            if url and not url.startswith("http"):
                url = f"https://www.youtube.com/watch?v={url}"
            print(f"[{i}] {title} ({dur_min}:{dur_sec:02d}) — {Fore.LIGHTBLACK_EX}{url}")
        # <!--- Interactive Mode --->
        print(f"\n{Fore.YELLOW}Pilih URL yang ingin anda Putar/Download:")
        choice = input(f"Masukkan nomor [1-{len(filtered)}]: ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if idx < 0 or idx >= len(filtered):
            return
        url = filtered[idx].get("webpage_url") or filtered[idx].get("url")
        if url and not url.startswith("http"):
            url = f"https://www.youtube.com/watch?v={url}"
        action = input(f"\nMau 1. Putar Langsung / 2. Download [1, 2]: ").strip()
        if action == "1":
            print(f"{Fore.CYAN}▶️ Memutar: {filtered[idx]['title']}")
            play_audio(url)
        elif action == "2":
            print(f"{Fore.GREEN}⬇️ Mengunduh: {filtered[idx]['title']}")
            download(url, "mp3", "720", "128")
        else:
            print(f"{Fore.RED}❌ Pilihan tidak valid.")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {str(e)}")


# <!-- CLI --->
if __name__ == "__main__":
    check_ffmpeg_mpv()
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    # <!-- penanganan flag bantuan lebih awal --->
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        sys.exit(0)
    url = sys.argv[-1]
    ext, quality, abr = "mp3", "720", "128"
    force_web = "--force-web" in sys.argv
    if "-f" in sys.argv or "--format" in sys.argv:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        idx = sys.argv.index("-f") if "-f" in sys.argv else sys.argv.index("--format")
        ext = sys.argv[idx + 1].replace(".", "").lower()
    if "-q" in sys.argv or "--quality" in sys.argv:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        idx = sys.argv.index("-q") if "-q" in sys.argv else sys.argv.index("--quality")
        quality = sys.argv[idx + 1].replace("p", "")
    if "-a" in sys.argv or "--abr" in sys.argv:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        idx = sys.argv.index("-a") if "-a" in sys.argv else sys.argv.index("--abr")
        abr = sys.argv[idx + 1]
    # <!-- fitur search --->
    if "-sr" in sys.argv or "--search" in sys.argv:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        idx = sys.argv.index("-sr") if "-sr" in sys.argv else sys.argv.index("--search")
        query = sys.argv[idx + 1]
        max_results = 10
        min_duration = 0
        max_duration = None
        if "--max-results" in sys.argv:
            max_results = int(sys.argv[sys.argv.index("--max-results") + 1])
        if "--min-duration" in sys.argv:
            min_duration = int(sys.argv[sys.argv.index("--min-duration") + 1])
        if "--max-duration" in sys.argv:
            max_duration = int(sys.argv[sys.argv.index("--max-duration") + 1])
        search_youtube(query, max_results, min_duration, max_duration, force_web)
        sys.exit(0)
    # <!-- play atau download --->
    if "-p" in sys.argv or "--play" in sys.argv:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        play_audio(url, abr)
    else:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        download(url, ext, quality, abr)
