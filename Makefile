all: pinyol-db.png

pinyol-db.png: pinyol.sql
	sqlt-diagram -d=MySQL pinyol.sql -o pinyol-db.png --color
