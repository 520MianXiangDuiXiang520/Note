class BubbleSort:
    @staticmethod
    def run(nums: list):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[i]:
                    nums[i], nums[j] = nums[j], nums[i]
        print(nums)


if __name__ == '__main__':
    BubbleSort().run([5, 9, 3, 4, 7, 1])
