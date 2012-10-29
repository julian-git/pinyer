all: sql/all doc/all # tests/all www/pinyas/all 

sql/all:
	$(MAKE) -C sql

doc/all:
	$(MAKE) -C doc

tests/all:
	$(MAKE) -C tests

clean:
	rm -f *~ gurobi.log
	$(MAKE) -C python clean
	$(MAKE) -C sql clean
	$(MAKE) -C doc clean