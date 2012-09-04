all: sql/all doc/all

sql/all:
	$(MAKE) -C sql

doc/all:
	$(MAKE) -C doc

test: all
	$(MAKE) -C tests

clean:
	rm -f *~ gurobi.log
