from my_python_package import code_time

# 有20节楼梯，一次可以走1，2，3，4级，总共有多少种走法

def Modify(c = None):
    if c == None:
        c = {}
    def modify(func):
        catch = c
        def closer(*args):
            if args[0] not in catch:
                catch[args[0]] = func(*args)
            return catch[args[0]]
        return closer
    return modify

@Modify()
def _Stairs(num, steps):
    count = 0
    if num == 0:
        count = 1
    elif num > 0:
        for step in steps:
            count += _Stairs(num-step,steps)
    return count

@code_time
def Stairs(num,steps):
   count = _Stairs(num,steps)
   return count

if __name__ == '__main__':
    num = 20
    steps = [step for step in range(1,5)]
    count = Stairs(num, steps)
    print(count)

    # Stairs runs at: 0.0 s
    # 283953