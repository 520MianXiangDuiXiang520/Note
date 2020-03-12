class ShellSort:
    @staticmethod
    def shell_sort(nums: list, graps: tuple):
        for grap in graps:
            for i in range(grap - 1, len(nums) - 1):
                index = nums[i + 1]
                j = i
                while j >= 0 and nums[j] > index:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    j -= grap
        print(nums)

if __name__ == '__main__':
    ShellSort().shell_sort([2, 5, 9, 3, 4, 7, 1, 8, 7, 6, 0, -2], [6, 3, 1])