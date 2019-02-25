//1221是一个非常特殊的数，它从左边读和从右边读是一样的，编程求所有这样的四位十进制数。
#include<stdio.h>
#include<stdlib.h>
int main()
{
	int i = 10;
	int a, b, c;
	for (i = 10; i <= 99; i++)
	{
		a = i / 10;
		b = i - a * 10;
		c = a * 1000 + b * 100 + b * 10 + a;
		printf("%d\n", c);
	}
	system("pause");
	return 0;
}