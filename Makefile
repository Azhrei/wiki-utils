# Just boilerplate so far -- not ready for prime time.

all: i18n.properties

wiki-has.txt:
	./1-wiki-getfnnames.py > _tmp && mv _tmp wiki-has.txt

wiki.rptools.info/: wiki-has.txt
	./2-get-wiki-pages.sh

processed/: wiki.rptools.info/
	./3-extract-mw-content.sh

processed.txt: processed/
	./4-generate-macro-list.pl > _tmp && mv _tmp processed.txt

i18n.properties: processed.txt
	./5-create-properties.sh > _tmp && mv _tmp i18n.properties
