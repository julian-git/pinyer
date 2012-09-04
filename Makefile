all: sql/all doc/all tests/all

sql/all:
	$(MAKE) -C sql

doc/all:
	$(MAKE) -C doc

tests/all:
	$(MAKE) -C tests

clean:
	rm -f *~ gurobi.log
