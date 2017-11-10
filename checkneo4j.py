

from neo4j.v1 import GraphDatabase, basic_auth
from neo4j.util import watch
import logging
from sys import stdout
from config import NEO4J_IP
from config import NEO4J_PASSWORD

driver = GraphDatabase.driver("bolt://{}:7687".format(NEO4J_IP),
                              auth=basic_auth("neo4j", "{}".format(NEO4J_PASSWORD)))
session = driver.session()

class TEST1(object):
    def __init__(self):
        pass

    def test1(self):
        insert_query = '''
        MATCH (n)
        RETURN n
        '''
        watch("neo4j.bolt", logging.DEBUG, stdout)

        result = session.run(insert_query)
        for record in result:
            n = record['n']
            print(n)


if __name__ == '__main__':
    check = TEST1()

    check.test1()
