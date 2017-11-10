import csv
import pylyrics3
from config import NEO4J_PATH

neo4j_path = NEO4J_PATH


def get_lyrics(artist_name, song):
    filename = song.replace(' ', '_')

    filenamenew = filename + '.gk'

    lyrics = pylyrics3.get_song_lyrics(artist_name, song)
    # print(lyrics)

    with open("{}{}.csv".format(neo4j_path, filename), "w") as f:
        f.write(lyrics)

    with open('{}{}.csv'.format(neo4j_path, filename), "r") as openfile:
        with open('{}{}.csv'.format(neo4j_path, filenamenew), "w") as out_file:
            for j, line in enumerate(openfile):
                out_file.write('{}{}'.format((j + 1), ',' + line.replace(",", "")))

    with open('{}{}.csv'.format(neo4j_path, filenamenew), "r") as csv_header:
        csv_reader = csv.reader(csv_header)
        filenamefinal = 'final_' + filenamenew
        with open('{}{}.csv'.format(neo4j_path, filenamefinal), "w") as csv_final:
            csv_writer = csv.writer(csv_final)
            csv_writer.writerow(['Sequence', 'Songsentence'])
            for line in csv_reader:
                csv_writer.writerow(line)
    return filenamefinal, artist_name, song, lyrics


if __name__ == '__main__':
    artist_name = ''
    song = ''
    get_lyrics(artist_name, song)
