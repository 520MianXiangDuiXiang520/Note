import random


class BernoulliExp:
    def __init__(self, freq: int, rounds: int, num: int):
        """
        Args:
            freq: int,每轮进行多少次实验
            rounds: k_max 对多少轮实验求平均
            num: 进行多少次这样的实验（求误差）
        """
        self.freq = freq
        self.option = [0, 1]
        self.rounds = rounds
        self.number_of_trials = num

    def _run_one_round(self):
        k_max = 0
        for i in range(self.freq):
            num = 0
            while True:
                num += 1
                result = random.choice(self.option)
                if result == 1:
                    break
            # print(f"第{i}次伯努利实验，抛了{num}次硬币")
            if num > k_max:
                k_max = num
        return k_max

    def get_k_max(self):
        sum_k_max = 0
        for i in range(self.rounds):
            sum_k_max += self._run_one_round()
        return sum_k_max / self.rounds

    def deviation(self):
        dev = 0
        for i in range(self.number_of_trials):
            k_max = self.get_k_max()
            print(f"第{i}次：k_max = {k_max}")
            dev += 0.3652 * (2 ** k_max) - self.freq
        return (dev/self.number_of_trials)/self.freq


if __name__ == '__main__':
    be = BernoulliExp(80, 16384, 5)
    dev = be.deviation()
    print(f"误差：{dev}")
