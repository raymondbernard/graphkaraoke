import time
from models import GraphKaraokeNeo4j
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from neo4jrobot import RoboRunGraphKaraoke

chrome_options = webdriver.ChromeOptions()


class RunGraphKaraoke(object):
    def __init__(self):
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument("disable-infobars")

        #Please point the app to your local chrome profile!

        chrome_options.add_argument("user-data-dir=C:\\Users\cosmicray\AppData\Local\Google\Chrome\\User2 Data")

        #Change path to the location of the chromedriver

        self.driver = webdriver.Chrome('C:\\Users\\cosmicray\\Downloads\\chromedriver_win32\\chromedriver.exe',
                                       chrome_options=chrome_options)

        self.driver.maximize_window()

    def open_browser(self):
        self.driver.get('http://localhost')

    def play_song(self):
        # Check Neo4j for Artist songs in Neo4j
        graphkaraokeneo4j = GraphKaraokeNeo4j()
        x = 1
        while x == 1:

            songexsist = graphkaraokeneo4j.check_for_song()
            print('Does Song Exists?...checking..')
            time.sleep(1)

            youtube = graphkaraokeneo4j.check_youtubeplayer()
            print(youtube)

            if songexsist and not youtube:

                record = graphkaraokeneo4j.check_for_song()
                try:
                    print('Song record = ' + str(record))
                    artistname = record[0]
                    song = record[1]

                    youtubeplayer = self.driver
                    searchyoutube = artistname + ' ' + song
                except Exception as e:
                    print(e)
                    break
                try:
                    youtubeplayer.switch_to.frame('youtube_iframe')
                except Exception as e:
                    print(e)
                # youtubeplayer.get('https://www.youtube.com')

                try:
                    youtubeplayer.find_element_by_css_selector('button#search-button').click()
                    youtubeplayer.find_element_by_css_selector('input#search').send_keys(searchyoutube)
                    youtubeplayer.find_element_by_css_selector('button#search-icon-legacy').click()
                    youtubeplayer.implicitly_wait(100)
                    graphkaraokeneo4j.now_playing()
                    youtubeplayer.find_element_by_css_selector(
                        '#contents > ytd-video-renderer:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div > h3 > a').click()
                    youtubeplayer.implicitly_wait(100)
                    # self.play_neo4j(youtubeplayer)

                    neo4jbot = RoboRunGraphKaraoke()
                    neo4jbot.open_browser()
                    neo4jbot.robo_play_neo4j()

                except Exception as e:
                    print(e)

                return youtubeplayer
            else:
                print('the song was played already ... Skipping youtube player')
                continue

    def play_neo4j(self, youtubeplayer):
        print('** inside of neo4j player')
        neo4jplayer = youtubeplayer
        try:
            neo4jplayer.switch_to.frame('neo4j_iframe')
        except Exception as e:
            print(e)
        graphkaraokeneo4j = GraphKaraokeNeo4j()
        max_seq = graphkaraokeneo4j.get_max_seq()
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("disable-infobars")

        neo4jplayer.implicitly_wait(10)
        time.sleep(3)
        neo4jplayer.find_element_by_css_selector(
            '#mount > div > div > div > div.eDGLpH > div > div.juaakC > article > div.bdeIvc > div > div.XgqFE > div > div.eyORHI > form > div:nth-child(3) > input').send_keys(
            'Cosmic2016#')
        neo4jplayer.maximize_window()
        neo4jplayer.find_element_by_css_selector('button[type="button"]').click()

        for record in max_seq:
            action = webdriver.ActionChains(neo4jplayer)
            max_seq = record['max_seq']
            print('the max_seq = ' + str(max_seq))
            counter = 0
            size = neo4jplayer.find_element_by_name('DB').size
            location = neo4jplayer.find_element_by_name('DB').location

            print(size)
            print(location)

            time.sleep(2)
            action.move_by_offset(0, -325).context_click()
            action.perform()
            print('maq_seq after call ==' + str(max_seq))
            for x in range(max_seq + 1):
                action.send_keys(Keys.ENTER)

                time.sleep(1)
                counter += 1
                seq = 'seq:{}'.format(counter)

                seq = '{' + seq + '}'
                query_string = 'MATCH (n:Word{}) RETURN n'.format(seq)
                print('neo4j query string = ' + str(query_string))
                for character in query_string:
                    action.send_keys(character)
                    time.sleep(0.1)

                action.perform()

                action.reset_actions()
                # neo4jplayer.find_element_by_class_name('bputMa').click()
                # action.send_keys('MATCH this sucks ass').perform()
            time.sleep(3)


if __name__ == '__main__':

    rungraphkaraoke = RunGraphKaraoke()
    rungraphkaraoke.open_browser()
    x = 1
    while x == 1:
        rungraphkaraoke.play_song()
