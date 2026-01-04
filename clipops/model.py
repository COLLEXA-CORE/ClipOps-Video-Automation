# clipops/model.py

import os
import re
import whisper
from deep_translator import GoogleTranslator
from .utils import seconds_to_vtt_fmt, run_ffmpeg_command

class ClipOpsModel:
    """
    Handles all business logic: Transcription, Translation, Media Processing.
    """

    def transcribe_video(self, video_path, log_callback):
        log_callback(f"🎧 Engine: Transcribing {os.path.basename(video_path)}...")
        try:
            model = whisper.load_model("base")
            result = model.transcribe(video_path)
            
            base_name = os.path.splitext(video_path)[0]
            output_file = f"{base_name}_transcript.txt"
            
            with open(output_file, "w", encoding="utf-8") as f:
                for segment in result["segments"]:
                    line = f"[{int(segment['start'])}s - {int(segment['end'])}s]: {segment['text']}\n"
                    f.write(line)
            
            log_callback(f"✅ Saved: {os.path.basename(output_file)}")
            return True
        except Exception as e:
            log_callback(f"❌ Error: {e}")
            return False

    def translate_text(self, txt_file, target_lang, log_callback, progress_callback):
        if not txt_file or not os.path.exists(txt_file):
            log_callback("⚠️ File not found.")
            return False

        log_callback(f"🌍 Engine: Translating to '{target_lang}'...")
        translator = GoogleTranslator(source='auto', target=target_lang)
        output_file = txt_file.replace(".txt", f"_{target_lang}.txt")

        try:
            with open(txt_file, "r", encoding="utf-8") as infile:
                lines = infile.readlines()

            total = len(lines)
            with open(output_file, "w", encoding="utf-8") as outfile:
                for i, line in enumerate(lines):
                    match = re.match(r"(\[.*?\]):\s*(.*)", line)
                    if match and match.group(2).strip():
                        try:
                            tr = translator.translate(match.group(2))
                            outfile.write(f"{match.group(1)}: {tr}\n")
                        except Exception:
                            outfile.write(line)
                    else:
                        outfile.write(line)
                    
                    if progress_callback:
                        progress_callback((i + 1) / total)

            log_callback(f"✅ Translated: {os.path.basename(output_file)}")
            return True
        except Exception as e:
            log_callback(f"❌ Error: {e}")
            return False

    def convert_to_vtt(self, txt_file, log_callback, progress_callback):
        if not txt_file or not os.path.exists(txt_file):
            log_callback("⚠️ File not found.")
            return False

        output_vtt = txt_file.replace(".txt", ".vtt")
        log_callback("📜 Converting to VTT...")

        try:
            with open(txt_file, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            total = len(lines)
            with open(output_vtt, 'w', encoding='utf-8') as outfile:
                outfile.write("WEBVTT\n\n")
                for i, line in enumerate(lines):
                    match = re.search(r'\[(\d+)s\s*-\s*(\d+)s\]:\s*(.*)', line)
                    if match:
                        start = seconds_to_vtt_fmt(match.group(1))
                        end = seconds_to_vtt_fmt(match.group(2))
                        text = match.group(3).strip()
                        outfile.write(f"{start} --> {end}\n{text}\n\n")
                    
                    if progress_callback:
                        progress_callback((i + 1) / total)
            
            log_callback(f"✅ VTT Ready: {os.path.basename(output_vtt)}")
            return True
        except Exception as e:
            log_callback(f"❌ Error: {e}")
            return False

    def slice_whatsapp(self, video_path, log_callback):
        log_callback("📱 Engine: Slicing 3-min chunks...")
        base = os.path.splitext(os.path.basename(video_path))[0]
        folder = os.path.join(os.path.dirname(video_path), f"WhatsApp_{base}")
        
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        pat = os.path.join(folder, f"{base}_part%03d.mp4")
        cmd = [
            "ffmpeg", "-y", "-i", video_path, "-c", "copy", "-map", "0",
            "-f", "segment", "-segment_time", "180", "-reset_timestamps", "1", pat
        ]
        
        success = run_ffmpeg_command(cmd, log_callback)
        if success:
            log_callback(f"📂 Check folder: /WhatsApp_{base}")
        return success

    def slice_topics(self, video_path, raw_text, log_callback):
        log_callback("✂️ Engine: Processing topics...")
        topics = []
        for line in raw_text.strip().split('\n'):
            if not line.strip(): continue
            # Matches: 00:00 - 05:00 : Title
            match = re.search(r"(\d+:?\d*:?\d*)\s*[-to\s]+\s*(\d+:?\d*:?\d*)\s*[:|-]?\s*(.*)", line)
            if match:
                topics.append({
                    "start": match.group(1),
                    "end": match.group(2),
                    "title": match.group(3).strip().replace(" ", "_").replace("/", "-")
                })

        if not topics:
            log_callback("❌ No valid topics found.")
            return False

        base = os.path.splitext(os.path.basename(video_path))[0]
        folder = os.path.join(os.path.dirname(video_path), f"Topics_{base}")
        if not os.path.exists(folder): os.makedirs(folder)

        for idx, t in enumerate(topics):
            fname = f"{idx+1:02d}_{t['title']}.mp4"
            out_path = os.path.join(folder, fname)
            log_callback(f"⚡ Cutting: {t['title']}...")
            
            cmd = ["ffmpeg", "-y", "-i", video_path, "-ss", t['start'], "-to", t['end'], "-c", "copy", out_path]
            run_ffmpeg_command(cmd, log_callback)
        
        log_callback("🎉 All topics exported!")
        return True

    def manual_cut(self, video_path, start, end, log_callback):
        log_callback(f"✂️ Cutting {start} to {end}...")
        output = os.path.splitext(video_path)[0] + "_cut.mp4"
        cmd = ["ffmpeg", "-y", "-i", video_path, "-ss", start, "-to", end, "-c", "copy", output]
        return run_ffmpeg_command(cmd, log_callback)