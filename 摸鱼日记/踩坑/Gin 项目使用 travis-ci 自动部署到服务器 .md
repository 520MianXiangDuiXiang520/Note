# Golang 快速进行参数检查

## 为什么整

之前面知乎面试官看了我 GitHub 上的项目，说我见你的每个请求都会先去单独检查请求参数，这样感觉很麻烦，有没有什么好一点的方法解决，当时没想到使用反射和标签检查，这几天写课设时又遇到这个问题，受 gorm 的启发，想到能不能在需要检查的字段后面加一个 `check` 标签，然后搞一个方法去逐个验证检查项，一旦不通过，直接返回 `false`

## 示例

```go
type TestStruct struct {
	Name string `check:"not null; len:[0, 12];"`
	Age  int    `json:"age" check:"not null; size: [1, 150]"`
	Q    []int  `check:"len: [1, 3]"`
}

func TestCheckRequest(t *testing.T) {
	ok := CheckRequest(&TestStruct{
		Name: "name",
		Age:  10,
	})
	if ok {
		t.Error("fail")
	}
}
```



