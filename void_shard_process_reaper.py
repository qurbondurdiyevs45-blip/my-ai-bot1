import os
import time
import psutil
import random
import curses
from datetime import datetime

# Void Shard Process Reaper
# A stylized CLI utility to monitor system entropy and 'reap' excessive memory usage
# with a cinematic, data-heavy dashboard interface.

class VoidShards:
    def __init__(self):
        self.shards = []
        self.threshold = 85.0  # CPU warning threshold
        self.max_history = 50

    def get_system_stats(self):
        stats = {
            'cpu': psutil.cpu_percent(interval=None),
            'ram': psutil.virtual_memory().percent,
            'procs': len(psutil.pids()),
            'net': psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        }
        return stats

    def get_top_processes(self, limit=10):
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                procs.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(procs, key=lambda x: x['memory_percent'], reverse=True)[:limit]

    def draw_dashboard(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(1000)
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

        while True:
            stdscr.erase()
            h, w = stdscr.getmaxyx()
            
            stats = self.get_system_stats()
            procs = self.get_top_processes(h - 15)

            # Frame
            stdscr.attron(curses.color_pair(2))
            stdscr.border()
            stdscr.attroff(curses.color_pair(2))

            # Header
            title = " ⚡ VOID SHARD PROCESS REAPER v1.0.4 ⚡ "
            stdscr.addstr(0, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))

            # System Load Bars
            stdscr.addstr(2, 4, f"SYSTEM ENTROPY: {stats['cpu']}% ", curses.color_pair(1))
            bar_len = int((stats['cpu'] / 100) * (w - 25))
            stdscr.addstr(2, 20, "[" + "#" * bar_len + " " * (w - 26 - bar_len) + "]")

            stdscr.addstr(3, 4, f"MEMORY FLUX:    {stats['ram']}% ", curses.color_pair(2))
            ram_bar = int((stats['ram'] / 100) * (w - 25))
            stdscr.addstr(3, 20, "[" + "=" * ram_bar + " " * (w - 26 - ram_bar) + "]")

            # Process Table Header
            stdscr.addstr(6, 4, f"{'PID':<8} {'NAME':<25} {'MEM%':<10} {'CPU%':<10} {'STATUS':<10}", curses.A_UNDERLINE)
            
            # Process List
            for i, p in enumerate(procs):
                if i + 8 >= h - 4: break
                color = curses.color_pair(4) if p['cpu_percent'] < 50 else curses.color_pair(3)
                row_str = f"{p['pid']:<8} {str(p['name'])[:24]:<25} {p['memory_percent']:>5.2f}%    {p['cpu_percent']:>5.2f}%    STABLE"
                stdscr.addstr(7 + i, 4, row_str, color)

            # Decorative Shard Visualization
            shard_chars = ['◢', '◣', '◤', '◥', '⬥', '⬦']
            footer_y = h - 3
            for _ in range(15):
                rx, ry = random.randint(2, w-3), random.randint(footer_y - 2, footer_y)
                stdscr.addstr(ry, rx, random.choice(shard_chars), curses.color_pair(random.randint(1, 2)))

            stdscr.addstr(h - 2, 4, f"| Uptime: {datetime.now().strftime('%H:%M:%S')} | Press 'q' to collapse the void | Active PIDs: {stats['procs']} |", curses.color_pair(1))
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == ord('q'):
                break

def main():
    engine = VoidShards()
    try:
        curses.wrapper(engine.draw_dashboard)
    except KeyboardInterrupt:
        pass
    print("\n[!] Void Shard Disconnected. Systems stabilizing...")

if __name__ == "__main__":
    main()