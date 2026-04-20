"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from datetime import datetime

from streaming.users import User, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.tracks import Track, Song
from streaming.playlists import Playlist, CollaborativePlaylist


class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.artists = []
        self.tracks = []
        self.albums = []
        self.playlists = []
        self.sessions = []
    
    # ------- Registration Methods ----
    
    def add_user(self, user):
        """add user to the platform"""
        self.users.append(user)
    
    def add_artist(self, artist):
        """add an artist"""
        self.artists.append(artist)
    
    def add_track(self, track):
        """add a track to catalog"""
        self.tracks.append(track)
    
    def add_album(self, album):
        """register album on platform"""
        self.albums.append(album)
    
    def add_playlist(self, playlist):
        """add playlist to system"""
        self.playlists.append(playlist)
    
    def record_session(self, session):
        """record a listening session"""
        self.sessions.append(session)
    
    # ------- Accessor Methods ------
    
    def get_track(self, track_id):
        """retrieve track by id from collection"""
        for track in self.tracks:
            if track.track_id == track_id:
                return track
        return None
    
    def get_user(self, user_id):
        """find user in system"""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_artist(self, artist_id):
        """search for artist by their id"""
        for artist in self.artists:
            if artist.artist_id == artist_id:
                return artist
        return None
    
    def get_album(self, album_id):
        """lookup album"""
        for album in self.albums:
            if album.album_id == album_id:
                return album
        return None
    
    def all_users(self):
        """get all users"""
        return self.users
    
    def all_tracks(self):
        """get all tracks"""
        return self.tracks
    
    # ---- Query Methods -------
    
    # Q1: Total Cumulative Listening Time
    def total_listening_time_minutes(self, start, end):
        """Return total listening time (in minutes) for sessions in the given time window."""
        total_seconds = 0
        for session in self.sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0
    
    # Q2: Average Unique Tracks per Premium User
    def avg_unique_tracks_per_premium_user(self, days = 30):
        """calculate avg unique tracks listened by premium users in N days"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        
        # get premium users (not family account)
        premium_users = []
        for u in self.users:
            if isinstance(u, PremiumUser) and not isinstance(u, FamilyAccountUser):
                premium_users.append(u)
        
        if not premium_users:
            return 0.0
        
        total_unique = 0
        for user in premium_users:
            track_set = set()  # unique tracks for this user
            for session in user.sessions:
                if session.timestamp >= cutoff:
                    track_set.add(session.track.track_id)
            total_unique += len(track_set)
        
        average = total_unique / len(premium_users)
        return average
    
    # Q3: Track with Most Distinct Listeners
    def track_with_most_distinct_listeners(self):
        """find the track with most different people listening to it"""
        if not self.sessions:
            return None
        
        # count listeners per track
        track_listeners = {}
        for session in self.sessions:
            tid = session.track.track_id
            uid = session.user.user_id
            if tid not in track_listeners:
                track_listeners[tid] = set()
            track_listeners[tid].add(uid)

        most_heard_id = max(track_listeners.keys(), key=lambda t: len(track_listeners[t]))
        result = self.get_track(most_heard_id)
        return result
    
    # Q4: Average Session Duration by User Type
    def avg_session_duration_by_user_type(self):
        """avg listening time per user type sorted longest first"""
        # group sessions by type
        type_sessions = {}
        
        for session in self.sessions:
            utype = type(session.user).__name__
            if utype not in type_sessions:
                type_sessions[utype] = []
            type_sessions[utype].append(session.duration_listened_seconds)

        results = []
        for utype, durations in type_sessions.items():
            total = sum(durations)
            avg = total / len(durations)
            results.append((utype, avg))
        
        # sort descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    # Q5: Total Listening Time for Underage Sub-Users
    def total_listening_time_underage_sub_users_minutes(self, age_threshold = 18):
        """total listening time for family members under age limit in minutes"""
        total_secs = 0
        
        for user in self.users:
            if isinstance(user, FamilyMember):
                if user.age < age_threshold:
                    total_secs += user.total_listening_seconds()
        
        minutes_result = total_secs / 60.0
        return minutes_result
    
    # Q6: Top Artists by Listening Time
    def top_artists_by_listening_time(self, n = 5):
        """return top N artists by total time listened (songs only)"""
        artist_time = {}  # map artist id to total minutes
        
        for session in self.sessions:
            if isinstance(session.track, Song):
                art = session.track.artist
                aid = art.artist_id
                if aid not in artist_time:
                    artist_time[aid] = 0.0
                artist_time[aid] += session.duration_listened_seconds / 60.0
        
        sorted_list = sorted(
            artist_time.items(),
            key=lambda x: x[1],
            reverse=True)[:n]
        
        output = []
        for aid, mins in sorted_list:
            a = self.get_artist(aid)
            if a:
                output.append((a, mins))
        
        return output
    
    # Q7: User's Top Genre
    def user_top_genre(self, user_id):
        """get most listened genre for user and percentage of total"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        genre_map = {}
        total = 0
        
        for sess in user.sessions:
            g = sess.track.genre
            if g not in genre_map:
                genre_map[g] = 0
            genre_map[g] += sess.duration_listened_seconds
            total += sess.duration_listened_seconds
        
        if total == 0:
            return None
        
        top = max(genre_map.keys(), key=lambda g: genre_map[g])
        pct = (genre_map[top] / total) * 100.0
        
        return (top, pct)
    
    # Q8: Collaborative Playlists with Many Artists
    def collaborative_playlists_with_many_artists(self, threshold = 3):
        """find collaborative playlists with more than X different artists (only songs)"""
        
        outcomes = []
        
        for plist in self.playlists:
            if isinstance(plist, CollaborativePlaylist):
                # collect unique artists from songs
                artist_ids = set()
                for track in plist.tracks:
                    if isinstance(track, Song):
                        if hasattr(track, 'artist'):
                            artist_ids.add(track.artist.artist_id)
                
                if len(artist_ids) > threshold:
                    outcomes.append(plist)
        
        return outcomes
    
    # Q9: Average Tracks per Playlist Type
    def avg_tracks_per_playlist_type(self):
        """average number of tracks in each playlist type"""
        counts_by_type = {
            "Playlist": [],
            "CollaborativePlaylist": []
        }
        
        for pl in self.playlists:
            if isinstance(pl, CollaborativePlaylist):
                counts_by_type["CollaborativePlaylist"].append(len(pl.tracks))
            else:
                counts_by_type["Playlist"].append(len(pl.tracks))
        
        averages = {}
        for ptype, count_list in counts_by_type.items():
            if count_list:
                averages[ptype] = sum(count_list) / len(count_list)
            else:
                averages[ptype] = 0.0
        
        return averages
    
    # Q10: Users Who Completed Albums
    def users_who_completed_albums(self):
        """users who listened to every song on at least one album"""
        outcomes = []
        
        for user in self.users:
            finished_albums = []
            
            for alb in self.albums:
                if not alb.tracks:
                    continue
                
                # get users tracks
                heard_ids = set()
                for sess in user.sessions:
                    heard_ids.add(sess.track.track_id)
                
                album_ids = alb.track_ids()
                
                # check if all album tracks heard
                if album_ids.issubset(heard_ids):
                    finished_albums.append(alb.title)
            
            if finished_albums:
                outcomes.append((user, finished_albums))
        
        return outcomes