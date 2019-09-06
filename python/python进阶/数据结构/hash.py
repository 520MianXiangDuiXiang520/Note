# python 实现哈希表

class HashTable:
    """
    哈希函数的构造
    解决冲突
    """

    def __init__(self, source):
        self.source = source
        self._index = []
        self._val = []
        self.table = []
        self._mod = 13

    def Output(self):
        print(self._index)
        print(self._val)
    
    def _create_table(self):
        """
        初始化哈希表
        哈希表长度最短为取余因子_mod,一般为源数据长度
        """
        if len(self.source) < self._mod:
            length = self._mod
        else:
            length = len(self.source)
        
        self._index = [i for i in range(length)]
        self._val = [None for i in range(length)]

    def _func_hash(self):
        """
        构建哈希函数
        """
        for sour in self.source:
            remainder = sour % self._mod
            if self._val[remainder] is None:
                self._val[remainder] = sour
            else:
                # 处理冲突
                rem = remainder
                while self._val[rem] is not None:
                    if(rem + 1 >= len(self._val)):
                        rem = -1
                    rem += 1
                self._val[rem] = sour
        self.table = list(zip(self._index, self._val))


    def get(self, num):
        """
        查找
        """
        rem = num % self._mod
        if self._val[rem] != num:
            while True:
                if(rem + 1 >= len(self._val)):
                    rem = 0
                if self._val[rem] == num:
                    break
                rem += 1
        return rem
    
    def run(self):
        self._create_table()
        self._func_hash()
        self.Output()

if __name__ == '__main__':
    test = [12, 15, 17, 21, 22, 25, 13, 0]
    h = HashTable(test)
    h.run()
    h.get(12)
