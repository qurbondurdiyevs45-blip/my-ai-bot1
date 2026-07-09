import time
import random
import math
import os
from dataclasses import dataclass
from typing import List

# --- A Terminal-based Algorithmic Groove Generator ---
# This script generates a dynamic, evolving rhythmic pattern in the terminal
# and maps it to frequency values. While it doesn't output real-time audio 
# (to maintain cross-platform zero-dependency scripts), it provides a 
# visual-logic framework for a generative MIDI/OSC sequencer.

@dataclass
class Step:
    velocity: int
    note: str
    is_active: bool
    probability: float

class NeuralSequencer:
    def __init__(self, steps: int = 16):
        self.steps = steps
        self.grid = self._initialize_grid()
        self.bpm = 120
        self.iteration = 0
        self.scale = ["C3", "Eb3", "F3", "G3", "Bb3", "C4"]
        self.glitch_threshold = 0.05

    def _initialize_grid(self) -> List[Step]:
        return [Step(
            velocity=random.randint(60, 110),
            note=random.choice(["C3", "Eb3", "G3"]),
            is_active=random.random() > 0.7,
            probability=random.uniform(0.5, 0.9)
        ) for _ in range(self.steps)]

    def evolve_pattern(self):
        """Mutates the sequence over time using pseudo-neural weights."""
        for i, step in enumerate(self.grid):
            # Higher probability items are more stable
            if random.random() < (1.0 - step.probability) * 0.2:
                step.is_active = not step.is_active
            
            # Randomly shift notes within the scale
            if random.random() < 0.05:
                step.note = random.choice(self.scale)
            
            # Modify velocity with a sine wave drift
            step.velocity = int(80 + 30 * math.sin(self.iteration * 0.1 + i))

    def get_visual_bar(self, step: Step, is_current: bool) -> str:
        if not step.is_active:
            char = "·"
            color = "\033[90m"  # Dark Grey
        else:
            char = "■"
            color = "\033[92m" if not is_current else "\033[97m" # Green or White
        
        if is_current:
            return f"\033[1m[{color}{char}\033[0m\033[1m]"
        return f" {color}{char}\033[0m "

    def run(self, loops: int = 100):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\033[1m--- NEURAL DRIFT SEQUENCER ---\033[0m")
            print("Logic: Stochastic Rhythmic Evolution\n")

            for _ in range(loops):
                current_step_idx = self.iteration % self.steps
                
                # Evolution cycle every measure
                if current_step_idx == 0:
                    self.evolve_pattern()

                # Build Display String
                display = "  "
                for i, step in enumerate(self.grid):
                    display += self.get_visual_bar(step, i == current_step_idx)

                # Simulation of "Audio Engine" parameters
                current = self.grid[current_step_idx]
                status = f" FREQ: {current.note if current.is_active else '---'} | VEL: {current.velocity if current.is_active else '000'}"
                
                # Print UI to terminal (Carriage Return for overwrite)
                print(f"\r{display} | {status}", end="", flush=True)
                
                time.sleep(60 / (self.bpm * 4)) # 16th notes
                self.iteration += 1

        except KeyboardInterrupt:
            print("\n\n\033[93mSequence Halted by User.\033[0m")

if __name__ == "__main__":
    # Initialize the utility
    engine = NeuralSequencer(steps=16)
    
    # Inject a specific seed for predictable creativity (optional)
    # random.seed(42)
    
    # Start the execution loop
    engine.run()
