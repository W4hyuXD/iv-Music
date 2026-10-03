import time
import re
import requests
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.text import Text

console = Console()

# ambil lirik ter-sinkronisasi (.lrc) dari LRCLIB API.
def fetch_synced_lyrics(title: str, artist: str = "") -> str | None:
    clean_title = re.sub(r'\(.*?\)|\[.*?\]', '', title).strip()
    query = f"{clean_title} {artist}".strip()
    url = f"https://lrclib.net/api/search?q={requests.utils.quote(query)}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            results = response.json()
            for item in results:
                if item.get("syncedLyrics"):
                    return item["syncedLyrics"]
    except Exception:
        pass
    return None

#ubah format .lrc ([mm:ss.xx] teks) menjadi list [(timestamp_detik, teks_lirik)].
def parse_lrc(lrc_text: str) -> list[tuple[float, str]]:
    lyrics_data = []
    pattern = re.compile(r"\[(\d+):(\d+\.\d+)\](.*)")
    for line in lrc_text.splitlines():
        match = pattern.match(line)
        if match:
            minutes = float(match.group(1))
            seconds = float(match.group(2))
            text = match.group(3).strip()
            total_seconds = minutes * 60 + seconds
            lyrics_data.append((total_seconds, text))
    return sorted(lyrics_data, key=lambda x: x[0])

def render_lyrics_ui(lyrics_data: list[tuple[float, str]], current_index: int, song_title: str) -> Panel:
    ui_text = Text()
    start = max(0, current_index - 2)
    end = min(len(lyrics_data), current_index + 3)
    for i in range(start, end):
        _, line_text = lyrics_data[i]
        if not line_text:
            line_text = "🎵 ... 🎵"
        if i == current_index:
            ui_text.append(f"▶  {line_text}\n", style="bold yellow reverse")
        elif i < current_index:
            ui_text.append(f"   {line_text}\n", style="dim white")
        else:
            ui_text.append(f"   {line_text}\n", style="cyan")
    return Panel(
        Align.center(ui_text, vertical="middle"),
        title=f"[bold green]🎶 Playing: {song_title}[/bold green]",
        border_style="magenta",
        padding=(1, 2)
    )

def start_lyrics_animation(song_title: str, artist: str = "", delay_offset: float = 3.5):
    console.print(f"[cyan]🔎 Mengunduh lirik untuk {song_title}...[/cyan]")
    lrc_raw = fetch_synced_lyrics(song_title, artist)
    if not lrc_raw:
        console.print(f"\n[bold red][!] Lirik ter-sinkronisasi tidak ditemukan untuk:[/bold red] {song_title}\n")
        return
    lyrics_data = parse_lrc(lrc_raw)
    if not lyrics_data:
        console.print("\n[bold red][!] Format lirik tidak dapat diproses.[/bold red]\n")
        return
    # Hitung waktu mulai setelah lirik siap didownload
    start_time = time.time()
    current_idx = 0
    with Live(render_lyrics_ui(lyrics_data, current_idx, song_title), refresh_per_second=10, console=console) as live:
        while current_idx < len(lyrics_data):
            # Kurangi delay_offset agar waktu lirik disesuaikan dengan waktu MPV buffer
            elapsed_time = (time.time() - start_time) - delay_offset
            # Cari baris lirik yang paling sesuai dengan elapsed_time saat ini
            target_idx = 0
            for i, (timestamp, _) in enumerate(lyrics_data):
                if elapsed_time >= timestamp:
                    target_idx = i
                else:
                    break
            if target_idx != current_idx:
                current_idx = target_idx
                live.update(render_lyrics_ui(lyrics_data, current_idx, song_title))
            time.sleep(0.05)

