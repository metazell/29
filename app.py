from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import PlaylistForm, SongForm, AddSongToPlaylistForm
import os

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/playlists")
def show_all_playlists():
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(new_playlist)
        db.session.commit()
        flash('Playlist created successfully!', 'success')
        return redirect(url_for('show_all_playlists'))
    return render_template('new_playlist.html', form=form)

@app.route("/songs")
def show_all_songs():
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        flash('Song added successfully!', 'success')
        return redirect(url_for('show_all_songs'))
    return render_template('new_song.html', form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = AddSongToPlaylistForm()

    curr_on_playlist = [song.id for song in playlist.songs]
    form.song.choices = [(song.id, song.title) for song in Song.query.all() if song.id not in curr_on_playlist]

    if form.validate_on_submit():
        playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=form.song.data)
        db.session.add(playlist_song)
        db.session.commit()
        flash('Song added to playlist!', 'success')
        return redirect(url_for('show_playlist', playlist_id=playlist_id))
    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)

if __name__ == '__main__':
    app.run(debug=True)
