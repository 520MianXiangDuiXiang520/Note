class SplitList:
    @staticmethod
    def hcf(a: int, b: int):
        x = a % b
        while x != 0:
            a = b
            b = x
            x = a % b
        return b

    def run(self, nums: list):
        length = len(nums)
        if self.hcf(nums[0], nums[-1]) > 1:
            return 1
        start = 0
        end = length - 1
        mid = []
        # [2, 3, 5, 7]
        while start <= end:
            # end 从后往前找，让第0个元素尽量长
            while end > start and nums[end] % nums[start] != 0:
                end -= 1
            mid.append(nums[start: end + 1])
            start = end + 1
            end = length - 1
        return mid


if __name__ == '__main__':
    print(SplitList().run([2, 3, 4, 5, 6, 7]))
