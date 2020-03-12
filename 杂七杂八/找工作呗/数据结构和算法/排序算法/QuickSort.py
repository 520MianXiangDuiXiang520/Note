class QuickSort:

    @staticmethod
    def get_pivot(nums: list, left: int, right: int):
        pivot = nums[left]
        while left < right:
            while nums[right] > pivot and left < right:
                right -= 1
            nums[left] = nums[right]
            while nums[left] < pivot and left < right:
                left += 1
            nums[right] = nums[left]
        nums[left] = pivot
        return left


    def quick_sort(self, nums: list, left: int, right: int):
        if left < right:
            pivot = self.get_pivot(nums, left, right)
            self.quick_sort(nums, left, pivot - 1)
            self.quick_sort(nums, pivot + 1, right)

    
    def run(self, nums: list):
        self.quick_sort(nums, 0, len(nums) - 1)
        print(nums)


if __name__ == '__main__':
    QuickSort().run([5, 9, 3, 4, 7, 1])
