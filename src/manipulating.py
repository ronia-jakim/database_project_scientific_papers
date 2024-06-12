import psycopg2 as psql
import json

def add_article (parsed, cursor, connection):
    arguments = parsed['article']
    
    username = arguments['login']
    passwrd = arguments['password']

    cursor.execute("""
        SELECT *
        FROM users 
        WHERE login = %s AND passwd = %s
    """, (username, passwrd))
    try: 
        cursor.fetchone() 
    except:
        print('{ "status" : "ERROR" }')
        return
    
    for el in arguments['author list']:
        auth = el['author']
        inst = el['institution']

        # jeśli podana konferencja nie istnieje, to tutaj wyrzuci errora strasznego
        try: 
            # bazie jest ustawiony trigger, ktory po wstawieniu do paper robi wazne rzeczy
            cursor.execute("""
               INSERT INTO paper (
                    auth_id, 
                    institution_id, 
                    conference_id, 
                    publication_date, 
                    title
                    ) VALUES (%s, %s, %s, DATE %s, %s)
               """, (  auth, 
                       inst, 
                       arguments['conference'], 
                       arguments['date'], 
                       arguments['title']
                   )
               )

            #zapisuje zmiany
            connection.commit()
        except:
            print('{ "status" : "ERROR" }')
            return
    print('{ "status": "OK" }')


def change_points (parsed, cursor, connection):
    arguments = parsed['points']
    
    username = arguments['login']
    passwrd = arguments['password']

    cursor.execute("""
        SELECT *
        FROM users 
        WHERE login = %s AND passwd = %s
    """, (username, passwrd))
    try: 
        cursor.fetchone() 
    except:
        print('{ "status" : "ERROR" }')
        return
    
    for el in arguments['points_list']:
        conf = el['conference']
        pkts = el['points']

        # jeśli podana konferencja nie istnieje, to tutaj wyrzuci errora strasznego
        try: 
            # bazie jest ustawiony trigger, ktory po wstawieniu do paper robi wazne rzeczy
            cursor.execute("""
               INSERT INTO conference_points (
                    conference_id, 
                    points, 
                    date_of_change
                    ) VALUES (%s, %s, DATE %s)
               """, (
                       conf, 
                       pkts,
                       arguments['date']
                   )
               )

            #zapisuje zmiany
            connection.commit()
            print('{ "status": "OK" }')
        except:
            print('{ "status" : "ERROR" }')
            return
