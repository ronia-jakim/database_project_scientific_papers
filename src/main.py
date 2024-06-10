import json
import psycopg2 as psql
import math

import mainpulating as manip
import listing as lst

# import handle_connection as conn
# import modifying_database as art
# import author_listing as auth_lst

def main():
    cursor = None
    connection = None

    while True:
        try:
            cmd = str(input())
            parsed = json.loads(cmd)


            if 'open' in parsed: 
                arguments = parsed['open']
                # (cursor, connection) = conn.open_connection(arguments['host'], arguments['baza'], arguments['login'], arguments['password'])
                try: 
                    connection = psql.connect(database=arguments['baza'], user=arguments['login'], password=arguments['password'], host=arguments['host'])  
                    cursor = connection.cursor()
                except:
                    print('{ "status" : "ERROR could not open database" }')

            elif 'article' in parsed: 
                if cursor is None or connection is None: 
                    print('{ "status" : "ERROR no database open" }')
                else:
                    manip.add_article(parsed, cursor, connection)

            elif 'points' in parsed: 
                print('{ "status" : "NOT IMPLEMENTED" }')

            elif 'institution' in parsed: 
                if cursor is None or connection is None: 
                    print('{ "status" : "ERROR no database open" }')
                else:
                    lst.list_institutions(parsed, cursor, connection)


            elif 'author' in parsed: 
                if cursor is None or connection is None: 
                    print('{ "status" : "ERROR no database open" }')
                else:
                    lst.list_authors(parsed, cursor, connection)

            elif 'author_details' in parsed: 
                print('{ "status" : "NOT IMPLEMENTED" }')
        except EOFError:
            return


main()
