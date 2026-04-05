"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

class Artist:
    def __init__(self, artist_id, name, genre):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def track_count(self):
        count = len(self.tracks)
        return count