TARGETS = simple.pdf

all: $(TARGETS)
	@echo > /dev/null

simple.dat: $(DATA) processsimple.py
	./$< $(DATA)

simple.pdf: simple.dat gensimple.py
	./$<

clean:
	@rm -f $(TARGETS)

.PHONY: clean all
