# clipops/utils.py

import os
import subprocess
import sys

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
    """
    نسخة ذكية تحدد مسار FFmpeg سواء في وضع التطوير أو الـ EXE
    """
    # 1. تحديد المسار الأساسي (Base Path)
    if getattr(sys, 'frozen', False):
        # لو البرنامج شغال كـ EXE، المسار هو مكان ملف الـ EXE
        base_path = os.path.dirname(sys.executable)
    else:
        # لو البرنامج شغال كـ Python Script، المسار هو مكان الملف الحالي
        base_path = os.getcwd()
    
    # 2. تحديد مسار ffmpeg.exe المتوقع بجانب البرنامج
    local_ffmpeg = os.path.join(base_path, "ffmpeg.exe")
    
    # 3. تعديل الأمر لاستخدام الملف المحلي لو موجود
    if os.path.exists(local_ffmpeg):
        cmd[0] = local_ffmpeg
        # log_callback(f"🔧 Using bundled FFmpeg: {local_ffmpeg}") # (اختياري للتبع)
    else:
        # لو مش موجود، حاول تعتمد على الـ System Path (بس ده خطر في الـ exe)
        cmd[0] = "ffmpeg"

    # 4. التنفيذ
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
            errors='replace',
            startupinfo=startupinfo
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            log_callback("✅ Operation Successful!")
            return True
        else:
            # عرض جزء من الخطأ للمستخدم
            err_msg = stderr[-200:] if stderr else "Unknown Error"
            log_callback(f"❌ FFmpeg Failed:\n{err_msg}")
            return False

    except FileNotFoundError:
        log_callback("❌ CRITICAL: 'ffmpeg.exe' missing!\nPlease put ffmpeg.exe in the same folder as this app.")
        return False
    except Exception as e:
        log_callback(f"❌ Error: {str(e)}")
        return False