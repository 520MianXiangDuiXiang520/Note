from 分页管理.PageTable import PageTable
from 分页管理.PageTableRegister import PageTableRegister
from 分页管理.Process import Process, PCB
from 分页管理.TLB import TLB


class OutOfBounds(Exception):
    """
    越界中断
    """
    pass


class LogicalAddress:
    def __init__(self, p: int, w: int):
        self.page_id = p
        self.offset = w

    def __repr__(self):
        return f"log_addr: {self.page_id}"


class AddressTranslation:
    def __init__(self, process: Process):
        self.process = process

    def base_translation(self, logical_address: LogicalAddress):
        """
        基本地址变换机构
        逻辑地址块号 = 页表始址（页表寄存器中） + 页号（来自逻辑地址） * 页表项长度（PRT）
        :param logical_address: 逻辑地址
        :return:
        """
        # page_id = PageTableRegister.page_table_start_address + (logical_address.page_id
        #                                                         * PageTableRegister.page_table_length)
        # 越界中断
        if logical_address.page_id >= len(self.process.page_table.page_table):
            raise OutOfBounds("越界中断")
        page_id = logical_address.page_id
        return self.process.page_table.page_table[page_id]

    def translation_mechanism_with_tlb(self, logical_address: LogicalAddress):
        """
        具有快表的地址变换机构
        :param logical_address: 逻辑地址
        :return:
        """
        # 遍历快表，看要请求的页在不在快表中
        for tlb in TLB():
            # 如果在快表中能找到就直接返回
            if tlb[0] == logical_address.page_id:
                print(f"{logical_address.page_id} 从快表中查到了")
                return tlb[1]
        # 否则就用基本地址变换在页表中找
        print(f"{logical_address.page_id} 没在快表中，去页表中找")
        block_id = self.base_translation(logical_address)
        print(f"{logical_address.page_id}从页表中找到了，加入快表！！")
        # 找到后加入快表
        TLB().append((logical_address, block_id))
        print(f"此时的快表{TLB().data}")
        return block_id


if __name__ == '__main__':
    process = Process(12, PCB(0, 0), PageTable([(0, 1), (1, 2), (2, 3), (3, 4)]))
    block_id = AddressTranslation(process).translation_mechanism_with_tlb(LogicalAddress(2, 18))
    print(f"物理块号{block_id}")
