import psycopg2 as psql
import json

def add_article(login, password, date, title, conference, author_list, cursor):
    print(author_list)
    for el in author_list:
        auth = el['author']
        inst = el['institution']

