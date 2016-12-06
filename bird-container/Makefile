default: help
all: help

#TMP:=$(shell pwd)/tmp-$(shell date "+%Y%m%d-%H%M%S")
TMP:=$(shell pwd)/tmp-$(shell date "+%Y%m%d")
CURL=curl -sSf
#GOLANG=golang:1.7.3-alpine
GOLANG=xenolog/golang #:1.7.3

CONTAINER="xenolog/k8s-rr-container"

BUILDER_ALPINE=3.4
BUILDER_FLAG=$(TMP)/.container_ready

CONFD_VERSION=0.12.1
CONFD_SRC_URL=https://codeload.github.com/bacongobbler/confd/zip/v$(CONFD_VERSION)
CONFD_SRC_DIR=$(TMP)/confd-$(CONFD_VERSION)
CONFD_BIN=$(CONFD_SRC_DIR)/bin/confd

BIRD_VERSION=1.6.2
BIRD_SRC_TARBALL=bird-$(BIRD_VERSION).tar.gz
BIRD_SRC_URL=ftp://bird.network.cz/pub/bird/$(BIRD_SRC_TARBALL)
BIRD_SRC_DIR=$(TMP)/bird-$(BIRD_VERSION)
#BIRD_BIN=$(CONFD_SRC_DIR)/bin/confd



tmp:
	mkdir -p $(TMP)

.PHONY: clean
clean:
	rm -rf $(TMP)

$(BUILDER_FLAG): tmp
	(docker build -t kargo-multirack-builder -f Dockerfile-builder .)
	(echo > $(BUILDER_FLAG))

.PHONY: builder
builder: $(BUILDER_FLAG)

$(CONFD_SRC_DIR): tmp
	(cd $(TMP) && curl -o confd-$(CONFD_VERSION).zip $(CONFD_SRC_URL))
	(cd $(TMP) && unzip -q -o confd-$(CONFD_VERSION).zip)

$(CONFD_BIN): $(BUILDER_FLAG) $(CONFD_SRC_DIR)
	(cd $(CONFD_SRC_DIR) && docker run -ti --rm -v `pwd`:/go/src/github.com/kelseyhightower/confd kargo-multirack-builder build_confd.sh)

.PHONY: build-confd
build-confd: $(CONFD_BIN)



$(BIRD_SRC_DIR): tmp
	(cd $(TMP) && curl $(BIRD_SRC_URL) | tar xzf -)

.PHONY: build-bird
build-bird: $(BUILDER_FLAG) $(BIRD_SRC_DIR)
	(cd $(BIRD_SRC_DIR) && ls -la)
	# (cd $(CONFD_SRC_DIR) && docker build -t confd_builder -f Dockerfile.build.alpine .)
	# (cd $(CONFD_SRC_DIR) && docker run -ti --rm -v `pwd`:/app confd_builder ./build)


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