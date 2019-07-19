value1 = (7, 8)
value2 = [9, 0]
print("DAY %s 格式化字符串 %s " % (value1,value2))
value3 = 1
s = "xxxix %s" % value3  # 不推荐
print(s)
try:
    s1 = "xxxx %s " % value1
    print(s1)  # TypeError: not all arguments converted during string formatting
except TypeError:
    print("TypeError")

s2 = "xxxx {age} xxxx {name}".format(age=18, name="hangman")
print(s2)  # xxxx 18 xxxx hangman
s3 = "xxxx {1} xxx{0}".format(value1,value2)
print(s3)  # xxxx [9, 0] xxx(7, 8)
s4 = "xxxx {} XXX {name} xxx {}".format(value2,value1,name="s4")
print(s4)  # xxxx [9, 0] XXX s4 xxx (7, 8)
print(f'{2+1}')
