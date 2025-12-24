import importlib
import json
import os
import signal
import sys
from dataclasses import dataclass
from typing import List, Tuple

from PyQt6.QtCore import pyqtSignal, Qt, QThread, QTimer, QFileSystemWatcher
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from constants import NUM_LIGHTS, TIME_LIMIT
from mocks import MockNeoPixel, MockPin
import pattern_definition

# Constants
DATA_PIN = MockPin.D18


@dataclass
class LED:
    x: float
    y: float
    color: Tuple[int, int, int] = (0, 0, 0)


class LEDCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.leds: List[LED] = []
        self.led_size = 15
        self.padding = 50
        self.setMinimumSize(800, 600)
        self.show_numbers = True

    def set_leds(self, leds: List[LED]):
        self.leds = leds
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fill background
        painter.fillRect(self.rect(), Qt.GlobalColor.black)

        # Calculate usable area
        usable_width = self.width() - 2 * self.padding
        usable_height = self.height() - 2 * self.padding

        for i, led in enumerate(self.leds):
            if led.x < 0 or led.y < 0:
                continue

            # Scale coordinates to usable area and add padding
            x = int(self.padding + led.x * usable_width)
            y = int(self.padding + led.y * usable_height)

            # Draw LED glow (larger, semi-transparent circle)
            r, g, b = led.color
            glow_color = QColor(r, g, b, 50)  # Semi-transparent
            glow_size = self.led_size * 2
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow_color)
            painter.drawEllipse(
                x - glow_size // 2, y - glow_size // 2, glow_size, glow_size
            )

            # Draw LED
            painter.setPen(QPen(QColor(r, g, b), 1))
            painter.setBrush(QColor(r, g, b))
            painter.drawEllipse(
                x - self.led_size // 2,
                y - self.led_size // 2,
                self.led_size,
                self.led_size,
            )

            # Draw LED number
            if self.show_numbers:
                painter.setPen(QPen(Qt.GlobalColor.white, 1))
                painter.drawText(x + self.led_size, y, str(i))


class PatternWorker(QThread):
    """Worker thread for running LED patterns"""

    def __init__(self, pattern_func, pixels, time_limit):
        super().__init__()
        self.pattern_func = pattern_func
        self.pixels = pixels
        self.time_limit = time_limit
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True

    def run(self):
        try:
            import inspect

            sig = inspect.signature(self.pattern_func)
            params = sig.parameters

            if "pixels" in params:
                self.pattern_func(self.time_limit, pixels=self.pixels)
            else:
                self.pattern_func(self.time_limit)
        except Exception as e:
            print(f"Pattern thread error: {e}")


class LEDSimulator(QMainWindow):
    update_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED Pattern Simulator")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Add control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # Pattern selector dropdown
        self.pattern_selector = QComboBox()
        self.load_patterns()
        self.pattern_selector.currentTextChanged.connect(self.change_pattern)
        control_layout.addWidget(QLabel("Pattern:"))
        control_layout.addWidget(self.pattern_selector)

        # LED size slider
        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setMinimum(5)
        size_slider.setMaximum(30)
        size_slider.setValue(15)
        size_slider.valueChanged.connect(self.change_led_size)
        control_layout.addWidget(QLabel("LED Size:"))
        control_layout.addWidget(size_slider)

        # Toggle numbers button
        toggle_numbers = QPushButton("Toggle Numbers")
        toggle_numbers.clicked.connect(self.toggle_led_numbers)
        control_layout.addWidget(toggle_numbers)

        layout.addWidget(control_panel)

        # Add canvas (existing code)
        self.canvas = LEDCanvas()
        layout.addWidget(self.canvas)

        self.positions = self._load_positions()
        self.canvas.set_leds(self.positions)

        self.pixels = MockNeoPixel(DATA_PIN, NUM_LIGHTS)
        self.pixels._callback = self._update_leds

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.process_updates)
        self.update_timer.start(16)  # ~60 FPS

        self.pending_updates = []
        self.update_signal.connect(self._queue_update)

        self.pattern_thread = None

        # Set up file system watcher for hot reloading
        self.file_watcher = QFileSystemWatcher()

        # Watch individual Python files in patterns and challenges directories
        import glob

        pattern_files = glob.glob("patterns/*.py") + glob.glob("challenges/*.py")
        for file_path in pattern_files:
            self.file_watcher.addPath(file_path)
            print(f"Watching file: {file_path}")

        self.file_watcher.fileChanged.connect(self.on_pattern_file_changed)

        self.show()

        # Start the first pattern automatically after the window is shown
        if self.available_patterns:
            first_pattern = list(self.available_patterns.keys())[0]
            self.change_pattern(first_pattern)

    def load_patterns(self):
        """Load all pattern functions from the PATTERNS dictionary"""
        self.available_patterns = {}

        if not pattern_definition.PATTERNS:
            print("No patterns defined in the PATTERNS dictionary.")
            raise ValueError("PATTERNS dictionary is empty.")

        for func_name, func in pattern_definition.PATTERNS.items():
            self.available_patterns[func_name] = func
            self.pattern_selector.addItem(func_name)

        if not self.available_patterns:
            print("No valid patterns were loaded.")
            raise ValueError("No valid patterns available.")

    def change_pattern(self, pattern_name):
        """Change to selected pattern"""
        print(f"Changing to pattern: {pattern_name}")

        # Stop current pattern if running
        if self.pattern_thread and self.pattern_thread.isRunning():
            self.pattern_thread.stop()
            # Use shorter timeout and terminate immediately if needed
            if not self.pattern_thread.wait(50):  # Reduced from 1000ms to 50ms
                self.pattern_thread.terminate()
                self.pattern_thread.wait(10)  # Very short wait after terminate

        # Clear any remaining updates
        self.pending_updates.clear()

        # Force cleanup of pixels
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

        # Start new pattern immediately
        if pattern_name in self.available_patterns:
            pattern_func = self.available_patterns[pattern_name]
            self.run_pattern(pattern_func)

    def _queue_update(self, pixels):
        """Queue updates instead of processing immediately"""
        # Convert GRB back to RGB for display
        rgb_pixels = [(color[1], color[0], color[2]) for color in pixels]
        self.pending_updates.append(rgb_pixels)

    def process_updates(self):
        """Process queued updates at a controlled rate"""
        if self.pending_updates:
            pixels = self.pending_updates[-1]  # Get most recent update
            self.pending_updates.clear()
            self._update_display(pixels)

    def run_pattern(self, pattern_func, time_limit=TIME_LIMIT):
        """Run pattern in QThread"""
        # Stop existing pattern if running
        if self.pattern_thread and self.pattern_thread.isRunning():
            self.pattern_thread.stop()
            self.pattern_thread.wait()

        # Create and start new pattern thread
        self.pattern_thread = PatternWorker(pattern_func, self.pixels, time_limit)
        self.pattern_thread.start()

    def _load_positions(self) -> List[LED]:
        try:
            with open("corrected_led_mapping.json", "r") as f:
                mapping = json.load(f)
        except FileNotFoundError:
            print(
                "Warning: corrected_led_mapping.json not found. Using default positions."
            )
            return [LED(x=-1, y=-1) for _ in range(NUM_LIGHTS)]
        except json.JSONDecodeError:
            print(
                "Warning: Invalid JSON in corrected_led_mapping.json. Using default positions."
            )
            return [LED(x=-1, y=-1) for _ in range(NUM_LIGHTS)]

        leds = []
        for i in range(NUM_LIGHTS):
            if str(i) in mapping:
                x, y = mapping[str(i)]
                leds.append(LED(x=x, y=y))
            else:
                leds.append(LED(x=-1, y=-1))

        return leds

    def _update_leds(self, pixels):
        self.update_signal.emit(pixels)

    def _update_display(self, pixels):
        for idx, color in enumerate(pixels):
            if idx < len(self.positions):
                self.positions[idx].color = color
        self.canvas.set_leds(self.positions)

    def toggle_led_numbers(self):
        self.canvas.show_numbers = not self.canvas.show_numbers
        self.canvas.update()

    def change_led_size(self, size):
        self.canvas.led_size = size
        self.canvas.update()

    def on_pattern_file_changed(self, file_path):
        """Handle pattern file changes for hot reloading"""
        print(f"File changed: {file_path}")  # Debug output
        try:
            if not os.path.basename(file_path).endswith(".py"):
                print(f"Ignoring non-Python file: {file_path}")
                return

            # Determine the module path for the changed file
            if file_path.startswith("patterns/"):
                module_name = (
                    f"patterns.{os.path.splitext(os.path.basename(file_path))[0]}"
                )
            elif file_path.startswith("challenges/"):
                module_name = (
                    f"challenges.{os.path.splitext(os.path.basename(file_path))[0]}"
                )
            else:
                return

            # Reload the specific module that changed
            print(f"Reloading module: {module_name}")
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)

            # Also reload pattern_definition to pick up any changes
            print("Reloading pattern_definition module...")
            importlib.reload(pattern_definition)

            # Update our local copy
            self.available_patterns = pattern_definition.PATTERNS.copy()

            print(f"Reloaded patterns due to change in: {file_path}")
            print(f"Available patterns: {list(self.available_patterns.keys())}")

            # If the current pattern still exists, restart it with the new version
            current_pattern = self.pattern_selector.currentText()
            print(f"Current pattern: {current_pattern}")
            if current_pattern in self.available_patterns:
                print(f"Restarting current pattern: {current_pattern}")
                self.change_pattern(current_pattern)
            else:
                # If current pattern was removed, switch to first available
                if self.available_patterns:
                    first_pattern = list(self.available_patterns.keys())[0]
                    print(f"Switching to first available pattern: {first_pattern}")
                    self.pattern_selector.setCurrentText(first_pattern)
                    self.change_pattern(first_pattern)

        except Exception as e:
            print(f"Error reloading patterns: {e}")
            import traceback

            traceback.print_exc()

    def closeEvent(self, event):
        """Clean up pattern thread when window is closed"""
        if self.pattern_thread and self.pattern_thread.isRunning():
            self.pattern_thread.stop()
            if not self.pattern_thread.wait(50):  # Reduced timeout
                self.pattern_thread.terminate()
                self.pattern_thread.wait(10)  # Brief wait after terminate
        event.accept()


def main():
    app = QApplication(sys.argv)
    simulator = LEDSimulator()

    # Handle SIGINT (Ctrl+C) gracefully
    def signal_handler(signum, frame):
        app.quit()

    signal.signal(signal.SIGINT, signal_handler)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
