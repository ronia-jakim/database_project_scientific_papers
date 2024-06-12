import json
import psycopg2 as psql
import math

import manipulating as manip
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
                    print('{ "status": "OK" }')
                except:
                    print('{ "status": "ERROR" }')
            elif 'newuser' in parsed:
                arguments = parsed['newuser']
                try:
                    cursor.execute("""
                                    INSERT INTO users (secret, login, passwd) VALUES (
                                        %s, %s, %s
                                        )
                                   """, (
                                       arguments['secret'], 
                                       arguments['newlogin'], 
                                       arguments['newpassword'])
                                   )
                    print('{ "status": "OK" }')
                except:
                    print('{ "status": "ERROR" }')
            elif 'deluser' in parsed: 
                print('{ "status": "NOT IMPLEMENTED" }')

            elif 'article' in parsed: 
                if cursor is None or connection is None: 
                    print('{ "status" : "ERROR" }')
                else:
                    manip.add_article(parsed, cursor, connection)

            elif 'points' in parsed: 
                # print('{ "status" : "NOT IMPLEMENTED" }')
                if cursor is None or connection is None: 
                    print('{ "status": "ERROR" }')
                else: 
                    manip.change_points(parsed, cursor, connection)

            elif 'institution' in parsed: 
                if cursor is None or connection is None: 
                    print('{ "status" : "ERROR" }')
                else:
                    lst.list_institutions(parsed, cursor, connection)


            elif 'author' in parsed: 
                if cursor is None or connection is None: 
                    print('{ "status" : "ERROR" }')
                else:
                    lst.list_authors(parsed, cursor, connection)

            elif 'author_details' in parsed: 
                print('{ "status" : "NOT IMPLEMENTED" }')
        except EOFError:
            return


main()
