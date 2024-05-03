import os
import tkinter as tk
from tkinter import filedialog
import pygame
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

class MediaPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Media Player")
        self.geometry("400x200")
        
        self.current_file = None
        self.is_paused = False
        
        self.initialize_ui()
        
    def initialize_ui(self):
        self.btn_open = tk.Button(self, text="Open File", command=self.open_file)
        self.btn_play_pause = tk.Button(self, text="Play", command=self.play_pause)
        self.btn_stop = tk.Button(self, text="Stop", command=self.stop)
        
        self.btn_open.pack(pady=10)
        self.btn_play_pause.pack(pady=5)
        self.btn_stop.pack(pady=5)
        
        self.progress_bar = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=300, command=self.set_playback_position)
        self.progress_bar.pack(pady=5)
        
        self.volume_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=100, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(pady=5)
        
        mixer.init()
        
    def open_file(self):
        self.current_file = filedialog.askopenfilename()
        if self.current_file:
            _, file_extension = os.path.splitext(self.current_file)
            if file_extension.lower() in ['.mp3', '.mp4']:
                self.load_media()
            else:
                print("Unsupported file format.")
    
    def load_media(self):
        mixer.music.load(self.current_file)
        if self.current_file.endswith('.mp3'):
            audio_info = MP3(self.current_file)
        elif self.current_file.endswith('.mp4'):
            audio_info = MP4(self.current_file)
        self.duration = audio_info.info.length
        self.progress_bar.config(to=self.duration)
        
    def play_pause(self):
        if not self.current_file:
            print("No file selected.")
            return
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            self.btn_play_pause.config(text="Pause")
        else:
            start_pos = self.progress_bar.get()
            mixer.music.play(start=int(start_pos))
            self.is_paused = True
            self.btn_play_pause.config(text="Play")
    
    def stop(self):
        mixer.music.stop()
        self.is_paused = False
        self.btn_play_pause.config(text="Play")
    
    def set_volume(self, volume):
        mixer.music.set_volume(int(volume) / 100)
    
    def set_playback_position(self, position):
        if self.is_paused:
            mixer.music.set_pos(float(position))

if __name__ == "__main__":
    app = MediaPlayer()
    app.mainloop()
