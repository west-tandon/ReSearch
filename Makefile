INSTALL_DIR=/opt/research
VENV_DIR=venv
BIN=/usr/local/bin

PEEK=rspeek
FLIP=rsflip

build: *
	virtualenv -p /usr/bin/python3 $(VENV_DIR)
	$(VENV_DIR)/bin/python setup.py install

.PHONY: install
install:
	mkdir -p $(INSTALL_DIR)
	cp -r $(VENV_DIR)/* $(INSTALL_DIR)
	cp bin/* $(INSTALL_DIR)/bin
	# rspeek
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/peek.py \$$@" > $(BIN)/$(PEEK)
	chmod a+x $(BIN)/$(PEEK)
	# rsflip
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/flip.py \$$@" > $(BIN)/$(FLIP)
	chmod a+x $(BIN)/$(FLIP)

.PHONY: uninstall
uninstall:
	rm -rf $(INSTALL_DIR)
	rm -f $(BIN)/$(PEEK) $(BIN)/$(FLIP)
	
.PHONY: clean
clean:
	rm -rf venv build ReSearch.egg-info
