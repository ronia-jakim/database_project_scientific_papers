SELECT * FROM conference_points;

SELECT * FROM list_inst_points( DATE '1000-01-01', DATE '2024-05-12');

INSERT INTO conference_points VALUES ('madra konferencja', 100, DATE '2024-05-12');
SELECT * FROM list_inst_points( DATE '1000-01-01', DATE '2100-01-01');
