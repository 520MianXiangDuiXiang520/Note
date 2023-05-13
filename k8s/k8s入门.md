

## QA

1. Flannel 下两个容器之间如何通信
   * 如果两个容器在同一个 Pod 内，由于他们共享网络栈和卷，所以可以直接通过 localhost 通信
   * 如果两个容器在不同 Pod 但在同一物理机上，通过 docker0 网关即可转发通信
   * 如果不在同一物理机上，数据包经由 docker0 和 flannel0 网关被 Flanneld 进程捕获，在原数据包基础上分装 UDP 报文，通过查询 ETCD 将 UDP 消息转发给对应物理机 Flanneld 进程， Flanneld 解包后再通过 Flannel0 和 docker0 网关转发给对应容器


问题：



K8S 

作用：协调一个高可用的集群
  * 集群中包括两类资源
    1. Master：调度集群
    2. Node：工作机器，Node 由 Kubelet 管理，Kubelet 是 Node 和 Master 通信的代理
   > Kubelet 如何管理 Node，Node 如何与 Master 通过 Kubelet 通信，通信干什么

Node 使用 Master 暴露的 Kubernetes API 与 Master 通信。终端用户也可以使用 Kubernetes API 与集群交互

> ? K8s Api 和 Kubelet 有啥关系

## Kubectl

作用：命令行操作 K8s集群
常用命令：

```sh
# 查看 kubectl 和 server 版本
kubectl version

# 查看集群信息
kubectl cluster-info

# 查看所有 node
kubectl get nodes

# 创建一个 deployment
kubectl create deployment ang --image=junebao/ang

# deployment 列表
kubectl get deployments

# pods 列表
kubectl get pods

# pods 的一些信息
kubectl describe pods

# pod 日志
kubectl logs $POD_NAME
```

## Deployment

Deployment 告诉 K8s 如何如何创建和更新应用程序实例.

Deployment 会监视 nodes 中的应用程序实例，一旦实例节点关闭或删除，Deployment 会使用另一个节点上的实例代替他
> ？ K8s Deployment 监视的是实例还是 node 一个 node 中如果部署了多个应用程序，其中一个挂了会检查到吗
>  
> ？K8s 如何选择使用哪个 node 部署应用
> ?
> Pod 和 Node 是什么关系？
>   Node 

## Service

Service 提供了外部对 pod 的访问方法，使得外部服务不需要关心 pod 的具体网络情况。 service 有四种类型：

* ClusterIP: 只允许集群内部访问
* NodePort：
* LoadBalancer
* ExternalName

```sh
# 创建 service 并暴露 deployment 的端口
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080

kubectl get services

kubectl describe services/kubernetes-bootcamp

kubectl delete service -l app=kubernetes-bootcamp
```

## Label

每种资源（deployment,node,pod,service）都可以添加标签，它是一个字符串的键值对；你可以使用 `kubectl describe xxx` 来查看，如：

```sh
{20:46}/Users/junebao ➭ kubectl describe services/kubernetes-bootcamp
Name:                     kubernetes-bootcamp
Namespace:                default
Labels:                   app=kubernetes-bootcamp
```

get 时可以使用 `-l` 过滤：

```sh
kubectl get services -l app=kubernetes-bootcamp
```

可以使用 `kubectl label` 设置标签：

```sh
kubectl label services $SERVICES_NAME version=v1
# kubectl label services kubernetes-bootcamp version=v1
```

## 扩缩容

```sh
# 复制集
kubectl get rs

# 缩放复制集到四台
kubectl scale deployments/kubernetes-bootcamp --replicas=4
```

## 更新

```sh
# 使用新镜像更新应用
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2

# 查看资源更新状态
kubectl rollout status deployments/kubernetes-bootcamp

# 回滚更新
kubectl rollout undo deployments/kubernetes-bootcamp
```


## 资源清单
* 名称空间级别
  * 工作负载型：Pod RS Deployments
  * 服务发现和负载均衡
  * 配置与存储型资源 Volume
  * 特殊类型的存储卷 ConfigMap Secret
* 集群级别
  * NameSpace Node 
* 元数据类型
  * HPA ……

资源清单一般用 YAML 配置

```yml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    name: myapp
spec:
  containers:
    - name: myapp
      image: docker.io/junebao857/ang
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
      ports:
        - containerPort: 80
```

### pod 的生命周期

1. pause 镜像初始化网络栈和容器卷
2. 依次执行 init 容器 [link](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/init-containers/)

## 工作负载资源

RS

Depolyments

DaemonSet 

StatefulSet

Job

CronJob

