PREFIX = /usr/local
PYDIR = python2.7
PYSITELIB = $(PREFIX)/lib/$(PYDIR)/site-packages

all:
	echo "Nothing to do"

install:
	mkdir -p $(PYSITELIB)/videoconvert
	mkdir -p $(PREFIX)/bin
	install -m0644 *py $(PYSITELIB)/videoconvert/
	install -m0755 videoconvert $(PREFIX)/bin/
