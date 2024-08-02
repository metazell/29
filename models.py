"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    songs = db.relationship('PlaylistSong', backref='playlist', lazy=True)

class Song(db.Model):
    """Song."""
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    playlists = db.relationship('PlaylistSong', backref='song', lazy=True)

class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
