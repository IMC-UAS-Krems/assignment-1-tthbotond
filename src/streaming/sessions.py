"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from datetime import datetime


class ListeningSession:
    def __init__(self, session_id, user, track, timestamp, duration_listened_seconds):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds
        self.duration_seconds = duration_listened_seconds
        user.add_session(self)
    
    def duration_listened_minutes(self):
        """convert listening time to minutes"""
        return self.duration_listened_seconds / 60.0