import time
import re
import requests
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()

# Ambil Lirik
def fetch_synced_lyrics(title: str, artist: str = "") -> str | None:
    clean_title = re.sub(r'\(.*?\)|\[.*?\]', '', title)
    clean_title = re.sub(r'(?i)\b(lirik|lyric|lyrics|official|video|music|audio|full|album)\b', '', clean_title)
    if "-" in clean_title:
        parts = clean_title.split("-")
        clean_title = parts[1] if len(parts) > 1 else parts[0]
    clean_title = clean_title.strip()
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

# ubah format lirik
"""format .lrc ([mm:ss.xx] teks) ke list [(timestamp_detik, teks_lirik)]."""
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

def format_time(seconds: float) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02d}:{s:02d}"

# ui audio
def render_simple_ui(lyrics_data: list[tuple[float, str]], current_index: int, song_title: str, elapsed: float, total: float) -> Text:
    ui_text = Text()
    ui_text.append(f"[🎶] Playing: {song_title}\n\n")
    start = max(0, current_index - 2)
    end = min(len(lyrics_data), current_index + 3)
    for i in range(start, end):
        _, line_text = lyrics_data[i]
        line = line_text if line_text else "🎵 ... 🎵"
        if i == current_index:
            ui_text.append(f"▶  {line}\n", style="bold #ff90d5 reverse")
        elif i < current_index:
            ui_text.append(f"   {line}\n", style="dim white")
        else:
            ui_text.append(f"   {line}\n", style="bold #ff00af")
    # Progress Bar
    pct = min(1.0, max(0.0, elapsed / total)) if total > 0 else 0.0
    bar_width = 30
    filled = int(bar_width * pct)
    bar_str = "━" * filled + ("╸🚣" if filled < bar_width else "") + "─" * max(0, bar_width - filled - 1)
    ui_text.append("\n")
    ui_text.append(f"[{format_time(elapsed)}] ", style="bold white")
    ui_text.append(f"▶ {bar_str} ", style="bold #6c6c6c")
    ui_text.append(f"[{format_time(total)}]\n", style="bold #ff70db")
    return ui_text

# animasi teks lirik
def start_lyrics_animation(song_title: str, artist: str = "", delay_offset: float = 4.8):
    console.print(f"[🔎] Mengunduh lirik untuk {song_title}...")
    lrc_raw = fetch_synced_lyrics(song_title, artist)
    if not lrc_raw:
        console.print(f"\n[[bold #e80000]![/bold #e80000]] Lirik tidak ditemukan untuk: {song_title}\n")
        return
    lyrics_data = parse_lrc(lrc_raw)
    if not lyrics_data:
        console.print("\n[[bold #e80000]![/bold #e80000]] Format lirik tidak dapat diproses.\n")
        return
    total_duration = lyrics_data[-1][0] + 10.0 if lyrics_data else 180.0
    start_time = time.time()
    current_idx = 0
    try:
        with Live(render_simple_ui(lyrics_data, current_idx, song_title, 0.0, total_duration), refresh_per_second=10, console=console) as live:
            while current_idx < len(lyrics_data):
                elapsed_time = (time.time() - start_time) - delay_offset
                target_idx = 0
                for i, (timestamp, _) in enumerate(lyrics_data):
                    if elapsed_time >= timestamp:
                        target_idx = i
                    else:
                        break
                # Update UI hanya ketika indeks berubah atau timer progress bar berjalan
                current_idx = target_idx
                live.update(render_simple_ui(lyrics_data, current_idx, song_title, max(0.0, elapsed_time), total_duration))
                time.sleep(0.05)
    except KeyboardInterrupt:
        console.print("\n[#ff70db][!] Lirik dihentikan.[/#ff70db]")

