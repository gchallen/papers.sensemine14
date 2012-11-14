TARGETS = example template

all: $(TARGETS)
	@echo > /dev/null

example:
	@cd example ; make

template:
	@cd template ; make

clean:
	@cd example ; make clean
	@cd template ; make clean

.PHONY: clean all example template
