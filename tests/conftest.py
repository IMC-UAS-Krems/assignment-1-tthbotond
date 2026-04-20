"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",     genre="pop")
    synthwaves = Artist("a2", "SynthWaves", genre="electronic")
    bluejazz = Artist("a3", "Blue Jazz", genre="jazz")
    
    for artist in (pixels, synthwaves, bluejazz):
        platform.add_artist(artist)

    # ------------------------------------------------------------------
    # albums & AlbumTracks
    # ------------------------------------------------------------------
    # album 1: Pixels - Digital Dreams
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)
    
    # album 2: SynthWaves - Neon Nights
    nn = Album("alb2", "Neon Nights", artist=synthwaves, release_year=2023)
    t4 = AlbumTrack("t4", "Neon Dreams",     240, "electronic", synthwaves, track_number=1)
    t5 = AlbumTrack("t5", "Synthetic Heart", 200, "electronic", synthwaves, track_number=2)
    for track in (t4, t5):
        nn.add_track(track)
        platform.add_track(track)
        synthwaves.add_track(track)
    platform.add_album(nn)
    
    # single releases
    s1 = SingleRelease("t6", "Blue Vibes", 220, "jazz", bluejazz, release_date=date(2024, 1, 1))
    s2 = SingleRelease("t7", "Electric Soul", 200, "pop", pixels, release_date=date(2024, 2, 1))
    
    for track in (s1, s2):
        platform.add_track(track)
        track.artist.add_track(track)

    # ------------------------------------------------------------------
    # users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    parent = FamilyAccountUser("u3", "Parent", age=45, subscription_start=date(2022, 6, 1))
    child = FamilyMember("u4", "Child", age=15, parent=parent)
    parent.add_sub_user(child)

    for user in (alice, bob, parent, child):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # listening sessions
    # ------------------------------------------------------------------
    # Alice's sessions (FreeUser)
    session1 = ListeningSession("s1", alice, t1, RECENT - timedelta(hours=2), 180)  # 3 mins
    session2 = ListeningSession("s2", alice, t2, RECENT - timedelta(hours=1), 210)  # 3.5 mins
    session3 = ListeningSession("s3", alice, t4, OLD, 240)  # 4 mins (old)
    
    # Bob's sessions (PremiumUser)
    session4 = ListeningSession("s4", bob, t1, RECENT, 180)
    session5 = ListeningSession("s5", bob, t3, RECENT - timedelta(hours=3), 195)
    session6 = ListeningSession("s6", bob, t4, RECENT - timedelta(hours=4), 240)
    session7 = ListeningSession("s7", bob, s1, RECENT - timedelta(days=1), 220)
    session8 = ListeningSession("s8", bob, s2, RECENT - timedelta(days=2), 200)
    
    # parent's sessions (FamilyAccountUser)
    session9 = ListeningSession("s9", parent, t2, RECENT - timedelta(hours=5), 210)
    session10 = ListeningSession("s10", parent, s1, RECENT - timedelta(hours=6), 220)
    
    # child's sessions (FamilyMember - underage)
    session11 = ListeningSession("s11", child, t1, RECENT - timedelta(hours=7), 180)
    session12 = ListeningSession("s12", child, t5, RECENT - timedelta(hours=8), 200)
    
    # add sessions to platform
    for session in [session1, session2, session3, session4, session5, session6, 
                    session7, session8, session9, session10, session11, session12]:
        platform.sessions.append(session)

    # ------------------------------------------------------------------
    # playlists
    # ------------------------------------------------------------------
    # standard playlist
    pl1 = Playlist("pl1", "Pop Hits", alice)
    pl1.add_track(t1)
    pl1.add_track(t2)
    pl1.add_track(s2)
    platform.playlists.append(pl1)
    
    # collaborative playlist with multiple artists
    cpl1 = CollaborativePlaylist("cpl1", "Mixed Vibes", bob)
    cpl1.add_track(t1)
    cpl1.add_track(t4)
    cpl1.add_track(s1)
    cpl1.add_track(t5)  # more than 3 artists (pixels, synthwaves, bluejazz, synthwaves)
    cpl1.add_contributor(alice)
    platform.playlists.append(cpl1)
    
    # another collaborative playlist with fewer artists
    cpl2 = CollaborativePlaylist("cpl2", "Jazz Night", parent)
    cpl2.add_track(s1)
    cpl2.add_track(t2)
    platform.playlists.append(cpl2)

    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
