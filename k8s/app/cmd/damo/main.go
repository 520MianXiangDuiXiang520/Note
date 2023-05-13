package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

//func init() {
//	dao.InitRedisConn()
//	err := dao.InitMongoDB(context.TODO(), os.Getenv("MGO_URL"), "test")
//	if err != nil {
//		panic(err)
//	}
//}

func main() {
    engine := gin.Default()
    engine.GET("/version", func(ctx *gin.Context) {
        ctx.JSON(http.StatusOK, map[string]string{"version": "v1"})
    })
    //engine.GET("/redis", func(ctx *gin.Context) {
    //	resp := dao.CheckRedis()
    //	ctx.JSON(http.StatusOK, map[string]string{"redis": resp})
    //})
    //engine.GET("/mgo", func(ctx *gin.Context) {
    //	resp := dao.CheckMgo()
    //	ctx.JSON(http.StatusOK, map[string]string{"redis": resp})
    //})
    engine.Run(":8080")
}
