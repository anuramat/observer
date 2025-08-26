"""Screenshot capture functionality."""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import tuple

import i3ipc
from PIL import Image


class ScreenCapture:
    """Screenshot capture and window management."""
    
    def __init__(self, screenshot_dir: Path):
        self.screenshot_dir = screenshot_dir
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.i3 = i3ipc.Connection()
    
    def get_focused_window(self) -> dict:
        """Get focused window info and geometry."""
        tree = self.i3.get_tree()
        focused = tree.find_focused()
        
        return {
            'title': focused.name or 'Unknown',
            'class': focused.window_class or 'Unknown',
            'rect': {
                'x': focused.rect.x,
                'y': focused.rect.y,
                'width': focused.rect.width,
                'height': focused.rect.height
            }
        }
    
    def capture(self) -> tuple[Path, dict]:
        """Capture screenshot and return path + window info."""
        window = self.get_focused_window()
        rect = window['rect']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        screenshot_path = self.screenshot_dir / f"screenshot_{timestamp}.png"
        
        # Capture with grim
        rect_str = f"{rect['x']},{rect['y']} {rect['width']}x{rect['height']}"
        subprocess.run(['grim', '-g', rect_str, str(screenshot_path)], check=True)
        
        # Optimize for storage
        with Image.open(screenshot_path) as img:
            if img.width > 1920:
                img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                img.save(screenshot_path, optimize=True)
        
        return screenshot_path, window