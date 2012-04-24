DESTDIR = 
PREFIX = /usr/local
PYDIR = python2.7
PYSITELIB = $(PREFIX)/lib/$(PYDIR)/site-packages

all:
	echo "Nothing to do"

install:
	mkdir -p $(DESTDIR)/$(PYSITELIB)/videoconvert
	mkdir -p $(DESTDIR)/$(PREFIX)/bin
	install -m0644 *py $(DESTDIR)/$(PYSITELIB)/videoconvert/
	install -m0755 videoconvert $(DESTDIR)/$(PREFIX)/bin/
