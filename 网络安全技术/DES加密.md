# DES加密算法原理及实现

DES是一种对称加密算法【即发送者与接收者持有相同的密钥】，它的基本原理是将要加密的数据划分为n个64位的块，然后使用一个56位的密钥逐个加密每一个64位的块，得到n个64位的密文块，最后将密文块拼接起来得到最终的密文

<!-- more -->

加密过程：

1. 初态置换
2. 扩展置换
3. S盒压缩
4. P盒置换
5. 终态置换

## 初始转换

这一步的目的是将用户输入转换为64位的块，不足64位需要补位

python实现

```python
from bitarray import bitarray


class MyDES:
    def __init__(self, enter: str):
        self._enter = enter

    def processing_input(self) -> list:
        """
        处理输入，将要加密/解密的数据先处理成二进制形式，
        然后划分为n个64位的块
        Return:
            [[0, 1, 0, ...], [], []]
        """
        result = []
        bit_string = bitarray(
            ''.join([bin(int('1' + hex(c)[2:], 16))[3:]
                     for c in self._enter.encode('utf-8')])).to01()
        # 如果长度不能被64整除，就补零
        if len(bit_string) % 64 != 0:
            for i in range(64 - len(bit_string) % 64):
                bit_string += '0'
        for i in range(len(bit_string) // 64):
            result.append(bit_string[i * 64: i * 64 + 64])
        return result


```

这一步的结果大致为：

```python
if __name__ == '__main__':
    md = MyDES("junebao.top")
    print(md.processing_input())
```

```txt
['0110101001110101011011100110010101100010011000010110111100101110', '0111010001101111011100000000000000000000000000000000000000000000']
```



## 初态/终态置换

初态/终态置换是指按照一定的规则【IP置换表】，将原来的64位二进制数据重新排列。

IP正向置换表

```txt
58, 50, 42, 34, 26, 18, 10, 2, 
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17, 9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7
```

IP逆向置换表

```
 40, 8, 48, 16, 56, 24, 64, 32,
 39, 7, 47, 15, 55, 23, 63, 31,
 38, 6, 46, 14, 54, 22, 62, 30,
 37, 5, 45, 13, 53, 21, 61, 29,
 36, 4, 44, 12, 52, 20, 60, 28,
 35, 3, 43, 11, 51, 19, 59, 27,
 34, 2, 42, 10, 50, 18, 58, 26,
 33, 1, 41, 9, 49, 17, 57, 25
```

IP置换表中每一位的意思是：如第一个58就表示把原来比特串中第58位放在新串的第1位，第二个50表示把原来比特串的第50位放在新串的第2位......

python 实现

```python
from bitarray import bitarray


class MyDES:
    
    @staticmethod
    def replace_block(block: str, replace_table: list) -> str:
        """
        对单个块进行置换
        Args:
            block: str, 要进行转换的64位长的01字符串
            replace_table: 转换表
        Return:
            返回转换后的字符串
        """
        result = ""
        for i in replace_table:
            result += block[i-1]
        return result

    def _init_replace_block(self, block: str):
        """
        对一个块进行初态置换
        """
        replace_table = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
        return self.replace_block(block, replace_table)

    def _end_replace_block(self, block: str) -> str:
        """
        对某一个块进行终态转换
        """
        replace_table = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        ]
        return self.replace_block(block, replace_table)

    def initial_state_replacement(self) -> list:
        """
        对所有的块进行初态置换
        Return:
            返回置换后的所有块的列表
        """
        blocks = self.processing_input()
        result = []
        for block in blocks:
            result.append(self._init_replace_block(block))
        return result

    def end_state_replacement(self):
        """
        对所有的块进行终态置换
        """
        pass

```

这一步结束后结果为：

```python
if __name__ == '__main__':
    md = MyDES("junebao.top")
    print(md.processing_input())
    print(md.initial_state_replacement())
    print(md.end_state_replacement())
```

为了测试，终态置换的输入我直接用了初态置换的输出

```txt
['0110101001110101011011100110010101100010011000010110111100101110', '0111010001101111011100000000000000000000000000000000000000000000']
['0111111100000010110011100110101000000000111111111100010111010101', '0000011100000101000000110000001000000000000001110000001000000010']
['0110101001110101011011100110010101100010011000010110111100101110', '0111010001101111011100000000000000000000000000000000000000000000']
```

## 拓展置换

将初态置换后的块分为左右各32位的子块，将其中一个子块根据【拓展置换表】拓展为一个48位的数据；具体就是将32位的数据分成4*8小块，每个小块拓展为6位。

拓展置换表：

```txt
32, 1,  2,  3,  4,  5,
4,  5,  6,  7,  8,  9,
8,  9,  10, 11, 12, 13,
12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21,
20, 21, 22, 23, 24, 25,
24, 25, 26, 27, 28, 29,
28, 29, 30, 31, 32, 1
```

拓展置换表中，每一行代表拓展后的一个小块，内部数字表示原来子块中01的位置，其实就是在每一个小块前面加上前一个小块的最后一个字符，后面加上下一个小块的第一个字符，比如有三个小块：

```txt
0 1 0 0     1 0 1 1     1 0 0 1
```

那么第二个小块拓展之后就是

```
0 1 0 1 1 1
```

python 实现

```python
@staticmethod
    def block_extend(block: str) -> tuple:
        """
        对每一块进行拓展置换
        Args:
            block: 64位的01字符串
        Return:
            返回一个二元组，第0位是32位的原串，第1位是经过拓展置换后的48位串
        """
        # 将原来的块分为左右各32位的子块
        left, right = block[0: 32], block[32: 64]
        extended_block = ""
        extend_table = (
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        )
        for i in extend_table:
            extended_block += right[i - 1]
        return left, extended_block
```

##  密钥生成

DES初始密钥是一个64位的串，其中8，16， 24， 32， 40， 48，56， 64位作为奇偶检验位，实际加密中使用的只有56位，由于DES加密过程中需要16次循环迭代，所以需要产生16个子密钥，单次子密钥的生成过程如图

![image-20200306172508700](image/DES加密/image-20200306172508700.png)

### 密钥转换

密钥转换的目的是将64位原始密钥转换为56位的密钥，并进行一次置换

* 依照的表是密钥转换表

  ```txt
  57,49,41,33,25,17,9,1,58,50,42,34,26,18,
  10,2,59,51,43,35,27,19,11,3,60,52,44,36,
  63,55,47,39,31,23,15,7,62,54,46,38,30,22,
  14,6,61,53,45,37,29,21,13,5,28,20,12,4
  ```

  具体转换规则盒前面一样

代码实现

```python
    def key_conversion(self):
        """
        将64位原始密钥转换为56位的密钥，并进行一次置换
        """
        first_key = self._key[0: 8] + self._key[9: 16] + self._key[17: 24] + \
            self._key[25: 32] + self._key[33: 40] + self._key[41: 48] + self._key[49: 56]
        key_replace_table = (
            57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
        )
        key_after_replace = ""
        for i in key_replace_table:
            key_after_replace += first_key[i - 1]
        return key_after_replace
```



### 密钥旋转

64位初始密钥经过密钥转换去除奇偶检验位，并将得到的56位密钥分成两个28位的子串，然后将这两个子串进行循环旋转，具体规则依照**DesRotations**表

| **Round**     | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   | 15   | 16   |
| ------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| **Rotations** | 1    | 1    | 2    | 2    | 2    | 2    | 2    | 2    | 1    | 2    | 2    | 2    | 2    | 2    | 2    | 1    |

* Round表示第几轮旋转，也就是第几个key
* Rotations表示旋转次数

> 除了第1， 2， 9， 16个key旋转1位，其他都旋转两位

代码实现：

```python
    def spin_key(self):
        """
        旋转获得子密钥
        """
        first, second = self.key_conversion()
        spin_table = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)
        for i in range(1, 17):
            first_after_spin = first[spin_table[i - 1]:] + first[:spin_table[i - 1]]
            second_after_spin = second[spin_table[i - 1]:] + second[:spin_table[i - 1]]
            yield first_after_spin + second_after_spin
```



### 置换选择

目的是将56位数据变成48位子密钥，对照的表是 置换选择表

```txt
14,17,11,24,1,5,3,28,15,6,21,10,
23,19,12,4,26,8,16,7,27,20,13,2,
41,52,31,37,47,55,30,40,51,45,33,48,
44,49,39,56,34,53,46,42,50,36,29,32    
```

置换规则也与其他置换表一样

代码实现：

```python
    def key_selection_replacement(self):
        """
        通过选择置换得到48位的子密钥
        """
        key_select_table = (
            14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
        )
        for child_key56 in self.spin_key():
            child_key48 = ""
            for i in key_select_table:
                child_key48 += child_key56[i - 1]
            self.child_keys.append(child_key48)
```



## S盒压缩

![image-20200306114626096](image/DES加密/image-20200306114626096.png)

S盒压缩的目的是将拓展置换得到的48位比特串与48位密钥（不算8个校验位）做异或运算后重新得到一个32位的串。这里用到了8张 4*16 的【S盒压缩表】

```python
s_box1 = [
    [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
],
s_box2 = [
    [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
    [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
    [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
    [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
],
s_box3 = [
    [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
    [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
    [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
    [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
],
s_box4 = [
    [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
    [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
    [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
    [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
],
s_box5 = [
    [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
    [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
    [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
    [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
],
s_box6 = [
    [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
    [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
    [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
    [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
],
s_box7 = [
    [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
    [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
    [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
    [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
],
s_box8 = [
    [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
    [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
    [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
    [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
]
```

具体做法是：

将经过拓展置换后得到的48位串与48位密钥做异或，得到48位密文串，每6个分一组，分8组，如第二组是`111011`就查找把第一位与最后一位取出得到`11`,转换为十进制3作为行号，中间四位`1101`转换为十进制13作为列号，查找s_box2的3行13列得到9，将9转换为二进制为`1001`就是这6为密文压缩后的结果，其他一样，最终会输出32位密文串



## 完整代码

```python
from bitarray import bitarray


class MyDES:
    def __init__(self, enter: str):
        self._enter = enter
        self.child_keys = []

    @staticmethod
    def _bit_encode(s: str) -> str:
        return bitarray(
            ''.join([bin(int('1' + hex(c)[2:], 16))[3:]
                     for c in s.encode('utf-8')])).to01()

    @staticmethod
    def _bit_decode(s: str) -> str:
        bit = bitarray(s)
        return bit.hex()

    @staticmethod
    def negate(s: str):
        result = ""
        try:
            for i in s:
                result += '0' if i == '1' else '1'
            return result
        except:
            print("密钥错误")
            raise

    @staticmethod
    def replace_block(block: str, replace_table: tuple) -> str:
        """
        对单个块进行置换
        Args:
            block: str, 要进行转换的64位长的01字符串
            replace_table: 转换表
        Return:
            返回转换后的字符串
        """
        result = ""
        for i in replace_table:
            try:
                result += block[i - 1]
            except IndexError:
                print(i)
                print(f"block= {block}, len={len(block)}")
                raise
        return result

    def processing_encode_input(self) -> list:
        """
        处理加密输入，将要加密/解密的数据先处理成二进制形式，
        然后划分为n个64位的块
        Return:
            [[0, 1, 0, ...], [], []]
        """
        result = []
        bit_string = self._bit_encode(self._enter)
        # 如果长度不能被64整除，就补零
        if len(bit_string) % 64 != 0:
            for i in range(64 - len(bit_string) % 64):
                bit_string += '0'
        for i in range(len(bit_string) // 64):
            result.append(bit_string[i * 64: i * 64 + 64])
        return result

    @staticmethod
    def processing_decode_input(enter: str) -> list:
        result = []
        try:
            input_list = enter.split("0x")[1:]
            int_list = [int("0x" + i, 16) for i in input_list]
            for i in int_list:
                bin_data = str(bin(i))[2:]
                while len(bin_data) < 64:
                    bin_data = '0' + bin_data
                result.append(bin_data)
            return result
        except Exception as e:
            raise

    def key_conversion(self, key):
        """
        将64位原始密钥转换为56位的密钥，并进行一次置换
        """
        first_key = key
        key_replace_table = (
            57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
        )
        key_after_replace = self.replace_block(first_key, key_replace_table)
        return key_after_replace[0: 28], key_after_replace[28: 56]

    def spin_key(self, key: str):
        """
        旋转获得子密钥
        """
        first, second = self.key_conversion(key)
        # spin_table = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)
        spin_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)
        print(f"去掉校验位后的key: {first + second}")
        for i in range(1, 17):
            # first, second = self.child_keys[i - 1][0: 28], self.child_keys[i - 1][28:]
            first_after_spin = first[spin_table[i - 1]:] + first[:spin_table[i - 1]]
            second_after_spin = second[spin_table[i - 1]:] + second[:spin_table[i - 1]]
            print(f"旋转后的key： left: {first_after_spin}, right: {second_after_spin}")
            yield first_after_spin + second_after_spin

    def key_selection_replacement(self, key: str):
        """
        通过选择置换得到48位的子密钥
        """
        key_select_table = (
            14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
        )
        for child_key56 in self.spin_key(key):
            self.child_keys.append(self.replace_block(child_key56, key_select_table))

    def _init_replace_block(self, block: str):
        """
        对一个块进行初态置换
        """
        replace_table = (
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        )
        return self.replace_block(block, replace_table)

    def _end_replace_block(self, block: str) -> str:
        """
        对某一个块进行终态转换
        """
        replace_table = (
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        )
        return self.replace_block(block, replace_table)

    def initial_state_replacement(self, blocks) -> list:
        """
        对所有的块进行初态置换
        Return:
            返回置换后的所有块的列表
        """
        result = []
        for block in blocks:
            result.append(self._init_replace_block(block))
        return result

    def initial_state_replace_decode(self, blocks) -> list:
        result = []
        for block in blocks:
            result.append(self._end_replace_block(block))
        return result

    @staticmethod
    def block_extend(block: str) -> str:
        """
        对每一块进行拓展置换
        Args:
            block: 64位的01字符串
        Return:
            返回经过拓展置换后的48位串
        """
        # 将原来的块分为左右各32位的子块

        extended_block = ""
        extend_table = (
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        )
        for i in extend_table:
            extended_block += block[i - 1]
        return extended_block

    @staticmethod
    def _not_or(a: str, b: str) -> str:
        """
        对两个01字符串做异或
        """
        result = ""
        size = len(a) if len(a) < len(a) else len(b)
        for i in range(size):
            result += '0' if a[i] == b[i] else '1'
        return result

    def _s_box_replace(self, block48: str) -> str:
        """
        S盒置换，将48位的输入转换为32位输出
        """
        s_box_table = (
            (
                (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
                (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
                (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
                (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
            ),
            (
                (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
                (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
                (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
                (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
            ),
            (
                (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
                (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
                (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
                (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
            ),
            (
                (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
                (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
                (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
                (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
            ),
            (
                (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
                (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
                (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
                (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
            ),
            (
                (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
                (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
                (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
                (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
            ),
            (
                (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
                (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
                (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
                (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
            ),
            (
                (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
                (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
                (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
                (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
            )
        )
        result = ""
        for i in range(8):
            row_bit = (block48[i * 6] + block48[i * 6 + 5]).encode("utf-8")
            line_bit = (block48[i * 6 + 1: i * 6 + 5]).encode("utf-8")
            row = int(row_bit, 2)
            line = int(line_bit, 2)
            # print(f"第{row}行， 第{line}列")
            data = s_box_table[i][row][line]
            no_full = str(bin(data))[2:]
            while len(no_full) < 4:
                no_full = '0' + no_full
            result += no_full
        return result

    def s_box_compression(self, num: int, block48: str) -> str:
        """
        对经过拓展置换后的48位01串进行S盒压缩，有两部：
          1. 与key做异或
          2. 根据S盒压缩表经48位压缩为36位
        Args:
            num: 第几次迭代
            block48: right
        Return:
            返回经过S盒压缩后的32位01字符串
        """
        result_not_or = self._not_or(block48, self.child_keys[num])
        print(f"与key 做异或后的结果{result_not_or}")
        return self._s_box_replace(result_not_or)

    def p_box_replacement(self, block32: str) -> str:
        """
        P盒置换
        Return:
            返回经过P盒置换后的32位01串
        """
        p_box_replace_table = (
            16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
        )
        return self.replace_block(block32, p_box_replace_table)

    def iteration(self, block: str, is_decode: bool) -> str:
        for i in range(16):
            left, right = block[0: 32], block[32: 64]
            next_left = right
            right = self.block_extend(right)
            print(f"拓展置换后的结果：{left, right}")
            if is_decode:
                sbc_result = self.s_box_compression(15 - i, right)
            else:
                sbc_result = self.s_box_compression(i, right)
            print(f"s盒压缩后的结果:{sbc_result}")
            pbr_result = self.p_box_replacement(sbc_result)
            print(f"P盒拓展后的结果:{pbr_result}")
            right = self._not_or(left, pbr_result)
            print(f"与left做异或后的结果:{right}")
            block = next_left + right
        return block

    def encode(self, key: str):
        result = ""
        self.key_selection_replacement(key)
        blocks = self.processing_encode_input()
        for block in self.initial_state_replacement(blocks):
            block_result = self.iteration(block, is_decode=False)
            block_result = self._end_replace_block(block_result[32:] + block_result[:32])
            result += str(hex(int(block_result.encode(), 2)))
        return result

    def decode(self, cipher_text: str, key: str):
        result = ""
        blocks = self.processing_decode_input(cipher_text)
        self.key_selection_replacement(key)
        for block in self.initial_state_replacement(blocks):
            # 对right进行S合压缩
            block_result = self.iteration(block, is_decode=True)
            block_result = self._end_replace_block(block_result)
            result += block_result
        return result


if __name__ == '__main__':
    key = "0110101001110101011011100110010101100010011000010110111100101110"
    md = MyDES("junebao")
    print(md.encode(key))

```

