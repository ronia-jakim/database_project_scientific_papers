import psycopg2 as psql
import json

def add_article(date, title, conference, author_list, cursor):
    auth_nr = len(author_list)

    for el in author_list:
        auth = el['author']
        inst = el['institution']

        # sprawdzam, czy taki user istnieje
        cursor.execute("""
                          SELECT * FROM smart_guys 
                          WHERE id = %s
                          """,
                          [auth])
        res = cursor.fetchall()
        
        if res == []:
            # jesli institution jeszcze nie ma, to dodaj
            cursor.execute("""
                           INSERT INTO institution VALUES
                           (%s) ON CONFLICT DO NOTHING
                           """, [inst])
            # dodaj naukowca do tablicy smart_guys
            cursor.execute("""
                           INSERT INTO smart_guys VALUES
                           (%s, %s)
                           """, (auth, inst))
        elif res[0][1] != inst:
            # sprawdzam, czy praca nie jest w innym institution 
            # niz dotychcas smart guy byl przypisany
            # jest jest rozna, to podmieniam institution_id
            cursor.execute("""
                           UPDATE smart_guys
                           SET institution_id = %s
                           WHERE id = %s
                           """, (inst, auth))

        cursor.execute("""
                       INSERT INTO 
                       paper (auth_id, inst_id, conference_id, public_date, title)
                       VALUES (%s, %s, %s, %s, %s)
                       """,
                       (auth, inst, conference, date, title))

def change_points(date, points_list, cursor):
    for el in points_list: 
        conf = el['conference'], 
        points = el['points']
        
        # sprawdzam, czy taka konferencja juz istnieje
        cursor.execute("""
                        SELECT * FROM conference
                        WHERE id = %s
                       """, [conf])
        res = cursor.fetchone()
        
        if res is None: 
            cursor.execute("""
                           INSERT INTO conference (id, current_points)
                           VALUES (%s, %s)
                           """, (conf, int(points)) )
            cursor.execute("""
                           INSERT INTO conference_points (conf_id, date_of_change, current_points)
                           VALUES (%s, %s, %s)
                           """, (conf, date, int(points)))
        elif res[3] != points:
            # jesli konferencja juz istnieje, ale teraz mamy nowa ilosc punktow
            cursor.execute("""
                           UPDATE conference
                           SET current_points = %s, 
                           WHERE id = %s
                           """, (int(points), conf))
            cursor.execute("""
                           UPDATE conference
                           SET current_points = %s, 
                           WHERE conf_id = %s
                           """, (int(points), conf))

