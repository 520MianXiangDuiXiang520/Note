#include<stdio.h>
#include<stdlib.h>

int main()
{
	int n, m;//行，列
	scanf("%d%d", &n, &m);
	char str[32][32];
	//A的位置
	int i,j;
	for (i = 0;i < n; i++)
	{
		for (j = 0; j < m; j++)
		{
			if (i == j)
				str[i][j] = 'A';
			else if (i > j)
				str[i][j] = 'A' + (i-j);
			else
				str[i][j] = 'A' + (j-i);
		}
		
	}
	for (i = 0; i < n; i++)
	{
		for (j = 0; j < m; j++)
			printf("%c", str[i][j]);
		printf("\n");
	}
		
	system("pause");
	return 0;
}