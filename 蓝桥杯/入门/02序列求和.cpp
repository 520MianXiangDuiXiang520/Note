#include<stdio.h>
#include<stdlib.h>
int main()
{
	long long n;
	scanf("%I64d", &n);
	long long sum ;
	sum = ((n + 1)*n) / 2;
	printf("%I64d",sum);
	system("pause");
	return 0;
}