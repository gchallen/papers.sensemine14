TARGETS = simple.pdf

all: $(TARGETS)
	@echo > /dev/null

simple.dat: processsimple.py $(DATA)
	./processsimple.py $(DATA)

simple.pdf: gensimple.py simple.dat
	./gensimple.py simple.dat

clean:
	@rm -f simple.dat
	@rm -f $(TARGETS)

.PHONY: clean all
