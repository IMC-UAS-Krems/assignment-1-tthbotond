"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

from datetime import date

class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []
        
    def add_session(self, session):
        self.sessions.append(session)
        
    def total_listening_seconds(self):
        total = 0
        for session in self.sessions:
            total += session.duration_seconds
        return total
        
    def total_listening_minutes(self):
        seconds = self.total_listening_seconds()
        minutes = seconds / 60.0
        return minutes
    
    def unique_tracks_listened(self):
        tracks = set()
        for session in self.sessions:
            tracks.add(session.track.track_id)
        return tracks


class FreeUser(User):
    def __init__(self, user_id, name, age, max_skips_per_hour = 6):
        super().__init__(user_id, name, age)
        self.max_skips_per_hour = max_skips_per_hour


class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start = None):
        super().__init__(user_id, name, age)
        if subscription_start is None:
            self.subscription_start = date.today()
        else:
            self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id, name, age, subscription_start = None, sub_users = None):
        super().__init__(user_id, name, age, subscription_start)
        if sub_users is None:
            self.sub_users = []
        else:
            self.sub_users = sub_users
        
    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)
        
    def all_members(self):
        members = [self]
        members.extend(self.sub_users)
        return members


class FamilyMember(User):
    def __init__(self, user_id, name, age, parent = None):
        super().__init__(user_id, name, age)
        self.parent = parent
