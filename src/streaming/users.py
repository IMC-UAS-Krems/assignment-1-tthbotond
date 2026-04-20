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
        """add listening session to user"""
        self.sessions.append(session)
        
    def total_listening_seconds(self):
        """sum up all listening time"""
        return sum(session.duration_seconds for session in self.sessions)
        
    def total_listening_minutes(self):
        """convert total seconds to minutes"""
        return self.total_listening_seconds() / 60.0
    
    def unique_tracks_listened(self):
        """get set of unique tracks user has heard"""
        return {session.track.track_id for session in self.sessions}


class FreeUser(User):
    def __init__(self, user_id, name, age, max_skips_per_hour = 6):
        super().__init__(user_id, name, age)
        self.max_skips_per_hour = max_skips_per_hour


class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start = None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start or date.today()


class FamilyAccountUser(PremiumUser):
    # inherits from premium user for the premium features
    def __init__(self, user_id, name, age, subscription_start = None, sub_users = None):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = sub_users if sub_users is not None else []
        
    def add_sub_user(self, sub_user):
        """add family member to account"""
        self.sub_users.append(sub_user)
        
    def all_members(self):
        """return list of account holder and all family members"""
        return [self] + self.sub_users


class FamilyMember(User):
    def __init__(self, user_id, name, age, parent = None):
        super().__init__(user_id, name, age)
        self.parent = parent
