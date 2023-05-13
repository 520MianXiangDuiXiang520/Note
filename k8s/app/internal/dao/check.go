package dao

import (
    "context"
    "fmt"
    "github.com/gomodule/redigo/redis"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
    "log"
    "time"
)

func CheckRedis() string {
    _, err := GetRedisC().Do("SET", "hello", time.Now().String())
    if err != nil {
        fmt.Println(err)
        return err.Error()
    }
    s, err := redis.String(GetRedisC().Do("GET", "hello"))
    if err != nil {
        fmt.Println(err)
        return err.Error()
    }
    return s
}

func CheckMgo() string {
    s, err := Mgo().Collection("test").InsertOne(context.TODO(), bson.D{{"name", "Mgo" + time.Now().String()}})
    if err != nil {
        return err.Error()
    }
    opts := options.FindOne().SetSort(bson.D{{"age", 1}})
    var result bson.M
    err = Mgo().Collection("test").FindOne(context.TODO(), bson.D{{"_id", s.InsertedID}}, opts).Decode(&result)
    if err != nil { // ErrNoDocuments means that the filter did not match any documents in     // the collection.
        if err == mongo.ErrNoDocuments {
            return err.Error()
        }
        log.Fatal(err)
    }
    fmt.Printf("%+v \n", result)
    return result["name"].(string)
}
