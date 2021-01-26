# IO 模型

## 阻塞型 IO

> 老李去火车站买票，排队三天买到一张退票。
>
> 耗费：在车站吃喝拉撒睡 3天，其他事一件没干。

```c
int main(int argc, char *argv[])
{
    // ......
	while(1)
	{
        // 第一次阻塞等待客户端连接
		clnt_sock=accept(serv_sock, (struct sockaddr*)&clnt_adr, &clnt_adr_sz);
        // 第二次阻塞等待客户端发送数据
		while((str_len=read(clnt_sock, message, BUF_SIZE))!=0)
			write(clnt_sock, message, str_len);
	}
}
```

在阻塞型 IO 地模式下，以第二次阻塞为例，程序会被阻塞在第二个 `while` 处，直到客户端消息准备好，在这期间，不能干任何事。

## 非阻塞型 IO

> 老李去火车站买票，隔12小时去火车站问有没有退票，三天后买到一张票。
>
> 耗费：往返车站6次，路上6小时，其他时间做了好多事。



