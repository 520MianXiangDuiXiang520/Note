count1 = [i for i in range(10)]
count2 = [i for i in range(2, 12)]
count = list(zip(count1, map(lambda x: x * -1, count2)))
print(count)
count.sort(key=lambda x: x[0])
print(count)

# x = Lambda(lambda x : x[:, 0:1, :])(embedding_output)
