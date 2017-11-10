import time
from models import GraphKaraokeNeo4j
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class RoboRunGraphKaraoke(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument('--no-sandbox')
        path_to_extension = r'C:\Users\cosmicray\AppData\Local\Google\Chrome\User Data\Default\Extensions\gleekbfjekiniecknbkamfmkohkpodhe\1.1_0'
        chrome_options.add_argument('load-extension=' + path_to_extension)
        self.driver = webdriver.Chrome('C:\\Users\\cosmicray\\Downloads\\chromedriver_win32\\chromedriver.exe',
                                       chrome_options=chrome_options)

        self.driver.maximize_window()

    def open_browser(self):
        self.driver.get('http://localhost:7474')

    def robo_play_neo4j(self):
        neo4jplayer = self.driver
        # neo4jplayer.switch_to.frame('neo4j_iframe')
        graphkaraoke = GraphKaraokeNeo4j()

        neo4jplayer.maximize_window()
        max_seq = graphkaraoke.get_max_seq()

        neo4jplayer.implicitly_wait(10)

        neo4jplayer.maximize_window()

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
            action.move_by_offset(150, 50).click()
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

            time.sleep(3)
        time.sleep(600)


if __name__ == '__main__':
    neo4jbot = RoboRunGraphKaraoke()
    neo4jbot.open_browser()
    neo4jbot.robo_play_neo4j()
