.PHONY: test test-build

# Do not pass in user flags to build tests.
unexport PYTHON_CFLAGS
unexport PYTHON_CONFIGURE_OPTS

test: bats
	PATH="./bats/bin:$$PATH" test/run
	cd plugins/python-build && $(PWD)/bats/bin/bats $${CI:+--tap} test

PYTHON_BUILD_ROOT := $(CURDIR)/plugins/python-build
PYTHON_BUILD_OPTS ?= --verbose
PYTHON_BUILD_VERSION ?= 3.8-dev
PYTHON_BUILD_TEST_PREFIX ?= $(PYTHON_BUILD_ROOT)/test/build/tmp/dist

test-build:
	$(RM) -r $(PYTHON_BUILD_TEST_PREFIX)
	$(PYTHON_BUILD_ROOT)/bin/python-build $(PYTHON_BUILD_OPTS) $(PYTHON_BUILD_VERSION) $(PYTHON_BUILD_TEST_PREFIX)
	[ -e $(PYTHON_BUILD_TEST_PREFIX)/bin/python ]
	$(PYTHON_BUILD_TEST_PREFIX)/bin/python -V
	[ -e $(PYTHON_BUILD_TEST_PREFIX)/bin/pip ]
	$(PYTHON_BUILD_TEST_PREFIX)/bin/pip -V

bats:
	git clone --depth 1 https://github.com/bats-core/bats-core.git bats

# tgd
install_dep:
	sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

install:
	./config_modify.py -a add --json config_zshenv.json

uninstall:
	./config_modify.py -a delete --json config_zshenv.json
