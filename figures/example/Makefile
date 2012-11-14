TARGETS = transitiongraph.pdf

all: $(TARGETS)
	@echo > /dev/null

transitiongraph.pdf: gentransitiongraph.py transitiongraph.txt
	./$< transitiongraph.txt

clean:
	@rm -f $(TARGETS)

.PHONY: clean all
