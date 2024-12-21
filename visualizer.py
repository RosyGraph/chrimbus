import importlib
import inspect
import os
import sys
from unittest.mock import MagicMock


# Set up mocks before any other imports
class MockPin:
    D18 = "D18"


class MockNeoPixel:
    """Mock implementation of NeoPixel that works for both direct use and context manager"""

    _instance = None

    def __new__(cls, pin, num_lights, auto_write=False):
        if cls._instance is None:
            cls._instance = super(MockNeoPixel, cls).__new__(cls)
            cls._instance.num_lights = num_lights
            cls._instance.auto_write = auto_write
            cls._instance._pixels = [(0, 0, 0)] * num_lights
            cls._instance._callback = None
        return cls._instance

    def __init__(self, pin, num_lights, auto_write=False):
        # These values are kept for reference but not reset due to singleton pattern
        self.num_lights = num_lights
        self.auto_write = auto_write

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fill((0, 0, 0))
        self.show()

    def __len__(self):
        return self.num_lights

    def __setitem__(self, idx, color):
        if isinstance(idx, slice):
            start = idx.start if idx.start is not None else 0
            stop = idx.stop if idx.stop is not None else len(self)
            step = idx.step if idx.step is not None else 1

            if isinstance(color, list):
                for i, pos in enumerate(range(start, stop, step)):
                    if pos < len(self):
                        if len(color[min(i, len(color) - 1)]) == 3:
                            c = color[min(i, len(color) - 1)]
                            self._pixels[pos] = (c[0], c[1], c[2])
            else:
                for pos in range(start, stop, step):
                    if pos < len(self):
                        if len(color) == 3:
                            self._pixels[pos] = (color[0], color[1], color[2])
        else:
            if len(color) == 3:
                self._pixels[idx] = (color[0], color[1], color[2])

        if self.auto_write:
            self.show()

    def show(self):
        print("Show called, pixels:", self._pixels)  # Debug print
        if self._callback:
            self._callback(self._pixels)

    def fill(self, color):
        print(f"Fill called with color: {color}")  # Debug print
        if len(color) == 3:
            color = (color[0], color[1], color[2])  # Convert RGB to GRB
        self._pixels = [color] * self.num_lights
        if self.auto_write:
            self.show()


class MockNeoPixelModule:
    def NeoPixel(self, pin, num_lights, auto_write=False):
        return MockNeoPixel(pin, num_lights, auto_write)


# Create mock objects and patch modules
mock_board = MagicMock()
mock_board.D18 = MockPin.D18
sys.modules["board"] = mock_board

mock_neopixel = MockNeoPixelModule()
sys.modules["neopixel"] = mock_neopixel

# Now import the rest
import json
from dataclasses import dataclass
from typing import List, Tuple

from PyQt6.QtCore import pyqtSignal, Qt, QThread, QTimer
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
        print(
            f"Setting LEDs: {[led.color for led in leds[:5]]}"
        )  # Debug print first 5 LEDs
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
            print(f"LED {i} color: {led.color}")  # Debug print
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

        self.show()

    def load_patterns(self):
        """Load all pattern modules from the patterns directory"""
        patterns_dir = "patterns"
        self.available_patterns = {}

        try:
            # Get all Python files in the patterns directory
            pattern_files = [
                f[:-3]
                for f in os.listdir(patterns_dir)
                if f.endswith(".py") and f != "__init__.py"
            ]

            for pattern_file in pattern_files:
                try:
                    # Import the module
                    module = importlib.import_module(f"patterns.{pattern_file}")

                    # Find pattern functions in the module
                    pattern_funcs = inspect.getmembers(
                        module,
                        lambda m: inspect.isfunction(m)
                        and not m.__name__.startswith("_"),
                    )

                    for func_name, func in pattern_funcs:
                        self.available_patterns[func_name] = func
                        self.pattern_selector.addItem(func_name)

                except ImportError as e:
                    print(f"Error importing {pattern_file}: {e}")

        except FileNotFoundError:
            print("Patterns directory not found")

        if not self.available_patterns:
            # Add mono_rainbow as fallback
            from patterns.mono_rainbow import mono_rainbow

            self.available_patterns["mono_rainbow"] = mono_rainbow
            self.pattern_selector.addItem("mono_rainbow")

    def change_pattern(self, pattern_name):
        """Change to selected pattern"""
        print(f"Changing to pattern: {pattern_name}")

        # Stop current pattern if running
        if self.pattern_thread and self.pattern_thread.isRunning():
            print("Stopping current pattern...")
            self.pattern_thread.stop()

            # Wait with timeout
            if not self.pattern_thread.wait(1000):  # 1 second timeout
                print("Pattern thread didn't stop gracefully, forcing termination...")
                self.pattern_thread.terminate()
                self.pattern_thread.wait()

            print("Previous pattern stopped")

        # Clear any remaining updates
        self.pending_updates.clear()

        # Force cleanup of pixels
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

        # Add small delay to allow GUI to update
        QTimer.singleShot(100, lambda: self._start_new_pattern(pattern_name))

    def _start_new_pattern(self, pattern_name):
        """Helper to start new pattern after delay"""
        print(f"Starting new pattern: {pattern_name}")
        if pattern_name in self.available_patterns:
            pattern_func = self.available_patterns[pattern_name]
            self.run_pattern(pattern_func)

    def _queue_update(self, pixels):
        """Queue updates instead of processing immediately"""
        print(
            f"Queueing update with pixels: {pixels[:5]}"
        )  # Debug print first 5 pixels
        # Convert GRB back to RGB for display
        rgb_pixels = [(color[1], color[0], color[2]) for color in pixels]
        print(f"After conversion: {rgb_pixels[:5]}")  # Debug print
        self.pending_updates.append(rgb_pixels)

    def process_updates(self):
        """Process queued updates at a controlled rate"""
        if self.pending_updates:
            pixels = self.pending_updates[-1]  # Get most recent update
            print(f"Processing update with pixels: {pixels[:5]}")  # Debug print
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
        print(f"Update LEDs called with pixels: {pixels[:5]}")  # Debug print
        self.update_signal.emit(pixels)

    def _update_display(self, pixels):
        print(f"Updating display with pixels: {pixels[:5]}")  # Debug print
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


def main():
    app = QApplication(sys.argv)
    simulator = LEDSimulator()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
