all: sql/all doc/all

sql/all:
	$(MAKE) -C sql

doc/all:
	$(MAKE) -C doc

test: all
	python run_unit_tests.py

clean:
	rm -f *~ gurobi.log
