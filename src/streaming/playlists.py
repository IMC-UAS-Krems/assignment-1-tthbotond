"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""


class Playlist:
    def __init__(self, playlist_id, title, owner):
        self.playlist_id = playlist_id
        self.title = title
        self.owner = owner
        self.tracks = []
    
    def add_track(self, track):
        """add track to playlist (no duplicates)"""
        if track not in self.tracks:
            self.tracks.append(track)
    
    def remove_track(self, track_id):
        """remove track by id"""
        self.tracks = [t for t in self.tracks if t.track_id != track_id]
    
    def total_duration_seconds(self):
        """sum all track durations"""
        return sum(track.duration_seconds for track in self.tracks)


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, title, owner):
        super().__init__(playlist_id, title, owner)
        self.contributors = [owner]
    
    def add_contributor(self, user):
        """add user as contributor (no duplicates)"""
        if user not in self.contributors:
            self.contributors.append(user)
    
    def remove_contributor(self, user):
        """remove contributor but keep owner"""
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)