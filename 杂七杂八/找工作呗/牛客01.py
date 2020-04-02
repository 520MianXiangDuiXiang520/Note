while True:
    try:
        input_str = input()
        result = ""
        for i in range(len(input_str)):
            if len(input_str) == 1:
                result = input_str
                break
            if i == 0:
                if input_str[i + 1] != input_str[i]:
                    result = result + input_str[i]
            elif i == len(input_str) - 1:
                if input_str[i - 1] != input_str[i]:
                    result = result + input_str[i]
            else:
                if input_str[i - 1] != input_str[i] and input_str[i + 1] != input_str[i]:
                    result = result + input_str[i]
        if len(result) == 0:
            print("no")
        else:
            print(result)
    except:
        break
