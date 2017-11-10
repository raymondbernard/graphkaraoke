from neo4j.v1 import GraphDatabase, basic_auth
from config import NEO4J_IP
from config import NEO4J_PASSWORD

driver = GraphDatabase.driver("bolt://{}:7687".format(NEO4J_IP),
                              auth=basic_auth("neo4j", "{}".format(NEO4J_PASSWORD)))
session = driver.session()


class GraphKaraokeNeo4j(object):
    def __init__(self):
        self.session = session

    def graph_karaoke(self, loadfile):
        insert_query = '''
        LOAD csv with headers from {filename_new} as csv
        WITH csv.Sequence as seq, csv.Songsentence as row 
        UNWIND row as text
        WITH seq, reduce(t=tolower(text), delim in [",",".","!","?",'"',":",";","'","-"] | replace(t,delim,"")) as normalized
        WITH seq, [w in split(normalized," ") | trim(w)] as words
        unwind range(0,size(words)-2) as idx
        MERGE (w1:Word {name:words[idx], seq:toInt(seq)})
        MERGE (w2:Word {name:words[idx+1], seq:toInt(seq)})
        MERGE (w1)-[r:NEXT {seq:toInt(seq)}]->(w2)
        '''

        insert_query_match = '''
        MATCH (endword:Word), (startword:Word)
        WHERE NOT ()-[:NEXT]->(startword)
        AND NOT (endword)-[:NEXT]->()
        AND startword.seq=endword.seq+1
        MERGE (endword)-[:NEXTSENTENCE]->(startword)
        '''

        self.session.run(insert_query, parameters={"filename_new": loadfile})
        self.session.run(insert_query_match)
        # self.session.close()

    def add_artist_song(self, artist_name, song_title):
        print(artist_name)
        insert_query = '''
        MERGE (n:GraphKaraoke)  
        SET n.artist_name = {artist_name}
        SET n.song_title = {song_title}
        '''

        self.session.run(insert_query, parameters={"artist_name": artist_name, "song_title": song_title})

    def check_for_song(self):
        insert_query = '''
        MATCH (n:GraphKaraoke)
        RETURN n.artist_name AS artist_name, n.song_title AS song_title
        '''

        result = self.session.run(insert_query)
        for record in result:
            artist_name = record['artist_name']
            song_title = record['song_title']
            print('checking for artist in neo4j ... found artist_name = ' + str(artist_name))
            print('checking for songs in neo4j ... found song = ' + str(song_title))
            return artist_name, song_title
            # self.session.close()

    def get_max_seq(self):
        insert_query = '''
        MATCH (n:Word)
        WITH MAX(n.seq) AS MAXSEQ
        RETURN MAXSEQ AS max_seq
        '''
        max_seq = self.session.run(insert_query)
        # self.session.close()
        return max_seq

    def now_playing(self):
        insert_query = '''
        MATCH (n:GraphKaraoke)
        SET n.now_playing = true
        '''
        self.session.run(insert_query)
        # self.session.close()

    def reset_youtubeplayer(self):
        insert_query = '''
        MATCH (n:GraphKaraoke)
        SET n.now_playing = false
        '''
        self.session.run(insert_query)

    def check_youtubeplayer(self):
        insert_query = '''
        MATCH (n:GraphKaraoke)
        RETURN n.now_playing AS now_playing
        '''
        result = self.session.run(insert_query)
        for record in result:
            playing_status = record['now_playing']
            print('playing stauts is = ' + str(playing_status))
            return playing_status


if __name__ == '__main__':
    graphkaraoke = GraphKaraokeNeo4j()
    graphkaraoke.check_for_song()
