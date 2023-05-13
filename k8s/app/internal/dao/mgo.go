package dao

import (
	"context"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"time"
)

type MgoDB struct {
	*mongo.Database
}

var _db *MgoDB

func InitMongoDB(ctx context.Context, uri, database string, ops ...*options.DatabaseOptions) error {
	opt := options.Client().ApplyURI(uri)
	opt.SetConnectTimeout(time.Minute * 2)
	opt.SetServerSelectionTimeout(time.Minute)
	client, err := mongo.Connect(ctx, opt)
	if err != nil {
		return err
	}
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		return err
	}
	_db = &MgoDB{client.Database(database, ops...)}
	return nil
}

func Mgo() *MgoDB {
	if _db == nil || _db.Database == nil {
		panic("mongo database uninitialized!")
	}
	return _db
}
