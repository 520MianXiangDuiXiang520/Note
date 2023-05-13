# Navicat Premium连接SQL Server

步骤：

1. 激活SQL Server 服务
2. 配置SQL Server网络配置
3. 连接SQL Server
4. 导入数据

## 激活SQLServer服务

直接搜索 **计算机管理** 点 **服务和应用程序**， 点 **SQL Server**配置管理器， 双击第一个**SQL Server服务**

![01](image/01.png)

不出意外的话，是这样的

![02](image/02.png)

如果出现这个 远程过程调用失败，那你一定是安装了Visual Studio，你需要卸载
**Microsoft SQL Server 2016 Express LocalDB**（控制面板->程序和功能）

![03](image/03.png)

最后：右键第一个，启动SQL Server服务

## 网络配置

双击第二个网络配置，再双击TCP/IP，点IP地址，拉到最下面，把TCP动态端口改为1433，确定，然后再右击TCP/IP，启用这个服务。

![04](image/04.png)

最后重启SQL Server服务

## 连接SQL Server

新建连接(Connection) -> SQL Server -> 随便起个名字 -> host设置为**localhost**或**127.0.0.1** -> 使用window验证连接 -> 测试连接 -> 如果测试通过，就ok了

![05](image/05.png)

这就好了！

![06](image/06.png)

## 导入数据

```sql
exec sp_attach_db @dbname = 'text',
@filename1 = 'E:\桌面文件\作业\XSCJ_DB\XSCJ_Data.MDF',
@filename2 = 'E:\桌面文件\作业\XSCJ_DB\XSCJ_Log.LDF';
```

* text：（数据库名） 必须是原先没有的数据库
* filename1和filename2：MDF文件和LDF文件路径，**user用户必须对该目录拥有完全控制权限**。（右键文件夹->属性->安全->Users->编辑->完全控制->确定）

![07](image/07.png)
