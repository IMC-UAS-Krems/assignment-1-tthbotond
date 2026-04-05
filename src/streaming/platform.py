"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.artists = []
        self.tracks = []
        self.albums = []
        self.playlists = []
        self.sessions = []
    
    def add_user(self, user):
        self.users.append(user)
    
    def add_artist(self, artist):
        self.artists.append(artist)
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def add_album(self, album):
        self.albums.append(album)
    
    def get_track(self, track_id):
        for track in self.tracks:
            if track.track_id == track_id:
                return track
        return None
    
    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_artist(self, artist_id):
        for artist in self.artists:
            if artist.artist_id == artist_id:
                return artist
        return None
    
    def get_album(self, album_id):
        for album in self.albums:
            if album.album_id == album_id:
                return album
        return None
    
    def all_users(self):
        return self.users
    
    def all_tracks(self):
        return self.tracks
    
    # ---------queries---------

    def total_listening_time_minutes(self, start, end):
        total_seconds = 0
        for session in self.sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        minutes = total_seconds / 60.0
        return minutes
    
    def track_with_most_distinct_listeners(self):
        if len(self.sessions) == 0:
            return None
        
        track_listeners = {}
        for session in self.sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id
            
            if track_id not in track_listeners:
                track_listeners[track_id] = set()
            track_listeners[track_id].add(user_id)
        
        max_track_id = None
        max_count = 0
        for track_id in track_listeners:
            count = len(track_listeners[track_id])
            if count > max_count:
                max_count = count
                max_track_id = track_id
        
        return self.get_track(max_track_id)
    
    def top_artists_by_listening_time(self, n = 5):
        artist_time = {}
        for session in self.sessions:
            if hasattr(session.track, 'artist'):
                artist = session.track.artist
                artist_id = artist.artist_id
                
                if artist_id not in artist_time:
                    artist_time[artist_id] = 0
                artist_time[artist_id] += session.duration_listened_seconds / 60.0
        
        sorted_artists = []
        for artist_id in artist_time:
            minutes = artist_time[artist_id]
            sorted_artists.append((artist_id, minutes))
        
        sorted_artists.sort(key=lambda x: x[1], reverse=True)
        
        result = []
        for i in range(min(n, len(sorted_artists))):
            artist_id, minutes = sorted_artists[i]
            artist = self.get_artist(artist_id)
            if artist:
                result.append((artist, minutes))
        
        return result
    
    def users_who_completed_albums(self):
        result = []
        
        for user in self.users:
            completed_albums = []
            
            for album in self.albums:
                if len(album.tracks) == 0:
                    continue
                
                user_track_ids = set()
                for session in user.sessions:
                    user_track_ids.add(session.track.track_id)
                
                album_track_ids = album.track_ids()
                
                all_tracks_heard = True
                for album_track_id in album_track_ids:
                    if album_track_id not in user_track_ids:
                        all_tracks_heard = False
                        break
                
                if all_tracks_heard:
                    completed_albums.append(album.title)
            
            if len(completed_albums) > 0:
                result.append((user, completed_albums))
        
        return result