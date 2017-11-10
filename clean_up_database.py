from neo4j.v1 import GraphDatabase, basic_auth
from config import NEO4J_IP
from config import NEO4J_PASSWORD

# Set Neo4j DB  login credentials

'''Script used to clean up DB , job node and fb_message_counter'''


def clean_db():
    driver = GraphDatabase.driver("bolt://{}:7687".format(NEO4J_IP),
                                  auth=basic_auth("neo4j", "{}".format(NEO4J_PASSWORD)))
    session = driver.session()

    insert_query = '''
    MATCH (n)
    DETACH DELETE n
    '''

    session.run(insert_query)

    session.close()


if __name__ == '__main__':
    clean_db()
