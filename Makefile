INSTALL_DIR=/opt/research
VENV_DIR=venv
BIN=/usr/local/bin

PEEK=rspeek
FLIP=rsflip
READD=rsreadd
FINDD=rsfindd
QPQT=qpqt
PDSQL=pdsql

build: *
	rm -rf ./env
	conda create --yes -p ./env python=3.6 nltk numpy pandas cython llvmlite numba thriftpy=0.3.9
	./env/bin/python setup.py install

.PHONY: install
install:
	mkdir -p $(INSTALL_DIR)
	cp -r env/* $(INSTALL_DIR)
	cp bin/* $(INSTALL_DIR)/bin
	# rspeek
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/peek.py \$$@" > $(BIN)/$(PEEK)
	chmod a+x $(BIN)/$(PEEK)
	# rsflip
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/flip.py \$$@" > $(BIN)/$(FLIP)
	chmod a+x $(BIN)/$(FLIP)
	# rsreadd
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/readd.py \$$@" > $(BIN)/$(READD)
	chmod a+x $(BIN)/$(READD)
	# rsreadd
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/findd.py \$$@" > $(BIN)/$(FINDD)
	chmod a+x $(BIN)/$(FINDD)
	# qpqt
	echo "$(INSTALL_DIR)/bin/python $(INSTALL_DIR)/bin/qpqt.py \$$@" > $(BIN)/$(QPQT)
	chmod a+x $(BIN)/$(QPQT)
	# pdsql
	echo "#!$(INSTALL_DIR)/bin/python" > $(BIN)/$(PDSQL)
	cat $(INSTALL_DIR)/bin/pdsql.py >> $(BIN)/$(PDSQL)
	chmod a+x $(BIN)/$(PDSQL)

.PHONY: uninstall
uninstall:
	rm -rf $(INSTALL_DIR)
	rm -f $(BIN)/$(PEEK) $(BIN)/$(FLIP) $(BIN)/$(READD) $(BIN)/$(FINDD) $(BIN)/$(QPQT) $(BIN)/$(PDSQL)
	
.PHONY: clean
clean:
	rm -rf env build ReSearch.egg-info
