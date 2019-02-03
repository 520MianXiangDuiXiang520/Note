#include<stdio.h>
#include<stdlib.h>
int main()
{
	int year;
	scanf("%d", &year);
	if (year % 400 == 0)
		printf("yes");
	else
	{
		if (year % 4 == 0 && year % 100 != 0)
			printf("yes");
		else
			printf("no");
	}
	system("pause");
	return 0;
}