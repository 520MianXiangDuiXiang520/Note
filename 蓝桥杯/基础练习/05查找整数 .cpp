#include<stdio.h>
#include<stdlib.h>
int main()
{
	int next[1001];
	int n;
	scanf("%d", &n);
	int i;
	for (i = 0; i < n; i++)
		scanf("%d", &next[i]);
	int f;
	scanf("%d", &f);
	for (i = 0; i < n; i++)
	{
		if (next[i] == f)
			break;
	}
	if (i == n)
		printf("-1");
	else
		printf("%d", i+1);
	system("pause");
	return 0;
}