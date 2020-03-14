DOC_SERVER := NA

REGISTRY  := NA
IMAGE_NAME := lazylog
IMAGE_NS := NA

PROJ_VERSION := $(shell git describe --always --match 'v[0-9]*')
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)


.PHONY: all coverage docs autopep tests help dist

all: autopep coverage docs


help:
	@echo
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  docs         to make standalone HTML files (in docs/build)"
	@echo "  reqs         to generate the pip requirements file in etc/"
	@echo "  black        to fix formatting"
	@echo "  autopep      to fix coding style in the project"
	@echo "  tests        to run project's tests (actually parsers)"
	@echo "  coverage     to run coverage against the tests"
	@echo "  dist         to push a new package to pypi (live)"
	@echo "  test_dist    to push a new package to test.pypi (test)"
	@echo "  distclean    to bring the folder in git-clone state"
	@echo "  help         to print this message..."
	@echo

docs:
	pandoc --from=markdown --to=rst --output=${CURDIR}/docs/source/README.rst README.md
	@(cd "$(CURDIR)/docs" && sphinx-apidoc -o ./source "$(CURDIR)/$(IMAGE_NAME)" -f && make html)

autopep:
	autopep8 --max-line-length 120 -r -i -j 2 "$(CURDIR)/${IMAGE_NAME}" "$(CURDIR)/tests" -v -aaa

black:
	black "$(CURDIR)/${IMAGE_NAME}" "$(CURDIR)/tests"

reqs:
	-@python3 -m pipreqs.pipreqs --savepath "$(CURDIR)/requirements.txt" "$(CURDIR)"


coverage:
	coverage erase
	coverage run --source="$(CURDIR)/${IMAGE_NAME}" ./test.py
	coverage report
	-rm -r "$(CURDIR)/docs/source/_static/coverage" 2> /dev/null
	coverage html -d "$(CURDIR)/docs/source/_static/coverage"

tests:
	chmod +x "$(CURDIR)/test.py"
	"$(CURDIR)/test.py"

dist:
	-@rm -r ./dist ./*.egg-info ./build
	@echo ${PROJ_VERSION} > $(CURDIR)/VERSION
	python setup.py sdist
	@rm $(CURDIR)/VERSION
	twine upload dist/*

test_dist:
	-@rm -r ./dist ./*.egg-info ./build
	@echo ${PROJ_VERSION} > $(CURDIR)/VERSION
	python setup.py bdist_wheel
	@rm $(CURDIR)/VERSION
	twine upload -r pypitest dist/*

distclean:
	-@rm -r ./dist ./*.egg-info ./build ./docs/build ./.coverage ./docs/source/_static/coverage
