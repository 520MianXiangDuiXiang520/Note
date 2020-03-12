class InsertionSort:
    @staticmethod
    def run(nums: list):
        for i in range(0, len(nums) - 1):
            insert = nums[i + 1]
            j = i
            # 一直往前换
            while j >= 0 and nums[j] > insert:
                nums[j + 1], nums[j] =  nums[j], nums[j + 1]
                j -= 1
        print(nums)

if __name__ == '__main__':
    InsertionSort().run([5, 9, 3, 4, 7, 1])

            
