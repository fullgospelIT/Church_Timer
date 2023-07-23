import tkinter as tk
from pynput import keyboard
from datetime import timedelta

class CountdownTimer:
    def __init__(self, minutes=10):
        self.minutes = minutes
        self.seconds = minutes * 60

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")
        self.root.bind("<Escape>", self.quit_fullscreen)
        self.root.bind("<space>", self.start_timer)

        self.time_adjustment = tk.IntVar(value=self.minutes)

        self.label = tk.Label(self.root, font=("Helvetica", 200, "bold"), fg="white", bg="black")
        self.label.grid(row=0, column=0, padx=50, pady=200, columnspan=3)

        self.subtitle_label = tk.Label(self.root, font=("Helvetica", 60, "bold"), fg="white", bg="black", text="Press Space to Start")
        self.subtitle_label.grid(row=1, column=0, columnspan=3, pady=50)

        self.entry = tk.Entry(self.root, textvariable=self.time_adjustment, font=("Helvetica", 80, "bold"), width=5)
        self.entry.grid(row=2, column=0, pady=20)

        self.up_button = tk.Button(self.root, text="▲", command=self.adjust_timer_up, font=("Helvetica", 48, "bold"), width=3)
        self.up_button.grid(row=2, column=1, padx=10)

        self.down_button = tk.Button(self.root, text="▼", command=self.adjust_timer_down, font=("Helvetica", 48, "bold"), width=3)
        self.down_button.grid(row=2, column=2, padx=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer, font=("Helvetica", 48, "bold"), width=10, state=tk.DISABLED)
        self.stop_button.grid(row=3, column=0, pady=20, columnspan=3)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.timer_running = False

    def quit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def start_timer(self, event=None):
        if not self.timer_running:
            self.minutes = self.time_adjustment.get()
            self.seconds = self.minutes * 60
            self.timer_running = True
            self.stop_button.config(state=tk.NORMAL)
            self.entry.config(state=tk.DISABLED)
            self.up_button.config(state=tk.DISABLED)
            self.down_button.config(state=tk.DISABLED)
            self.subtitle_label.config(text="")
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.stop_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.up_button.config(state=tk.NORMAL)
        self.down_button.config(state=tk.NORMAL)

    def update_timer(self):
        if self.timer_running:
            minutes = self.seconds // 60
            seconds = self.seconds % 60

            time_string = str(timedelta(minutes=minutes, seconds=seconds))
            self.label.config(text=time_string)

            if self.seconds > 0:
                self.seconds -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.label.config(bg="red")
                self.subtitle_label.config(text="Time Up!", bg="red")
                self.timer_running = False

    def adjust_timer_up(self):
        self.time_adjustment.set(self.time_adjustment.get() + 1)

    def adjust_timer_down(self):
        if self.time_adjustment.get() > 0:
            self.time_adjustment.set(self.time_adjustment.get() - 1)

    def on_close(self):
        self.stop_timer()
        self.root.destroy()

if __name__ == "__main__":
    timer = CountdownTimer()
    timer.root.mainloop()
