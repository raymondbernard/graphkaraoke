import pylyrics3
from flask import Flask, render_template, request
from process_lyrics import get_lyrics
from clean_up_database import clean_db
from models import GraphKaraokeNeo4j

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    song_lyrics = ''
    graphkaraoke = GraphKaraokeNeo4j()
    if request.method == 'POST':
        clean_db()
        # receiving the form
        artist_name = request.form['artist']
        song_title = request.form['song_title']
        print(artist_name)
        print(song_title)
        try:
            graphkaraoke.reset_youtubeplayer()
            song_lyrics = pylyrics3.get_song_lyrics(artist_name, song_title)
            get_lyrics(artist_name, song_title)

            filename = 'final_' + str(song_title).replace(' ', '_')
            loadfile = 'file:///{}.gk.csv'.format(filename)

            graphkaraoke.graph_karaoke(loadfile)
            graphkaraoke.add_artist_song(artist_name, song_title)

            return render_template('index.html', song_lyrics=song_lyrics, artist=request.form['artist'],
                                     song_title=request.form['song_title'])
        except Exception as e:
            print(e)
            error_msg = "Sorry the DJ, doesn't have caryy {} by {} :) Perahps you have a typo?".format(song_title, artist_name)
            return render_template('index.html', song_lyrics=song_lyrics, artist='',
                                   song_title=error_msg)
    else:
        clean_db()


        song_lyrics = ''
        return render_template('index.html', song_lyrics=song_lyrics)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, debug=True)


