import re

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        mat = re.match("^" + p + "$", s)
        return (mat is not None) and mat.string == s


if __name__ == '__main__':
    print(Solution().isMatch("aa", "a*"))