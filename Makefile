all: sql/all doc/all www/pinyas/cvg.3de9f/all # tests/all www/pinyas/all 

sql/all:
	$(MAKE) -C sql

doc/all:
	$(MAKE) -C doc

tests/all:
	$(MAKE) -C tests

www/pinyas/cvg.3de9f/all:
	$(MAKE) -C www/pinyas/cvg.3de9f

clean:
	rm -f *~ gurobi.log
	$(MAKE) -C python clean
	$(MAKE) -C sql clean
	$(MAKE) -C doc clean
	$(MAKE) -C www/pinyas/cvg.3de9f clean
