all: pinyol-db.png database-definition.up-to-date

pinyol-db.png: pinyol.sql
	sqlt-diagram -d=MySQL pinyol.sql -o pinyol-db.png --color

database-definition.up-to-date: pinyol.sql pinyol_setup.sql pinyol_dummy_entries.sql
	mysql -u pinyol -p -e "drop database pinyol; create database pinyol; use pinyol; source pinyol.sql; source pinyol_dummy_entries.sql;" 
	touch database-definition.up-to-date

