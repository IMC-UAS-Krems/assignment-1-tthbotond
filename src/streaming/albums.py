"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""


class Album:
    def __init__(self, album_id, title, artist, release_year):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []
    
    def add_track(self, track):
        track.album = self
        self.tracks.append(track)
        sorted_tracks = sorted(self.tracks, key=lambda t: t.track_number)
        self.tracks = sorted_tracks
    
    def track_ids(self):
        ids = set()
        for track in self.tracks:
            ids.add(track.track_id)
        return ids
    
    def duration_seconds(self):
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total