--CREATE USER weles WITH ENCRYPTED PASSWORD 'welesik';

-- właśnicicel bazy dancyh w projekcie to weles :3
--CREATE DATABASE database_project_scientists
--  WITH OWNER = 'weles';

-- tabelka z instytucjami, nazwa może być pusta, bo Pan nic o takowej nie pisze
CREATE TABLE IF NOT EXISTS institutions (
  id    varchar(40) PRIMARY KEY, 
  name  varchar(40)
);

-- tabelka dla mądrych ludzi, id i institution id są ważne
CREATE TABLE IF NOT EXISTS smart_guys (
  id              varchar(40) PRIMARY KEY, 
--  institution_id  varchar(40) REFERENCES institutions (id),
  name            varchar(40), 
  surname         varchar(40)
);

-- od kiedy ziomek był w jakiej instytucji
CREATE TABLE IF NOT EXISTS guy_aff (
  guy_id      varchar(40) REFERENCES smart_guys (id), 
  inst_id     varchar(40) REFERENCES institutions (id), 
  date_from   date NOT NULL
);

-- tabelka dla konferencji, nazwa i current_poitns mogą być puste
CREATE TABLE IF NOT EXISTS conference (
  id              varchar(40) PRIMARY KEY, 
  name            varchar(40), 
  current_points  integer 
);

-- tutaj z kolei punkty nie mogą być puste, tak samo data rozpoczęcia
-- sprawdzam, czy data zakończenia tej punktacji jest po dacie rozpoczęcia
CREATE TABLE IF NOT EXISTS conference_points (
  conference_id  varchar(40) REFERENCES conference(id), 
  points         integer NOT NULL, 
  date_of_change date NOT NULL
);

CREATE TABLE IF NOT EXISTS paper (
  auth_id           varchar(40) REFERENCES smart_guys(id), 
  institution_id    varchar(40) REFERENCES institutions(id), 
  conference_id     varchar(40) REFERENCES conference(id), 
  publication_date  date NOT NULL, 
  title             varchar(80)
);

-- tabelka dla użytkowników aplikacji, od razu sprawdza sekrecik
CREATE TABLE IF NOT EXISTS users (
  secret  varchar(40) NOT NULL, 
  login   varchar(40) PRIMARY KEY,
  passwd  varchar(40) NOT NULL,
  CONSTRAINT secret_constr CHECK (secret = 'd8512346fbc5bb7a325ca4')
);


-- =============================================================== -- 
--             TUTAJ BĘDĄ FUNKCJE KTORE WYZWOLE POTEM              --
-- =============================================================== -- 

CREATE OR REPLACE FUNCTION on_paper_insert() RETURNS TRIGGER
AS $X$
DECLARE 
  curr_inst varchar(40);
BEGIN
  -- jeśli ziomek jeszcze nie istniał, to go wstawiam
  INSERT INTO smart_guys VALUES (NEW.auth_id, NULL, NULL)
  ON CONFLICT DO NOTHING;

  -- sprawdzam, czy instytucja istnieje
  INSERT INTO institutions VALUES (NEW.institution_id)
  ON CONFLICT DO NOTHING;

  -- sprawdzam, jaką instytucję ma teraz ziomek podpientą
  SELECT inst_id FROM guy_aff INTO curr_inst
  WHERE 
    guy_id = NEW.auth_id
    AND date_from < NEW.publication_date 
    AND guy_id NOT IN (
      SELECT guy_id FROM guy_aff 
      WHERE date_from >= NEW.publication_date
    )
  LIMIT 1;

  --jeszcze ziomka nie było lub zmienił instytucję
  IF curr_inst IS NULL OR curr_inst != NEW.institution_id THEN
    INSERT INTO guy_aff VALUES (NEW.auth_id, NEW.institution_id, NEW.publication_date);
  END IF;

  RETURN NEW;
END $X$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION list_author_points (
  start_date date, 
  end_date date
) RETURNS table (
  auth_id   varchar(40), 
  point_amt bigint
)
LANGUAGE plpgsql 
AS $X$
BEGIN 
  RETURN QUERY 
  SELECT paper.auth_id, SUM(points) 
  FROM paper JOIN conference_points ON paper.conference_id = conference_points.conference_id
  WHERE 
    paper.publication_date > conference_points.date_of_change 
    -- ta zmiana jest najmłodsza spośród zmian przed publikacją papera
    AND conference_points.date_of_change IN ( 
      SELECT c1.date_of_change FROM 
      conference_points c1
      WHERE 
        c1.conference_id = paper.conference_id
        AND c1.date_of_change < paper.publication_date 
      ORDER BY 1 DESC
      LIMIT 1
    )
  GROUP BY paper.auth_id
  ORDER BY 2;
END; 
$X$;

CREATE OR REPLACE FUNCTION list_inst_points (
  start_date date, 
  end_date date
) RETURNS table (
  title varchar(80),
  points integer,
  institution_id   varchar(40), 
  all_authors bigint,
  from_this_inst bigint
)
LANGUAGE plpgsql 
AS $X$
BEGIN 
  RETURN QUERY

  WITH paper_points AS (
    SELECT paper.title, cp.points
    FROM paper JOIN conference_points cp ON paper.conference_id = cp.conference_id
    WHERE 
      paper.publication_date > cp.date_of_change 
      -- ta zmiana jest najmłodsza spośród zmian przed publikacją papera
      AND cp.date_of_change IN ( 
        SELECT c1.date_of_change FROM 
        conference_points c1
        WHERE 
          c1.conference_id = paper.conference_id
          AND c1.date_of_change < paper.publication_date 
        ORDER BY 1 DESC
        LIMIT 1
      )
  ),
  inst_nr AS (
    SELECT
      paper.institution_id, 
      COUNT(auth_id) AS cnt, 
      paper.title
    FROM paper 
    GROUP BY paper.institution_id, paper.title
  ), 
  auth_nr AS (
    SELECT paper.title, COUNT(auth_id) AS cnt
    FROM paper 
    GROUP BY paper.title
  )

  SELECT DISTINCT paper_points.title, paper_points.points, inst_nr.institution_id, auth_nr.cnt, inst_nr.cnt
  FROM auth_nr 
    JOIN inst_nr ON auth_nr.title = inst_nr.title
    JOIN paper_points ON auth_nr.title = paper_points.title;
END; 
$X$;

-- =============================================================== -- 
--                   TUTAJ SIEDZĄ SOBIE TRIGGERY                   --
-- =============================================================== -- 


CREATE TRIGGER paper_inserted BEFORE INSERT ON paper FOR EACH ROW EXECUTE PROCEDURE on_paper_insert();

INSERT INTO conference VALUES ( 
  'madra konferencja', 
  'madra nazwa konferencji', 
  69
);

INSERT INTO conference_points VALUES ( 
  'madra konferencja', 
  30,
  DATE '2010-01-01'
);

INSERT INTO conference_points VALUES ( 
  'madra konferencja', 
  20,
  DATE '2020-01-01'
);


INSERT INTO conference_points VALUES ( 
  'madra konferencja', 
  69,
  DATE '2023-12-13'
);

INSERT INTO paper VALUES ( 
  'weles',
  'kotomania', 
  'madra konferencja', 
  DATE '2022-10-02', 
  'Welesik jest czarnym psem, esej na 100 stron'
);

INSERT INTO paper VALUES ( 
  'welesik',
  'kotomania', 
  'madra konferencja', 
  DATE '2022-10-02', 
  'Welesik jest czarnym psem, esej na 100 stron'
);

INSERT INTO paper VALUES ( 
  'kycia',
  'grubaskowo', 
  'madra konferencja', 
  DATE '2022-10-02', 
  'Welesik jest czarnym psem, esej na 100 stron'
);

INSERT INTO paper VALUES ( 
  'kycia',
  'grubaskowo', 
  'madra konferencja', 
  DATE '2024-01-01', 
  'Welesik jest czarnym psem'
);

INSERT INTO paper VALUES ( 
  'weles',
  'kotomania', 
  'madra konferencja', 
  DATE '2022-10-02', 
  'Welesik'
);

INSERT INTO paper VALUES ( 
  'welesik',
  'kotomania', 
  'madra konferencja', 
  DATE '2022-10-02', 
  'Welesik'
);

INSERT INTO paper VALUES ( 
  'kycia',
  'grubaskowo', 
  'madra konferencja', 
  DATE '2022-10-02', 
  'Welesik'
);

SELECT * FROM paper;
SELECT * FROM smart_guys;
SELECT * FROM guy_aff;
SELECT * FROM institutions;
SELECT * FROM conference;
SELECT * FROM conference_points;

SELECT * FROM list_author_points(DATE '2019-03-03', DATE '2023-01-01');

SELECT * FROM list_inst_points(DATE '2019-03-03', DATE '2023-01-01');
