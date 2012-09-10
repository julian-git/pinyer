all: pinyer-db.png database-definition.up-to-date

pinyer-db.png: pinyer.sql
	sqlt-diagram -d=MySQL pinyer.sql -o pinyer-db.png --color

database-definition.up-to-date: pinyer.sql pinyer_dummy_entries.sql
	mysql -u pinyer -e "drop database pinyer; create database pinyer; use pinyer; source pinyer.sql; source pinyer_dummy_entries.sql;" 
	touch database-definition.up-to-date

