DOC_SERVER := NA

REGISTRY  := NA
IMAGE_NAME := simplelog
IMAGE_NS := NA

PROJ_VERSION := $(shell git describe --always)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)


.PHONY: all coverage docs autopep tests help

all: autopep coverage docs


help:
	@echo
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  docs         to make standalone HTML files (in docs/build)"
	@echo "  reqs         to generate the pip requirements file in etc/"
	@echo "  autopep      to fix coding style in the project"
	@echo "  tests        to run project's tests (actually parsers)"
	@echo "  coverage     to run coverage against the tests"
	@echo "  help         to print this message..."
	@echo

docs:
	pandoc --from=markdown --to=rst --output=${CURDIR}/docs/source/README.rst README.md
	@(cd "$(CURDIR)/docs" && sphinx-apidoc -o ./source "$(CURDIR)/$(IMAGE_NAME)" -f && make html)

autopep:
	autopep8  --max-line-length 120 -r -i -j 2 "$(CURDIR)/${IMAGE_NAME}" -v -aaa

reqs:
	-@python3 -m pipreqs.pipreqs --savepath "$(CURDIR)/requirements.txt" "$(CURDIR)"


coverage:
	coverage erase
	coverage run --source="$(CURDIR)/${IMAGE_NAME}" ./test.py
	coverage report
	-rm -r "$(CURDIR)/docs/source/_static/coverage" 2> /dev/null
	coverage html -d "$(CURDIR)/docs/source/_static/coverage"

tests:
	"$(CURDIR)/test.py"


# docker: docker_build docker_tag docker_push
#
# docker_clean:
# 	-@docker rmi ${IMAGE_NS}/${IMAGE_NAME}:${PROJ_VERSION} ${REGISTRY}/${IMAGE_NS}/${IMAGE_NAME}:${PROJ_VERSION}
# 	-@docker rmi ${IMAGE_NS}/${IMAGE_NAME}:latest ${REGISTRY}/${IMAGE_NS}/${IMAGE_NAME}:latest
#
# docker_build:
# 	docker build -t ${IMAGE_NS}/${IMAGE_NAME}:${PROJ_VERSION} -t ${IMAGE_NS}/${IMAGE_NAME}:latest .
#
# docker_tag:
# 	docker tag ${IMAGE_NS}/${IMAGE_NAME}:${PROJ_VERSION} ${REGISTRY}/${IMAGE_NS}/${IMAGE_NAME}:${PROJ_VERSION}
# 	docker tag ${IMAGE_NS}/${IMAGE_NAME}:latest ${REGISTRY}/${IMAGE_NS}/${IMAGE_NAME}:latest
#
# docker_push:
# 	docker push ${REGISTRY}/${IMAGE_NS}/${IMAGE_NAME}:latest
# 	docker push ${REGISTRY}/${IMAGE_NS}/${IMAGE_NAME}:${PROJ_VERSION}
#
# docker_gc:
# 	-docker rm -v `docker ps --filter status=exited -q 2>/dev/null` 2>/dev/null
# 	-docker rmi `docker images --filter dangling=true -q 2>/dev/null` 2>/dev/null
