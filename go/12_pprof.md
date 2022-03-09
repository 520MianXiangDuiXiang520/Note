# pprof

## runtime/pprof

```go
func Unmarshal(data []byte) (json_node.IJsonNode, error) {
	defer func() {
		pprof.StopCPUProfile()
	}()
	t := time.Now()
	f, err := os.Create(fmt.Sprintf("./pprof/%d_%d_%d_%d_%d.pprof",
		t.Year(), t.Month(), t.Day(), t.Hour(), t.Minute()))
	if err != nil {
		fmt.Println(err)
		panic("[Debug] fail to create pprof file")
	}
	err = pprof.StartCPUProfile(f)
	if err != nil {
		panic(err)
	}
    parse := NewParser()
    return parse.Parser(data)
}
```

go tool pprof -http=:8888 .\2021_10_7_23_41