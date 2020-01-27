num = int(input())
get = input()
s = [int(i) for i in get.split(" ") if i != '']
s.sort(reverse=True)
for i in range(num):
    print(s[i], end = " ")
