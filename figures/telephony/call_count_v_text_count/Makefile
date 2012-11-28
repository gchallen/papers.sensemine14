TARGETS = graph.pdf

all: $(TARGETS)
	@echo > /dev/null

data.dat: process.py $(MOBISYS_DATA)
	./process.py $(MOBISYS_DATA)

graph.pdf: graph.py data.dat
	./graph.py data.dat

clean:
	@rm -f data.dat
	@rm -f $(TARGETS)

.PHONY: clean all
