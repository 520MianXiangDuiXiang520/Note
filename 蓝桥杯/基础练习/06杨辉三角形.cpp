#include<stdio.h>
#include<stdlib.h>
int main()
{
	int n;
	scanf("%d", &n);
	int yang[34][34];
	int i,j;
	for (i = 0; i < n; i++)
		for (j = 0; j < n; j++)
			if (j == 0 || j == i)
				yang[i][j] = 1;
			else
				yang[i][j] = 0;
	for (i = 2; i < n; i++)
		for (j = 1; j < n; j++)
			if (i > j)
				yang[i][j] = yang[i - 1][j - 1] + yang[i - 1][j];
	for (i = 0; i < n; i++)
	{
		for (j = 0; j < n; j++)
		{
			
			if (i >= j)
				printf("%d ",yang[i][j]);
		}
		printf("\n");
	}
	system("pause");
	return 0;
}