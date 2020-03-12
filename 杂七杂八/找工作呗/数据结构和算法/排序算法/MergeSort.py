class MergeSort:

    @staticmethod
    def merge(left: list, right: list) -> list:
        """
        将输入的两个有序数组归并为一个有序数组
        """
        result = []
        l = r = 0
        while l < len(left) and r < len(right):
            if left[l] < right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        # 最后剩下的一个元素没有被加进去
        result += left[l:]
        result += right[r:]
        return result

    def sort(self, nums: list):
        if len(nums) <= 1:
            return nums
        mid = len(nums) // 2
        left = self.sort(nums[:mid])
        right = self.sort(nums[mid:])
        return self.merge(left, right)


if __name__ == '__main__':
    result = MergeSort().sort([5, 7, 7, 9, 3, 6, 1, 4, 2])
    print(result)
        
