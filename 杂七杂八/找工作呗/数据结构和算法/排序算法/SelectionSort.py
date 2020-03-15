class SelectSort:
    @staticmethod
    def sort(nums: list):
        if len(nums) <= 1:
            return
        for i in range(len(nums)):
            min_index = i
            for j in range(i+1, len(nums)):
                if nums[j] < nums[min_index]:
                    min_index = j
            if i != min_index:
                nums[i], nums[min_index] = nums[min_index], nums[i]
        print(nums)

if __name__ == '__main__':
    SelectSort().sort([7, 6, 1, 3, 8, 5, 2, 0, -1, -1])