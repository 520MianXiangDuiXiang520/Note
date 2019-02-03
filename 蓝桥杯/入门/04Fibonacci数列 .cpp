#include<stdio.h>
#include<stdlib.h>
int main()
{
	long long F[3];
	F[0] = 1;
	F[1] = 1;
	long long i;
	long long n;
	scanf("%I64d", &n);
	if (n == 1 || n == 2)
	{
		printf("%I64d", F[0] % 10007);
	}
	else {
		for (i = 3; i <= n; i++)
		{
			F[2] = (F[0] + F[1])%10007;
			F[0] = F[1];
			F[1] = F[2];
			printf("%I64d   ", F[2]);
		}
		printf("%I64d", F[2]);
	}
	system("pause");
	return 0;
}