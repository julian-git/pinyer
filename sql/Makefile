all: pinyer-db.png database-definition.up-to-date database-entries.up-to-date database-dummy-entries.up-to-date

pinyer-db.png: pinyer.sql
	sqlt-diagram -d=MySQL pinyer.sql -o pinyer-db.png --color

database-definition.up-to-date: pinyer.sql init-cvg.sql 
	mysql --default-character-set=utf8 -u pinyer -e "drop database pinyer; create database pinyer; use pinyer; source pinyer.sql; source init-cvg.sql;" 
	touch database-definition.up-to-date

database-entries.up-to-date: database-definition.up-to-date ../python/util/draw_casteller.py
	python ../python/util/draw_casteller.py
	touch database-entries.up-to-date

database-dummy-entries.up-to-date: pinyer_dummy_entries.sql
	mysql --default-character-set=utf8 -u pinyer -e "use pinyer; source pinyer_dummy_entries.sql;"
	touch database-dummy-entries.up-to-date

clean:
	rm -f *~ *#
