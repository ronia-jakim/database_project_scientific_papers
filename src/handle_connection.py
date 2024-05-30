import psycopg2 as psql

def open_connection(hst, db, login, psw):
    try:
        connection = psql.connect(database=db, user=login, password=psw, host=hst)
        cursor = connection.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS institution (
                        id              varchar(40),
                        PRIMARY KEY(id)
                    );
                        """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS smart_guys (
                        id              varchar(40),
                        institution_id  varchar(40) NOT NULL,
                        PRIMARY KEY(id)
                    );
                       """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS conference (
                        id              varchar(40),
                        name            varchar(40),
                        current_points  integer NOT NULL,
                        PRIMARY KEY(id)
                    );
                       """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS conference_points (
                        conf_id         varchar(40) NOT NULL,
                        date_of_change  varchar(40) NOT NULL,
                        current_points  integer,
                    );
                       """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS paper (
                        auth_id         varchar(40) NOT NULL,
                        inst_id         varchar(40) NOT NULL,
                        conference_id   varchar(40) NOT NULL,
                        public_date     varchar(40) NOT NULL,
                        title           varchar(40)
                    );
                       """)
        connection.commit()

        return (cursor, connection)
    except: 
        print('{ "status" : "ERROR: could not open the database" }')
        return None

