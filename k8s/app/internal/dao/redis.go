package dao

import (
	"github.com/gomodule/redigo/redis"
	"os"
)

var c redis.Conn

func InitRedisConn() {
	conn, err := redis.DialURL(os.Getenv("REDIS_URL"))
	if err != nil {
		// handle connection error
		panic(err)
	}
	c = conn
}

func GetRedisC() redis.Conn {
	if c == nil {
		// TODO
	}
	return c
}
