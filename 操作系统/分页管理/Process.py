from 分页管理.PageTable import PageTable


class PCB:
    def __init__(self, ptsa: int, ptl: int):
        page_table_start_address = ptsa
        page_table_length = ptl


class Process:
    def __init__(self, pid: int, pcb: PCB, page_table: PageTable):
        """
        进程
        :param pid: 进程号
        :param pcb: 进程控制块
        """
        self.pid = pid
        self.pcb = pcb
        # 页表， 每个进程对应一个页表
        self.page_table = page_table
