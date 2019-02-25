//153是一个非常特殊的数，它等于它的每位数字的立方和，即153=1*1*1+5*5*5+3*3*3。编程求所有满足这种条件的三位十进制数

#include<stdio.h>
int main()
{
	int i = 100;
	int a, b, c;
	for (i = 100; i <= 999; i++)
	{
		a = i / 100;
		b = (i - a * 100) / 10;
		c = (i - a * 100 - b * 10);
		if(a*a*a+b*b*b+c*c*c==i)
			printf("%d\n",i);
	}
	return 0;
}