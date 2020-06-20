# -*- coding: utf-8 -*-
from pathlib import Path
from flask import Flask, render_template
import io

from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

SONGS_PATH = Path('songs/')

app = Flask(__name__)
app.secret_key = 'dev'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

bootstrap = Bootstrap(app)
Markdown(app)


def load_songs():
    files = SONGS_PATH.glob("*.md")

    songs = []
    for fn in files:
        song_name = fn.name.replace('.md', '')
        song_title = song_name.replace('_', ' ').title()
        songs.append((song_name, song_title))

    return songs


@app.route('/')
def index():
    songs = load_songs()
    return render_template('index.html', songs=songs)

@app.route('/song/<song_name>')
def song(song_name):
    songs = load_songs()
    song_path = SONGS_PATH/f"{song_name}.md"
    with io.open(song_path, mode="r", encoding="utf-8") as fh:
        content = fh.read()
    song = dict(
        title=dict(songs)[song_name],
        content=content.replace("\n", "  \n")
    )
    return render_template('song.html', songs=songs, song=song)


if __name__ == '__main__':
    app.run(debug=True)
