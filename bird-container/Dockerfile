FROM alpine:3.4
MAINTAINER Sergey Vasilenko <svasilenko@mirantis.com>

# Set the minimum Docker API version required for libnetwork.
ENV DOCKER_API_VERSION 1.21
EXPOSE 179 180

RUN apk --no-cache add wget ca-certificates libgcc \
  && wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://raw.githubusercontent.com/sgerrand/alpine-pkg-glibc/master/sgerrand.rsa.pub \
  && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-2.23-r3.apk \
  && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-bin-2.23-r3.apk \
  && apk add glibc-2.23-r3.apk glibc-bin-2.23-r3.apk \
  && /usr/glibc-compat/sbin/ldconfig /lib /usr/glibc/usr/lib \
  && apk del wget \
  && rm -f glibc-2.23-r3.apk glibc-bin-2.23-r3.apk \
  && apk add --no-cache --repository "http://alpine.gliderlabs.com/alpine/edge/community" runit \
  && apk add --no-cache ip6tables ipset iputils iproute2 conntrack-tools \
  && date > /buildinfo.txt

# Copy in the filesystem - this contains confd, bird configs
COPY root/ /

CMD ["start_runit"]