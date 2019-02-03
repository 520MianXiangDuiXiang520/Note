#include<stdio.h>
#include<stdlib.h>
int main()
{
	int n,i;
	int j = 0;
	scanf("%d", &n);
	int a[10001];
	for (i = 0; i < n; i++)
	{
		scanf("%d", &a[i]);
	}
	int max, min;
	long long sum = a[0];
	max = a[0];
	min = a[0];
	for (i = 1; i < n; i++)
	{
		if (max < a[i])
			max = a[i];
		if (min > a[i])
			min = a[i];
		sum += a[i];
	}

	printf("%d\n", max);
	printf("%d\n", min);
	printf("%I64d\n", sum);
	system("pause");
	return 0;
}