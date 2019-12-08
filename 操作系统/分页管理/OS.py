from 分页管理.AddressTranslation import AddressTranslation, LogicalAddress
from 分页管理.PageTable import RAM, PageTable
from 分页管理.Process import Process, PCB
import random


class Page:
    def __init__(self, id: int):
        self.id = id

    def __str__(self):
        return "<Page> address:" + str(self.id)

    def __repr__(self):
        return "<Page> address:" + str(self.id)


class OS:
    fifo_index = 0

    def fifo(self, page: Page):
        RAM.blocks[self.fifo_index][1] = page
        if self.fifo_index < len(RAM.blocks):
            self.fifo_index += 1
        else:
            self.fifo_index = 0

    def create_process(self):
        pages = [i for i in range(15)]
        page_table = PageTable()
        # 开始时，页表中没有东西，内存的块中也没有东西
        print(f"页表中的数据：{page_table.page_table}")
        print(f"内存中的块：{RAM.blocks}")
        # page_table_data = list(tuple(zip(range(len(page)), page)))
        # 将页装入内存
        for index, page in enumerate(pages):
            for ind, block in enumerate(RAM().blocks):
                # 遍历内存，如果内存中某一块是空的，就把该页插入这一块
                if not block[1]:
                    block[1] = Page(index)
                    # 更新页表
                    page_table.append((index, block[0]))
                    print("将一页加入块中")
                    print(f"页表中的数据：{page_table.page_table}")
                    print(f"内存中的块：{RAM.blocks}")
                    break
                if ind == len(RAM.blocks) - 1:
                    print("内存已满，执行置换算法")
                    self.fifo(Page(index))
                    page_table.page_table.pop(self.fifo_index)
                    page_table.append((index, block[0]))
                    print(f"页表中的数据：{page_table.page_table}")
                    print(f"内存中的块：{RAM.blocks}")
        return Process(random.randint(0, 199), PCB(0, 0), page_table)

    def run_process(self):
        process = self.create_process()
        order = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
        for i in order:
            AddressTranslation(process).translation_mechanism_with_tlb(LogicalAddress(i, 18))


if __name__ == '__main__':
    OS().run_process()
    # print(Page(1))