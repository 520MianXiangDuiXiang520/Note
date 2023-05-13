FROM golang:1.18.1 AS demo_base

ENV GOPROXY https://goproxy.cn
ENV GO111MODULE on
ENV GOBIN /go/bin

WORKDIR /app

COPY ./go.mod .
COPY ./go.sum .
RUN go mod download


