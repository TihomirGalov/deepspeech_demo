import datetime
import threading
import tkinter as tk

import deepspeech
import numpy as np

from mic_vad_streaming import VADAudio, MODEL_DIR, SCORER_DIR, DEFAULT_SAMPLE_RATE


class RecordingThread(threading.Thread):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.end_now = False

    def run(self):
        while True:
            if not self.end_now:
                self.main_loop()
            else:
                break
        return

    def main_loop(self):
        model = deepspeech.Model(MODEL_DIR)

        if SCORER_DIR:
            model.enableExternalScorer(SCORER_DIR)

        vad_audio = VADAudio(aggressiveness=3,
                             device=None,
                             input_rate=DEFAULT_SAMPLE_RATE,
                             file=None)
        file = open(f"media/{datetime.datetime.now()}_session.txt", "w")
        frames = vad_audio.vad_collector()
        stream_context = model.createStream()
        for frame in frames:
            if self.end_now:
                break
            if frame is not None:
                stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
            else:
                text = stream_context.finishStream()
                text += '\n'
                file.write(text)
                stream_context = model.createStream()
        file.close()


class RecordVoice(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Voice to text")
        self.geometry("500x300")
        self.resizable(True, True)

        self.standard_font = (None, 16)

        self.main_frame = tk.Frame(self, width=500, height=300, bg="lightgrey")

        self.start_button = tk.Button(self.main_frame, text="Start", bg="lightgrey", fg="black", command=self.start,
                                      font=self.standard_font)
        self.stop_button = tk.Button(self.main_frame, text="Stop", bg="lightgrey", fg="black", command=self.stop,
                                     font=self.standard_font, state="disabled")

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.start_button.pack(fill=tk.X, padx=50, anchor=tk.CENTER)
        self.stop_button.pack(fill=tk.X, padx=50, anchor=tk.CENTER)

    def setup_worker(self):
        worker = RecordingThread(self)
        self.worker = worker

    def start(self):
        if not hasattr(self, "worker"):
            self.setup_worker()

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.worker.start()

    def stop(self):
        self.stop_button.configure(state="disabled")
        self.start_button.configure(state="normal")
        self.worker.end_now = True
        del self.worker


if __name__ == "__main__":
    recorder = RecordVoice()
    recorder.mainloop()
