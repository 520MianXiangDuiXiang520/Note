import datetime
name = "zings"
age = 17
date = datetime.date(2019,7,18)
print(f'my name is {name}, this year is {date:%Y},Next year, I\'m {age+1}')  # my name is zings, this year is 2019,Next year, I'm 18
money = 19999999877
print(f'{money:,}')
print(f'{name:^18}')
print(f'{money:+}')
