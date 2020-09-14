LOAD DATA LOCAL INFILE '/home/eric/PycharmProjects/ir_standings_analyzer/Generated CSVs/RTP_Points_Table.csv' INTO TABLE Races_Chart
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;