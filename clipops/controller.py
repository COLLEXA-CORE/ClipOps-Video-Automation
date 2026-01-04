# clipops/controller.py

import threading
from tkinter import filedialog
from .model import ClipOpsModel
from .view import ClipOpsView

class ClipOpsController:
    """
    Connects the View and Model.
    Handles Threading and Event Binding.
    """

    def __init__(self):
        self.model = ClipOpsModel()
        self.view = ClipOpsView()
        
        self._bind_events()

    def run(self):
        self.view.mainloop()

    def _bind_events(self):
        # File Browsing
        self.view.btn_browse_video.configure(command=self._browse_video)
        self.view.btn_browse_text.configure(command=self._browse_text)
        
        # Operations
        self.view.btn_transcribe.configure(command=self._start_transcribe)
        self.view.btn_whatsapp.configure(command=self._start_whatsapp)
        self.view.btn_translate.configure(command=self._start_translate)
        self.view.btn_vtt.configure(command=self._start_vtt)
        self.view.btn_topic_slice.configure(command=self._start_topic_slice)
        self.view.btn_manual_cut.configure(command=self._start_manual_cut)

    # --- UI Helpers ---
    def _log(self, msg):
        # Schedule update on main thread
        self.view.after(0, lambda: self.view.log_message(msg))

    def _progress(self, val):
        self.view.after(0, lambda: self.view.update_progress_val(val))

    def _browse_video(self):
        fn = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mkv *.avi")])
        if fn:
            self.view.set_video_path(fn)
            self._log(f"Video Loaded: {fn}")

    def _browse_text(self):
        fn = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if fn:
            self.view.set_text_path(fn)
            self._log(f"Transcript Loaded: {fn}")

    # --- Threading Managers ---
    def _run_threaded(self, target, *args, determinate=False):
        self.view.set_loading(True, determinate=determinate)
        
        def wrapper():
            if determinate:
                success = target(*args, log_callback=self._log, progress_callback=self._progress)
            else:
                success = target(*args, log_callback=self._log)
            
            self.view.after(0, lambda: self.view.set_loading(False, message="Done" if success else "Failed"))
            self.view.after(0, lambda: self.view.show_alert("Task Status", "Operation Completed!" if success else "Operation Failed!", not success))

        threading.Thread(target=wrapper, daemon=True).start()

    # --- Operation Handlers ---
    def _start_transcribe(self):
        path = self.view.get_video_path()
        if not path: return self.view.show_alert("Error", "No video selected!", True)
        self._run_threaded(self.model.transcribe_video, path)

    def _start_whatsapp(self):
        path = self.view.get_video_path()
        if not path: return self.view.show_alert("Error", "No video selected!", True)
        self._run_threaded(self.model.slice_whatsapp, path)

    def _start_translate(self):
        path = self.view.get_text_path()
        if not path: return self.view.show_alert("Error", "No text file selected!", True)
        lang = self.view.get_lang()
        self._run_threaded(self.model.translate_text, path, lang, determinate=True)

    def _start_vtt(self):
        path = self.view.get_text_path()
        if not path: return self.view.show_alert("Error", "No text file selected!", True)
        self._run_threaded(self.model.convert_to_vtt, path, determinate=True)

    def _start_topic_slice(self):
        path = self.view.get_video_path()
        text = self.view.get_topics_text()
        if not path: return self.view.show_alert("Error", "No video selected!", True)
        self._run_threaded(self.model.slice_topics, path, text)

    def _start_manual_cut(self):
        path = self.view.get_video_path()
        s, e = self.view.get_manual_times()
        if not path: return self.view.show_alert("Error", "No video selected!", True)
        self._run_threaded(self.model.manual_cut, path, s, e)