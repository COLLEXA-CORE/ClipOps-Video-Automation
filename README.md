# 🎬 ClipOps - Video Automation Suite

![Version](https://img.shields.io/badge/version-v1.5.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Powered By](https://img.shields.io/badge/Powered%20by-COLLEXA-orange)

**ClipOps** is a professional, all-in-one video automation tool designed for content creators and network engineers. Built with a robust **MVC architecture** and a modern **CustomTkinter** UI, it leverages **OpenAI Whisper** and **FFmpeg** to streamline video processing workflows.

---

## 🚀 Key Features

### ⚡ Auto Ops (One-Click Automation)
* **🎙️ AI Transcription:** Converts video speech to text locally using OpenAI Whisper (No internet required for the engine).
* **📱 WhatsApp Slicer:** Automatically splits long videos into **3-minute chunks** perfect for WhatsApp Status or Telegram.

### 📄 Text Ops (Subtitle Management)
* **🌍 Auto-Translation:** Translates generated transcripts between **English** and **Arabic**.
* **📜 VTT Conversion:** Converts standard text transcripts into web-ready `.vtt` subtitle files.

### ✂️ Smart Cutter (Topic Slicing)
* **intelligent Splitting:** Paste a list of timestamps and titles, and ClipOps will export individual video clips for each topic automatically.
    * *Format:* `00:00 - 05:00 : Topic_Title`

### 🔧 Precision & UI
* **Manual Cut:** Extract specific clips with millisecond precision.
* **Modern UI:** Dark/Light mode toggle, fullscreen support, and real-time progress bars.
* **Portable:** Runs as a standalone `.exe` (requires FFmpeg).

---

## 🛠️ Installation & Setup

### Option A: Running from Source (For Developers)

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YourUsername/ClipOps.git](https://github.com/YourUsername/ClipOps.git)
    cd ClipOps
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Requirements: `customtkinter`, `openai-whisper`, `deep-translator`, `pillow`)*

3.  **FFmpeg Setup**
    * Download `ffmpeg.exe` and place it in the project root folder.
    * [Download FFmpeg Essentials](https://www.gyan.dev/ffmpeg/builds/)

4.  **Run the App**
    ```bash
    python main.py
    ```

### Option B: Running the Portable App (.exe)
1.  Download the latest release.
2.  Ensure `ffmpeg.exe` is in the same folder as `ClipOps.exe`.
3.  Run `ClipOps.exe`.

---

## 📖 User Guide

### 1. The Interface
* **Dark/Light Mode:** Toggle the theme using the switch in the top-right header.
* **Fullscreen:** Use the `⛶ Fullscreen` button for a focused workspace.
* **Logs:** The bottom console shows real-time status, errors, and success messages.

### 2. How to Use "Auto Ops"
1.  Click **"Import Video 🎬"** to select your source file (`.mp4`, `.mkv`).
2.  **Transcribe:** Click to generate a time-stamped `.txt` file of the audio.
3.  **WhatsApp Slicer:** Click to automatically create a folder with 3-minute video parts.

### 3. How to Use "Text Ops"
1.  Go to the **📄 Text Ops** tab.
2.  Click **"Browse .txt"** (select the transcript generated from step 2).
3.  Select Target Language (e.g., `en` or `ar`).
4.  Click **Translate** or **Convert to VTT**.

### 4. How to Use "Topic Slice" (The Power Feature)
1.  Import your video.
2.  Go to **✂️ Topic Slice**.
3.  Paste your topic list in this format:
    ```text
    00:00 - 04:30 : Introduction
    04:31 - 12:00 : Network_Layers
    12:01 - 15:00 : Summary
    ```
4.  Click **SLICE TOPICS**. The app will generate a folder with named video clips.

---

## 🏗️ Architecture (MVC)

The project follows a strict **Model-View-Controller** pattern for scalability:

* **`model.py`**: Handles FFmpeg commands, Whisper AI logic, and file processing.
* **`view.py`**: Manages the CustomTkinter GUI layout and widgets.
* **`controller.py`**: Connects user actions to logic and manages threading.
* **`utils.py`**: Helper functions (Icon generation, Time formatting).

---

## 📜 License & Attribution

This project is licensed under the **MIT License**.

> **Powered by COLLEXA**
> If you use this code or software, please retain the copyright notice and attribution to **COLLEXA**.

Copyright (c) 2026 **COLLEXA**.