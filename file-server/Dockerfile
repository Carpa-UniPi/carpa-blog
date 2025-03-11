FROM golang:1.23-alpine

RUN apk add git curl
RUN git clone https://github.com/mayth/go-simple-upload-server /home/server
WORKDIR /home/server
RUN go mod download
RUN mkdir -p /usr/local/bin/
RUN go build -v -o /usr/local/bin/ ./...

COPY --chown=nonroot:nonroot ./health-check /root/health-check

ENTRYPOINT ["/usr/local/bin/go-simple-upload-server"]