#include<stdio.h>
#include<stdlib.h>

void dd(int a,int er[])
{
	int r, j;
	int i = 4;
	while (a != 0)
	{
		r = a % 2;
		er[i] = r;
		a = (a - r) / 2;
		i--;
	}
	for (j = 0; j < 5; j++)
	{
		printf("%d", er[j]);
	}
	printf("\n");
}
int main()
{
	int er[5] = { 0,0,0,0,0 };
	int i = 4;
	int p = 0;
	for(p=0;p<32;p++)
		dd(p, er);
	system("pause");
	return 0;
}