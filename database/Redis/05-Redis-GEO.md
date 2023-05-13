# GEO

> GEO即地址信息定位，可以用来存储经纬度，计算两地距离，范围计算等。这意味着我们可以使⽤ Redis 来实现美团和饿了么「附近的餐馆」，微信摇一摇等功能了。

<!-- more -->

常用API

1. `GEOADD key logitude latitude member[ logitude1  latitude1 member1...]`: 增加地理位置信息

```shell
127.0.0.1:8100> geoadd cities 12.28 55.41 test
(integer) 1
```

2. `geopos key member [member…]` 获取地理位置信息

```shell
127.0.0.1:8100> geopos cities test
1) 1) "12.27999776601791382"
   2) "55.40999942120450328
```

3. `geodist key member1 member2 [unit]` 获取两个地理位置的距离,unit:m(米),km(千米),mi(英里),ft(尺)

```shell
127.0.0.1:8100> geodist cities test baiying km
"6910.1248"
```

4. georedius key longitude latitude radiusm|km|ft|mi [withcoord] [withdist] [withhash] [COUNT count] [asc|desc] [store key][storedist key]
5. georadiusbymember key member radiusm|km|ft|mi [withcoord] [withdist] [withhash] [COUNT count] [asc|desc] [store key][storedist key]

获取指定位置范围内的地理位置信息集合

* withcoord:返回结果中包含经纬度
* withdist:返回结果中包含距离中心节点位置
* withhash:返回结果中包含geohash
* COUNT count:指定返回结果的数量
* asc|desc:返回结果按照距离中心节点的距离做升序或者降序
* store key:将返回结果的地理位置信息保存到指定键
* storedist key:将返回结果距离中心节点的距离保存到指定键


注意：

1. Redis的GEO功能是从3.2版本添加
2. geo功能基于zset实现
3. geo没有删除命令