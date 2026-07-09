import math
import time
import random
import os

class SpectralEntropyGenerator:
    """
    A command-line tool that generates cryptographically-inspired 
    visual patterns and entropy strings using mathematical oscillations.
    """

    BLOCKS = [' ', '░', '▒', '▓', '█']
    COLORS = [
        '\033[94m', # Blue
        '\033[96m', # Cyan
        '\033[92m', # Green
        '\033[93m', # Yellow
        '\033[91m', # Red
        '\033[95m'  # Magenta
    ]
    RESET = '\033[0m'

    def __init__(self, width=80, height=20):
        self.width = width
        self.height = height
        self.t = 0.0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def generate_point(self, x, y, t):
        """
        Calculates a density value based on interference patterns.
        """
        # Normalize coordinates
        nx = (x / self.width) * 2 - 1
        ny = (y / self.height) * 2 - 1

        # Complex wave interference formula
        v = math.sin(nx * 10 + t)
        v += math.sin((ny * 10 + t) * 0.5)
        v += math.sin((nx * 10 + ny * 10 + t) * 0.5)
        
        # Add a chaotic radial component
        r = math.sqrt(nx**2 + ny**2)
        v += math.sin(r * 20 - t * 2)
        
        # Normalize to 0.0 - 1.0
        return (v + 4) / 8

    def get_char(self, value):
        idx = int(value * (len(self.BLOCKS) - 1))
        return self.BLOCKS[max(0, min(idx, len(self.BLOCKS) - 1))]

    def get_color(self, value):
        idx = int(value * (len(self.COLORS) - 1))
        return self.COLORS[max(0, min(idx, len(self.COLORS) - 1))]

    def render_frame(self):
        frame = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                val = self.generate_point(x, y, self.t)
                char = self.get_char(val)
                color = self.get_color((val + self.t * 0.1) % 1.0)
                line += f"{color}{char}"
            frame.append(line + self.RESET)
        return "\n".join(frame)

    def generate_entropy_string(self, length=32):
        """Generates a pseudo-random hex string derived from the current state."""
        seed = str(time.time() + self.t).encode('utf-8')
        random.seed(seed)
        chars = "ABCDEF0123456789"
        return "".join(random.choice(chars) for _ in range(length))

    def run(self, cycles=50):
        print("\033[?25l")  # Hide cursor
        try:
            for _ in range(cycles):
                self.clear_screen()
                print(f"--- SPECTRAL ENTROPY FLOW [T={self.t:.2f}] ---")
                print(self.render_frame())
                print(f"\nEntropy Hash: {self.generate_entropy_string()}")
                print("Press Ctrl+C to stop.")
                
                self.t += 0.2
                time.sleep(0.05)
        except KeyboardInterrupt:
            pass
        finally:
            print("\033[?25h")  # Show cursor
            print("\nProcess Terminated.")

if __name__ == "__main__":
    # Attempt to detect terminal size, fallback to defaults
    try:
        columns, lines = os.get_terminal_size()
        gen = SpectralEntropyGenerator(width=columns, height=lines - 6)
    except:
        gen = SpectralEntropyGenerator()
    
    gen.run()