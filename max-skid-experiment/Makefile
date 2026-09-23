AS = as
LD = ld

SETUP_ITERATIONS ?= 3125
SLED_PASSES ?= 2000
BRANCHES_PER_SLED_PASS ?= 64
REPEATED_BRANCHES_TAKEN ?= 0

NAME = branch-sled-setup$(SETUP_ITERATIONS)-passes$(SLED_PASSES)-branches$(BRANCHES_PER_SLED_PASS)-taken$(REPEATED_BRANCHES_TAKEN)
OBJECT = build/$(NAME).o
BINARY = build/$(NAME)

.PHONY: all clean
all: $(BINARY)

$(OBJECT): branch-sled.s
	mkdir -p build
	$(AS) --64 --defsym SETUP_ITERATIONS=$(SETUP_ITERATIONS) \
		--defsym SLED_PASSES=$(SLED_PASSES) \
		--defsym BRANCHES_PER_SLED_PASS=$(BRANCHES_PER_SLED_PASS) \
		--defsym REPEATED_BRANCHES_TAKEN=$(REPEATED_BRANCHES_TAKEN) -o $@ $<

$(BINARY): $(OBJECT)
	$(LD) -o $@ $<

clean:
	rm -rf build
