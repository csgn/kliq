FROM golang:1.22.4-alpine AS builder

RUN apk -U add ca-certificates
RUN apk update && apk upgrade && apk add pkgconf git bash build-base sudo

WORKDIR /dependencies
RUN git clone https://github.com/edenhill/librdkafka.git && cd librdkafka && ./configure --prefix /usr && make && make install

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
RUN CGO_ENABLED=1 GOOS=linux GOARACH=amd64 GO111MODULE=on go build -tags musl -ldflags "-extldflags -static" -v -o build/kliq-collect

FROM alpine:latest
RUN apk add curl
WORKDIR /root
COPY --from=builder /app/build/kliq-collect .

ENTRYPOINT ["/root/kliq-collect"]
