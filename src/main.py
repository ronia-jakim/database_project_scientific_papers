import json
import psycopg2 as psql

import handle_connection as conn
import articles as art

def main():
    cursor = None
    connection = None
    while True:
        cmd = str(input())
        parsed = json.loads(cmd)

        if 'open' in parsed: 
            arguments = parsed['open']
            (cursor, connection) = conn.open_connection(arguments['host'], arguments['baza'], arguments['login'], arguments['password'])
            if cursor is None: 
                return
        elif 'article' in parsed: 
            if cursor is None or connection is None: 
                print('{ "status" : "ERROR: no database open" }')
            else:
                arguments = parsed['article']
                # print(arguments['login'])
                # print(arguments['password'])
                # print(arguments['date'])
                # print(arguments['conference'])
                # print(arguments['author list'])
                art.add_article(arguments['login'],    
                                arguments['password'], 
                                arguments['date'],    
                                arguments['title'],   
                                arguments['conference'], 
                                arguments['author list'],
                                        cursor)
                connection.commit()
            print("nieotwartowywanie")
        else:
            if not (cursor is None): 
                cursor.close()
            return

main()
