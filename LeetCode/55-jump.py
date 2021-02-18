class Solution:
    def canJump(self, nums) -> bool:
        if 0 not in nums:
            return True
        farthest_index = 0
        for i in range(len(nums)):
            if i <= farthest_index:
                farthest_index = max((i + nums[i]), farthest_index)
                if farthest_index >= len(nums) - 1:
                    return True
        return False


if __name__ == '__main__':
    print(Solution().canJump([3, 2, 1, 0, 4]))
