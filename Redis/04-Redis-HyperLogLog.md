# Redis-HyperLogLog

基于HyperLogLog算法，使用极小的空间完成巨量运算

<!-- more -->

## Redis HyperLogLog 基本操作命令

1. `PFADD key element [element …]`: 将任意数量的元素添加到指定的 HyperLogLog 里面。
2. `PFCOUNT key [key …]`: 计算hyperloglog的独立总数
3. `prmerge destkey sourcekey [sourcekey…]`: 合并多个hyperloglog

### python 操作Redis HyperLogLog

```py
from MyRedis.RedisTool import RedisTool


class RedisHLL:
    def __init__(self):
        self._conn = RedisTool.redis_connection("39.106.168.39", 8100, "redis19990805")

    def hll_test(self):
        self._conn.pfadd('test', "junebao", "python", "redis", "hyperloglog", "java")
        count = self._conn.pfcount("test")
        print(count)
        

if __name__ == '__main__':
    RedisHLL().hll_test()  # 5
```


## HyperLogLog 算法

特点：

* 能使用极少的内存来统计巨量的数据，在Redis中的HyperLogLog只需要12k内存就能统计 $2^{64}$
* 计数存在一定的误差，但误差率整体较低，标准误差为 0.81%
* 可以设置`辅助计算因子`减小误差

### HyperLogLog 简介

HyperLogLog 其实是 LogLog 算法的改进版，Loglog源于著名的`伯努利实验`。

这个实验是这样的：随机抛一枚硬币，那么正面朝上和反面朝上的概率都应该是 $ 50% $ ,那么如果一直重复抛硬币，直到出现正面朝上，就记作1次伯努利实验。

对于单个一次伯努利实验，抛硬币的次数是不确定的，有可能第一次就正面朝上，那这1次就被记为1次伯努利实验，也有可能抛了10次才出现正面朝上，那这10次才会被记作1次伯努利实验。

假设做了n次伯努利实验，第一次实验抛了 $ k_1 $ 次硬币， 第二次抛了 $ k_2 $ 次硬币，那么第 n 次实验就抛了 $ k_n $ 次硬币。在 $ [k_1 -k_n] $ 之间，就必然存在一个最大值 $ k_{max} $ , $k_{max}$的意义就是在这一组伯努利实验中，出现正面朝上需要的最多的抛掷次数。结合极大似然估计方法得到伯努利实验的次数 $ n $ 和这个最大值 $ k_{max} $ 存在关系: $$ n = 2^{k_{max}}$$

例如：实验0和1表示硬币的正反，一轮做五次实验，某轮伯努利实验的结果为

```txt
# 第一次
001
# 第二次
01
# 第三次
1
# 第四次
0001
# 第五次
001
```

那么这一轮伯努利实验的 $k_{max}=4$ ,按照上面的公式应该得到 $5=2^4$,这个误差显然太过巨大，我们可以增加某一轮实验的次数，用python模拟一下

```py
import random


class BernoulliExp:
    def __init__(self, freq: int):
        self.freq = freq
        self.option = [0, 1]

    def run(self):
        k_max = 0
        for i in range(self.freq):
            num = 0
            while True:
                num += 1
                result = random.choice(self.option)
                if result == 1:
                    break
            # print(f"第{i}次伯努利实验，抛了{num}次硬币")
            if num > k_max:
                k_max = num
        return k_max


if __name__ == '__main__':
    be = BernoulliExp(5000)
    k_max = be.run()
    print(f"k_max={k_max}")
```

通过测试，当每一轮进行5000次伯努利实验时，进行五轮，$k_{max}$分别为 12， 12， 14， 11， 15，误差仍旧很大，所以我们可以进行多轮伯努利实验，求$k_{max}$的平均值，用python模拟一下

```py
import random


class BernoulliExp:
    def __init__(self, freq: int, rounds: int, num: int):
        """
        Args:
            freq: int,每轮进行多少次实验
            rounds: k_max 对多少轮实验求平均
            num: 进行多少次这样的实验（求误差）
        """
        self.freq = freq
        self.option = [0, 1]
        self.rounds = rounds
        self.number_of_trials = num

    def _run_one_round(self):
        k_max = 0
        for i in range(self.freq):
            num = 0
            while True:
                num += 1
                result = random.choice(self.option)
                if result == 1:
                    break
            # print(f"第{i}次伯努利实验，抛了{num}次硬币")
            if num > k_max:
                k_max = num
        return k_max

    def get_k_max(self):
        sum_k_max = 0
        for i in range(self.rounds):
            sum_k_max += self._run_one_round()
        return sum_k_max / self.rounds

    def deviation(self):
        dev = 0
        for i in range(self.number_of_trials):
            k_max = self.get_k_max()
            print(f"第{i}次：k_max = {k_max}")
            dev += (2 ** k_max) - self.freq
        return dev/self.number_of_trials


if __name__ == '__main__':
    be = BernoulliExp(6, 16384, 5)
    dev = be.deviation()
    print(f"误差：{dev}")

```

```txt
第0次：k_max = 4.03546142578125
第1次：k_max = 4.034423828125
第2次：k_max = 4.05010986328125
第3次：k_max = 4.02423095703125
第4次：k_max = 4.045654296875
误差：10.427087015403654
```

这时误差依旧非常大，但我们发现 $ k_{max}$却浮动在4.038上下，这就说明$ n $和 $k_{max}$ 之间的关系确实存在，但公式前面还应该有一个常数项，原公式应该是 $$ n = \alpha · 2^{k_{max}}$$

通过简单计算，把 $ \alpha $设为 $ 0.3652 $:

```txt
第0次：k_max = 4.055908203125
第1次：k_max = 4.0262451171875
第2次：k_max = 4.03045654296875
第3次：k_max = 4.04534912109375
第4次：k_max = 4.048095703125
误差：0.01269833279264585
```

这里0.3652是用$n=6$计算出来的，但当n取其他值时，这个因子也能基本将相对误差控制在0.1以内。

上面的公式，便是LogLog的估算公式

$$DV_{LL} = constant * m * 2 ^ {\overline{R}}$$

其中 $DV_{LL}$就是n，constant就是调和因子， m是实验轮数，$ \overline{R}$ 是 $k_{max}$的平均值。

----

而 HyperLogLog和LogLog的区别就是使用调和平均数计算$k_{max}$，这样如果计算的数值相差较大，调和平均数可以较好的反应平均水平，调和平均数的计算方式为：

$$ H_n = \frac{n}{\sum_{i=1} ^ n \frac{1}{x_i}}$$

所以 HyperLogLog 的公式就可以写为

$$DV_{HLL} = const * m * \frac{m}{\sum_{j=1} ^ m \frac{1}{2^{R_j}}}$$

## 在Rebit中的应用

如果我们我们可以通过$k_{max}$来估计$n$,那同样的，对于一个比特串，我们就可以按照这个原理估算出里面1的个数，例如在

> 统计一个页面每日的点击量（同一用户不重复计算）

要实现这个功能，最简单的办法就是维持一个set，每当有用新户访问页面，就把ID加入集合（重复访问的用户也不会重复加），点击量就是集合的长度，但这样做最大的问题就是会浪费很多空间，如果一个用户ID占8字节，加入有一千万用户，那就得消耗几十G的空间，但Redis只用了12k就完成了相同的功能。

首先，他把自己的12k划分为 16834 个 6bit 大小的 “桶”，这样每个桶所能表示的最大数字为 ${1111}_{(2)} = 63$, 在存入时，把用户ID作为Value传入，这个value会被转换为一个64bit的比特串，前14位用来选择这个比特串从右往左看，第一次出现1的下标要储存的桶号。

例如一个value经过Hash转换后的比特串为

```bit
[0000 0000 0000 1100 01]01 0010 1010 1011 0110 1010 0111 0101 0110 1110 0110 0100
```

这个比特串前14位是 ${110001}_{(2)}$,转换成10进制也就是49，而它从右往左看，第3位是1，所以3会被放到49桶中（首先要看49桶中原来的值是不是小于3，如果比3小，就用3替换原来的，否则不变，【因为桶中存的是$k_{max}$】）, $k_{max}$在这里最大也只能是64，用6bit肯定够用。

这样不管有多少用户访问网站，存储的只有这12k的数据，访问量越多，$k_{max}$ 越大，然后根据HyperLogLog公式，就可以较精确的估计出访问量。（一个桶可以看作一轮伯努利实验）

### 修正因子

constant 并不是一个固定的值，他会根据实际情况而被分支设置，如： $$P = \log_2 m$$

m 是分桶数

```c
switch (p) {
   case 4:
       constant = 0.673 * m * m;
   case 5:
       constant = 0.697 * m * m;
   case 6:
       constant = 0.709 * m * m;
   default:
       constant = (0.7213 / (1 + 1.079 / m)) * m * m;
}
```

## 参考

[https://www.cnblogs.com/linguanh/p/10460421.html#commentform](https://www.cnblogs.com/linguanh/p/10460421.html#commentform)

[https://chenxiao.blog.csdn.net/article/details/104195908](https://chenxiao.blog.csdn.net/article/details/104195908)

