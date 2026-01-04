# clipops/view.py

import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from .config import APP_NAME, APP_VERSION, COMPANY_NAME, ACCENT_COLOR, ICON_FILE

class ClipOpsView(ctk.CTk):
    """
    The Main GUI Class.
    Follows PEP 8: Clean initialization and separated setup methods.
    """

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        self.title(f"{APP_NAME} {APP_VERSION} | Powered by {COMPANY_NAME}")
        self.geometry("950x850")
        self.minsize(900, 750)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        if os.path.exists(ICON_FILE):
            self.iconbitmap(ICON_FILE)

        self.is_fullscreen = False

    def _setup_ui(self):
        # 1. Header
        self._create_header()
        # 2. File Inputs
        self._create_file_inputs()
        # 3. Tabs
        self._create_tabs()
        # 4. Logs
        self._create_logs()

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, pady=(15, 5), sticky="ew", padx=25)
        
        # Brand
        brand_box = ctk.CTkFrame(header, fg_color="transparent")
        brand_box.pack(side="left")
        ctk.CTkLabel(brand_box, text=APP_NAME, font=("Impact", 32), text_color=ACCENT_COLOR).pack(anchor="w")
        ctk.CTkLabel(brand_box, text=f"Powered by {COMPANY_NAME}", font=("Roboto", 10, "bold"), text_color="gray").pack(anchor="w")

        # Controls
        self.switch_theme = ctk.CTkSwitch(header, text="Dark Mode", command=self._toggle_theme, onvalue="Dark", offvalue="Light")
        self.switch_theme.pack(side="right", padx=10)
        self.switch_theme.select()
        
        self.btn_fullscreen = ctk.CTkButton(header, text="⛶ Fullscreen", width=100, fg_color="transparent", 
                                            border_width=1, border_color="gray", command=self._toggle_fullscreen)
        self.btn_fullscreen.pack(side="right")

    def _create_file_inputs(self):
        self.frame_file = ctk.CTkFrame(self, fg_color=("gray85", "#2b2b2b"), corner_radius=10)
        self.frame_file.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        
        self.entry_video = ctk.CTkEntry(self.frame_file, placeholder_text="Select Source Video...", height=40, border_width=0)
        self.entry_video.pack(side="left", padx=15, pady=15, expand=True, fill="x")
        
        self.btn_browse_video = ctk.CTkButton(self.frame_file, text="Import Video 🎬", height=40, fg_color=ACCENT_COLOR)
        self.btn_browse_video.pack(side="right", padx=15)

    def _create_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=10, segmented_button_selected_color=ACCENT_COLOR)
        self.tabview.grid(row=2, column=0, padx=25, pady=10, sticky="ew")
        
        self.tab_auto = self.tabview.add("⚡ Auto Ops")
        self.tab_text = self.tabview.add("📄 Text Ops")
        self.tab_topics = self.tabview.add("✂️ Topic Slice")
        self.tab_manual = self.tabview.add("🔧 Precision")

        self._setup_auto_tab()
        self._setup_text_tab()
        self._setup_topic_tab()
        self._setup_manual_tab()

    def _setup_auto_tab(self):
        f = self.tab_auto
        f.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(f, text="Video Automation", font=("Roboto", 14, "bold"), text_color="gray").grid(row=0, column=0, columnspan=2, pady=10)
        
        self.btn_transcribe = ctk.CTkButton(f, text="🎙️ Transcribe Video", height=50, fg_color="#3F51B5")
        self.btn_transcribe.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_whatsapp = ctk.CTkButton(f, text="📱 WhatsApp Slicer", height=50, fg_color="#43A047")
        self.btn_whatsapp.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

    def _setup_text_tab(self):
        f = self.tab_text
        # Input
        frame_inp = ctk.CTkFrame(f, fg_color="transparent")
        frame_inp.pack(fill="x", pady=20, padx=20)
        self.entry_text = ctk.CTkEntry(frame_inp, placeholder_text="Select .txt transcript...")
        self.entry_text.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_browse_text = ctk.CTkButton(frame_inp, text="Browse .txt", width=100, fg_color="#607D8B")
        self.btn_browse_text.pack(side="right")
        
        # Actions
        frame_acts = ctk.CTkFrame(f, fg_color=("gray90", "#333"), corner_radius=10)
        frame_acts.pack(fill="x", padx=20, pady=10)
        
        inner = ctk.CTkFrame(frame_acts, fg_color="transparent")
        inner.pack(pady=10)
        
        self.combo_lang = ctk.CTkComboBox(inner, values=["en", "ar"], width=70)
        self.combo_lang.pack(side="left", padx=10)
        self.combo_lang.set("en")
        
        self.btn_translate = ctk.CTkButton(inner, text="Translate 🌍", width=150, fg_color="#009688")
        self.btn_translate.pack(side="left", padx=10)
        
        self.btn_vtt = ctk.CTkButton(inner, text="Convert to VTT 📜", width=150, fg_color="#E91E63")
        self.btn_vtt.pack(side="left", padx=10)

    def _setup_topic_tab(self):
        f = self.tab_topics
        # Toolbar
        tb = ctk.CTkFrame(f, fg_color="transparent")
        tb.pack(fill="x", pady=(10, 5))
        
        ctk.CTkButton(tb, text="Paste", width=60, command=self._paste_clipboard).pack(side="right", padx=5)
        ctk.CTkButton(tb, text="Clear", width=60, fg_color="#444", command=lambda: self.txt_topics.delete("0.0", "end")).pack(side="right", padx=5)
        
        self.txt_topics = ctk.CTkTextbox(f, height=120, font=("Consolas", 12))
        self.txt_topics.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_topics.insert("0.0", "00:00 - 10:00 : Part_1\n10:01 - 20:00 : Part_2")
        
        self.btn_topic_slice = ctk.CTkButton(f, text="SLICE TOPICS ✂️", fg_color=ACCENT_COLOR, height=40)
        self.btn_topic_slice.pack(pady=10, fill="x", padx=100)

    def _setup_manual_tab(self):
        f = self.tab_manual
        cbox = ctk.CTkFrame(f, fg_color="transparent")
        cbox.pack(expand=True)
        rt = ctk.CTkFrame(cbox, fg_color="transparent")
        rt.pack()
        self.entry_man_start = ctk.CTkEntry(rt, placeholder_text="00:00:00", width=100)
        self.entry_man_start.pack(side="left", padx=5)
        self.entry_man_end = ctk.CTkEntry(rt, placeholder_text="00:05:00", width=100)
        self.entry_man_end.pack(side="left", padx=5)
        
        self.btn_manual_cut = ctk.CTkButton(cbox, text="Export Clip", width=150, fg_color="#607D8B")
        self.btn_manual_cut.pack(pady=20)

    def _create_logs(self):
        self.log_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.log_frame.grid(row=3, column=0, padx=25, pady=(10, 25), sticky="nsew")
        
        ctk.CTkLabel(self.log_frame, text="SYSTEM LOGS", font=("Roboto", 10, "bold"), text_color="gray").pack(anchor="w", padx=5)
        self.textbox_log = ctk.CTkTextbox(self.log_frame, corner_radius=8, font=("Consolas", 12))
        self.textbox_log.pack(fill="both", expand=True, pady=(0, 10))
        self.textbox_log.configure(state="disabled")

        self.lbl_status = ctk.CTkLabel(self.log_frame, text="Ready", font=("Roboto", 12), text_color=ACCENT_COLOR)
        self.lbl_status.pack(anchor="w", padx=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.log_frame, height=12, corner_radius=5)
        self.progress_bar.pack(fill="x", padx=5)
        self.progress_bar.set(0)

    # --- UI Logic ---
    def _toggle_theme(self):
        mode = self.switch_theme.get()
        ctk.set_appearance_mode(mode)
        self.switch_theme.configure(text=f"{mode} Mode")

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def _paste_clipboard(self):
        try:
            self.txt_topics.insert("0.0", self.clipboard_get())
        except: pass

    # --- Public API for Controller ---
    def log_message(self, msg):
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"> {msg}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")

    def set_loading(self, is_loading, determinate=False, message="Processing..."):
        self.lbl_status.configure(text=message)
        if is_loading:
            if determinate:
                self.progress_bar.configure(mode="determinate")
                self.progress_bar.set(0)
            else:
                self.progress_bar.configure(mode="indeterminate")
                self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.set(1) # Full

    def update_progress_val(self, val):
        self.progress_bar.set(val)

    def show_alert(self, title, msg, is_error=False):
        if is_error:
            messagebox.showerror(title, msg)
        else:
            messagebox.showinfo(title, msg)

    def get_video_path(self): return self.entry_video.get()
    def set_video_path(self, path): 
        self.entry_video.delete(0, "end")
        self.entry_video.insert(0, path)

    def get_text_path(self): return self.entry_text.get()
    def set_text_path(self, path):
        self.entry_text.delete(0, "end")
        self.entry_text.insert(0, path)

    def get_lang(self): return self.combo_lang.get()
    def get_topics_text(self): return self.txt_topics.get("0.0", "end")
    def get_manual_times(self): return self.entry_man_start.get(), self.entry_man_end.get()