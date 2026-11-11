import tkinter as tk
from tkinter import colorchooser
from datetime import datetime
import json
import os

CONFIG_FILE = "clock_config.json"

DEFAULT_BG = "#1e1e2e"
DEFAULT_FG = "#cba6f7"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"bg": DEFAULT_BG, "fg": DEFAULT_FG}


def save_config(bg, fg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"bg": bg, "fg": fg}, f)


class DesktopClock:
    def __init__(self, root):
        self.root = root
        self.root.title("桌面时钟")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        self.config = load_config()

        self._build_ui()
        self._tick()

    def _build_ui(self):
        bg = self.config["bg"]
        fg = self.config["fg"]

        self.root.configure(bg=bg)

        self.time_label = tk.Label(
            self.root, text="", font=("Consolas", 48, "bold"),
            bg=bg, fg=fg
        )
        self.time_label.pack(expand=True)

        self.date_label = tk.Label(
            self.root, text="", font=("Microsoft YaHei", 12),
            bg=bg, fg=fg
        )
        self.date_label.pack()

        btn_frame = tk.Frame(self.root, bg=bg)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="改背景色", command=self._pick_bg,
            font=("Microsoft YaHei", 10)
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame, text="改文字色", command=self._pick_fg,
            font=("Microsoft YaHei", 10)
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame, text="恢复默认", command=self._reset,
            font=("Microsoft YaHei", 10)
        ).pack(side=tk.LEFT, padx=6)

    def _tick(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%Y-%m-%d  %A"))
        self.root.after(1000, self._tick)

    def _pick_bg(self):
        color = colorchooser.askcolor(title="选择背景色")[1]
        if color:
            self._apply(bg=color)

    def _pick_fg(self):
        color = colorchooser.askcolor(title="选择文字色")[1]
        if color:
            self._apply(fg=color)

    def _apply(self, bg=None, fg=None):
        if bg:
            self.config["bg"] = bg
            self.root.configure(bg=bg)
            self.time_label.configure(bg=bg)
            self.date_label.configure(bg=bg)
        if fg:
            self.config["fg"] = fg
            self.time_label.configure(fg=fg)
            self.date_label.configure(fg=fg)
        self._recolor_widgets(bg or self.config["bg"])
        save_config(self.config["bg"], self.config["fg"])

    def _recolor_widgets(self, bg):
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg)
            except tk.TclError:
                pass

    def _reset(self):
        self.config = {"bg": DEFAULT_BG, "fg": DEFAULT_FG}
        self._apply(bg=DEFAULT_BG, fg=DEFAULT_FG)


if __name__ == "__main__":
    root = tk.Tk()
    DesktopClock(root)
    root.mainloop()