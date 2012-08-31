all: sql/all

sql/all:
	make -C sql

test: all
	python run_unit_tests.py

clean:
	rm -f *~ gurobi.log
