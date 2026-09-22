# -*- coding: utf-8 -*-
"""Desktop window for Thorlabs Data Overview. No Python install needed once frozen."""

import os
import queue
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from Main_Folder_Walk import run_folder_walk
from version import APP_NAME, __version__


class ThorlabsOverviewApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME}  v{__version__}")
        self.geometry("820x560")
        self.minsize(640, 440)

        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Choose a parent folder, then click Run.")
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._worker = None
        self._pdf_path = None

        self._build_ui()
        self.after(100, self._poll_queue)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        header = ttk.Frame(self)
        header.pack(fill=tk.X, **pad)
        ttk.Label(
            header,
            text="Build TIFF stacks, averages, SNR stats, and a PDF overview.",
        ).pack(anchor=tk.W)

        folder_row = ttk.Frame(self)
        folder_row.pack(fill=tk.X, **pad)
        ttk.Label(folder_row, text="Folder:").pack(side=tk.LEFT)
        self.folder_entry = ttk.Entry(folder_row, textvariable=self.folder_var)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ttk.Button(folder_row, text="Browse…", command=self._browse).pack(side=tk.LEFT)

        buttons = ttk.Frame(self)
        buttons.pack(fill=tk.X, **pad)
        self.run_button = ttk.Button(buttons, text="Run", command=self._start_run)
        self.run_button.pack(side=tk.LEFT)
        self.stop_button = ttk.Button(buttons, text="Stop", command=self._request_stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=8)
        self.open_pdf_button = ttk.Button(
            buttons, text="Open PDF", command=self._open_pdf, state=tk.DISABLED
        )
        self.open_pdf_button.pack(side=tk.LEFT)

        ttk.Label(self, textvariable=self.status_var).pack(anchor=tk.W, padx=12)

        self.log_widget = ScrolledText(self, height=22, wrap=tk.WORD, state=tk.DISABLED)
        self.log_widget.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

    def _browse(self):
        chosen = filedialog.askdirectory(parent=self, title="Select the parent folder of Thorlabs recordings")
        if chosen:
            self.folder_var.set(chosen)

    def _append_log(self, message):
        self.log_widget.configure(state=tk.NORMAL)
        self.log_widget.insert(tk.END, message.rstrip() + "\n")
        self.log_widget.see(tk.END)
        self.log_widget.configure(state=tk.DISABLED)

    def _set_running(self, running):
        self.run_button.configure(state=tk.DISABLED if running else tk.NORMAL)
        self.stop_button.configure(state=tk.NORMAL if running else tk.DISABLED)
        self.folder_entry.configure(state=tk.DISABLED if running else tk.NORMAL)

    def _start_run(self):
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showinfo(APP_NAME, "Choose a parent folder first.")
            return
        if not os.path.isdir(folder):
            messagebox.showerror(APP_NAME, f"Folder does not exist:\n{folder}")
            return
        if self._worker and self._worker.is_alive():
            return

        self._stop_event.clear()
        self._pdf_path = None
        self.open_pdf_button.configure(state=tk.DISABLED)
        self.log_widget.configure(state=tk.NORMAL)
        self.log_widget.delete("1.0", tk.END)
        self.log_widget.configure(state=tk.DISABLED)
        self.status_var.set("Running… this can take several minutes.")
        self._set_running(True)

        self._worker = threading.Thread(target=self._run_worker, args=(folder,), daemon=True)
        self._worker.start()

    def _run_worker(self, folder):
        def log(message):
            self._queue.put(("log", str(message)))

        try:
            result = run_folder_walk(
                folder,
                log=log,
                should_stop=self._stop_event.is_set,
            )
            self._queue.put(("done", result))
        except Exception:
            self._queue.put(("crash", traceback.format_exc()))

    def _request_stop(self):
        self._stop_event.set()
        self.status_var.set("Stopping after the current step…")

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self._queue.get_nowait()
                if kind == "log":
                    self._append_log(payload)
                elif kind == "done":
                    self._on_done(payload)
                elif kind == "crash":
                    self._on_crash(payload)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _on_done(self, result):
        self._set_running(False)
        self._pdf_path = result.get("pdf_path")
        if self._pdf_path and os.path.isfile(self._pdf_path):
            self.open_pdf_button.configure(state=tk.NORMAL)

        if result.get("stopped"):
            self.status_var.set("Stopped.")
        elif result.get("errors"):
            self.status_var.set(f"Finished with {len(result['errors'])} error(s). See the log.")
        elif not result.get("recordings"):
            self.status_var.set("No recordings found. Check that you picked the right parent folder.")
        else:
            self.status_var.set("Done.")
            if self._pdf_path:
                if messagebox.askyesno(APP_NAME, f"Overview PDF written:\n{self._pdf_path}\n\nOpen it now?"):
                    self._open_pdf()

    def _on_crash(self, details):
        self._set_running(False)
        self.status_var.set("The run failed. See the log.")
        self._append_log(details)
        messagebox.showerror(APP_NAME, "The run failed. See the log for details.")

    def _open_pdf(self):
        if not self._pdf_path or not os.path.isfile(self._pdf_path):
            messagebox.showinfo(APP_NAME, "No PDF is available yet.")
            return
        try:
            os.startfile(self._pdf_path)
        except OSError as exc:
            messagebox.showerror(APP_NAME, f"Could not open the PDF:\n{exc}")

    def _on_close(self):
        if self._worker and self._worker.is_alive():
            self._stop_event.set()
        self.destroy()


def main():
    app = ThorlabsOverviewApp()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        details = traceback.format_exc()
        try:
            messagebox.showerror(APP_NAME, details)
        except Exception:
            print(details)
        raise
