PYTHONDIR = ../../../python

all: pinya.solved.svg 

pinya.solved.svg: pinya.svg pinya.complete.lp $(PYTHONDIR)/solve_ip.py 
	python $(PYTHONDIR)/solve_ip.py

pinya.svg: pinya.xml $(PYTHONDIR)/xml_to_svg.py
	python $(PYTHONDIR)/xml_to_svg.py

pinya.complete.lp: pinya.lp $(PYTHONDIR)/complete_lp.py
	python $(PYTHONDIR)/complete_lp.py

pinya.lp: pinya.xml $(PYTHONDIR)/xml_to_lp.py $(PYTHONDIR)/util/ineqs.py $(PYTHONDIR)/../sql/database-definition.up-to-date
	python $(PYTHONDIR)/xml_to_lp.py

pinya.xml: $(PYTHONDIR)/create_3de9f.py $(PYTHONDIR)/util/relations.py $(PYTHONDIR)/local_config.py
	python $(PYTHONDIR)/create_3de9f.py
