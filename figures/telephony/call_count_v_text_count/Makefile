TARGETS = graph.pdf

all: $(TARGETS)
	@echo > /dev/null

graph.pdf: graph.py $(MOBISYS13_DATA)/telephony.dat
	./graph.py

clean:
	@rm -f $(TARGETS)

.PHONY: clean all
