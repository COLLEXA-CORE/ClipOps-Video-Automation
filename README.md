# 🎬 ClipOps - Video Automation Suite

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Powered By](https://img.shields.io/badge/Powered%20by-COLLEXA-orange)

**ClipOps** is a modern, desktop-based video automation tool designed for content creators and engineers. It utilizes **OpenAI Whisper** for transcription and **FFmpeg** for precise video slicing, wrapped in a clean **MVC (Model-View-Controller)** architecture using `CustomTkinter`.

---

## 🚀 Features

* **🧠 AI Transcription:** Converts video speech to text using OpenAI Whisper locally.
* **🌍 Auto-Translation:** Translates transcripts between English and Arabic instantly.
* **📜 VTT Generator:** Converts text files into standard `.vtt` subtitles.
* **✂️ Smart Slicing:**
    * **WhatsApp Mode:** Auto-splits videos into 3-minute chunks.
    * **Topic Mode:** Slices video based on specific timestamps and titles.
    * **Manual Mode:** Precise cutting with start/end times.
* **🎨 Modern UI:** Dark/Light mode support with a responsive design.
* **🏗️ MVC Architecture:** Clean code structure following PEP 8 standards.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI:** CustomTkinter (Modern Tkinter wrapper)
* **Core Engine:** FFmpeg (Multimedia processing)
* **AI Model:** OpenAI Whisper (Speech-to-Text)
* **Pattern:** Model-View-Controller (MVC)

---

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YourUsername/ClipOps-Video-Automation.git](https://github.com/YourUsername/ClipOps-Video-Automation.git)
    cd ClipOps-Video-Automation
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install FFmpeg**
    * Ensure `ffmpeg` is installed and added to your system PATH.
    * [Download FFmpeg Here](https://ffmpeg.org/download.html)

---

## ▶️ Usage

Run the main entry point:

```bash
python main.py