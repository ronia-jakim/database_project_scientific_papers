import psycopg2 as psql
import json
import math

def list_institutions(parsed, cursor, connection):
    arguments = parsed['institution']
    start_date = arguments['start_date']
    end_date = arguments['end_date']

    try: 
        cursor.execute("""
                SELECT * FROM list_inst_points(DATE %s, DATE %s)
            """, (start_date, end_date))
        inst_listed = cursor.fetchall()

        inst_dic = {}

        # new_points = 0
        for ret in inst_listed:
            new_points = 0
            try:
                conf_points = float(ret[1]) 
                if conf_points >= 100:
                    new_points = conf_points
                elif conf_points == 70: 
                    new_points = conf_points * math.sqrt(float(ret[4]) / float(ret[3]) )
                else: 
                    new_points = conf_points * float(ret[4]) / float(ret[3])
            except:
                new_points = 0

            if ret[2] in inst_dic:
                inst_dic[ret[2]] += new_points
            else:
                inst_dic[ret[2]] = new_points

        print('{ "status": "OK", "data": [ ')
        for w in sorted(inst_dic, key=inst_dic.get, reverse = True):
            print(' { ')
            print(f''' "institution": "{w}",''', ' "number of points": "{:.4f}" '.format(inst_dic[w]))
            print(' },')
        print(' ] }')

    except:
        print('{ "status": "ERROR" }')
        return

def list_authors(parsed, cursor, connection):
    arguments = parsed['author']
    start_date = arguments['start_date']
    end_date = arguments['end_date']

    try:
        cursor.execute("""
                SELECT * FROM list_author_points(DATE %s, DATE %s)
            """, (start_date, end_date))
        try:
            authors_listed = cursor.fetchall()

           
            print('{ "status": "OK", "data": [ ')
            for ret in authors_listed:
                    print('{ ')
                    print(f''' "author": "{ret[0]}", "number of points": "{ret[1]}" ''')
                    print('}, ')
            print(' ] }')
        except:
            print('{ "status": "OK", "data": [] }')


    except:
        print('{ "status": "ERROR" }')
        return 
