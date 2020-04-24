class HeapSort:
    def _get_heap(self, nums: list, start: int, end: int):
        root = start
        while True:
            child = root * 2 + 1
            if child >= end:
                break
            if child + 1 < end and nums[child + 1] > nums[child]:
                child += 1
            if nums[child] > nums[root]:
                nums[child], nums[root] = nums[root], nums[child]
                root = child
            else:
                break

    def sort(self, nums: list):
        length = len(nums)
        for start in range(length - 1, -1, -1):
            self._get_heap(nums, start, length)
        print(nums)
        for end in range(length - 1, 0, -1):
            nums[0], nums[end] = nums[end], nums[0]
            self._get_heap(nums, 0, end - 1)


if __name__ == '__main__':
    nums = [5, 9, 3, 4, 7, 1]
    HeapSort().sort(nums)
    print(nums)

