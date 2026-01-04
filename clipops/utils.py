# clipops/utils.py

import os
import subprocess

def seconds_to_vtt_fmt(seconds):
    """Converts seconds to HH:MM:SS.000 format."""
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.000"

def ensure_icon_exists(icon_path):
    """Generates the app icon if it doesn't exist."""
    if not os.path.exists(icon_path):
        try:
            from PIL import Image, ImageDraw
            size = (256, 256)
            bg_color = (43, 43, 43)
            accent = (255, 87, 34)
            
            img = Image.new('RGB', size, bg_color)
            draw = ImageDraw.Draw(img)
            
            # Draw Circle
            draw.ellipse((20, 20, 236, 236), outline=accent, width=20)
            # Draw Play Triangle
            triangle = [(85, 70), (85, 186), (190, 128)]
            draw.polygon(triangle, fill=accent)
            
            img.save(icon_path, format='ICO', sizes=[(256, 256)])
        except ImportError:
            pass  # Pillow not installed
        except Exception:
            pass

def run_ffmpeg_command(cmd, log_callback):
    """Executes FFmpeg commands silently."""
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            encoding='utf-8', 
            startupinfo=startupinfo
        )
        process.wait()
        
        if process.returncode == 0:
            log_callback("✅ Operation Successful!")
            return True
        else:
            log_callback("❌ Operation Failed (Check Console)!")
            return False
    except Exception as e:
        log_callback(f"❌ Execution Error: {str(e)}")
        return False