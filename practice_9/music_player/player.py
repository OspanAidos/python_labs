import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.folder = music_folder
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith(('.mp3'))]
        self.current_index = 0
        self.is_playing = False

    def play(self):
        if not self.playlist:
            return
        
        track_path = os.path.join(self.folder, self.playlist[self.current_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def prev_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "Playlist is empty"
        return self.playlist[self.current_index]