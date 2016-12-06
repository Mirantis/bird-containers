default: help
all: help

TMP:=$(shell pwd)/tmp-$(shell date "+%Y%m%d-%H%M%S")
CURL=curl -sSf
#GOLANG=golang:1.7.3-alpine
GOLANG=xenolog/golang #:1.7.3

CONTAINER="xenolog/k8s-rr-container"
CONFD_VERSION=0.12.1
CONFD_SRC_URL=https://codeload.github.com/bacongobbler/confd/zip/v$(CONFD_VERSION)
CONFD_SRC_DIR=$(TMP)/confd-$(CONFD_VERSION)
CONFD_BIN=$(CONFD_SRC_DIR)/bin/confd


tmp:
	mkdir -p $(TMP)

.PHONY: clean
clean:
	rm -rf $(TMP)

$(CONFD_SRC_DIR): tmp
	(cd $(TMP) && curl -o confd-$(CONFD_VERSION).zip $(CONFD_SRC_URL))
	(cd $(TMP) && unzip -q -o confd-$(CONFD_VERSION).zip)

.PHONY: build-confd
build-confd: $(CONFD_SRC_DIR) tmp
	(cd $(CONFD_SRC_DIR) && docker build -t confd_builder -f Dockerfile.build.alpine .)
	(cd $(CONFD_SRC_DIR) && docker run -ti --rm -v `pwd`:/app confd_builder ./build)
	#clean

.PHONY: list-tags
list-tags:
	docker images | grep xenolog/k8s-rr-container
.PHONY: help
## Display this help text
help:
	@echo "Use make with following parameter:"
	@echo "  biuld-container   --  build container"
	@echo "  upload-container  --  upload container to dockerhub"
	@echo "  list-tags         --  list tags of existing containers"