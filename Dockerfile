FROM alpine
LABEL vendor="ACME Incorporated" \
      com.example.is-beta \
      com.example.version=1 \
      com.example.release-date="2015-02-12"
RUN apk add --update bash && rm -rf /var/cache/apk/*
CMD ["/bin/bash"]
