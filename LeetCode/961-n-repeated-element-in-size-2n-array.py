from typing import List

class Solution:
    def repeatedNTimes(self, nums: List[int]) -> int:
        n = len(nums) / 2
        map = {}
        for num in nums:
            v = map.get(num)
            map[num] = 1 if not v else v + 1
        for k, v in map.items():
            if v == n:
                return k
            
if __name__ == "__main__":
    print(Solution().repeatedNTimes([2, 1, 2, 5, 3, 2]))