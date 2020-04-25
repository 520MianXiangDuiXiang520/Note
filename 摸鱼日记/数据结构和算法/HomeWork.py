class Solution:
    def minTime(self, time: list, m: int) -> int:
        if len(time) < m:
            return 0
        time.sort()
        return sum(time[:(m * -1)])


if __name__ == '__main__':
    print(Solution().minTime([1, 7, 3, 3], 2))