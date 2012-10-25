PYTHONDIR = ../../../python

all: pinya.solved.svg 

pinya.solved.svg: pinya.svg pinya.complete.lp $(PYTHONDIR)/solve_ip.py 
	python $(PYTHONDIR)/solve_ip.py

pinya.svg: pinya.xml $(PYTHONDIR)/xml_to_svg.py
	python $(PYTHONDIR)/xml_to_svg.py

pinya.complete.lp: pinya.lp $(PYTHONDIR)/complete_lp.py
	python $(PYTHONDIR)/complete_lp.py

pinya.lp: pinya.xml $(PYTHONDIR)/xml_to_lp.py $(PYTHONDIR)/util/ineq.py 
	python $(PYTHONDIR)/xml_to_lp.py

$(PYTHONDIR)/util/ineq.py:

