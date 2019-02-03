#include<stdio.h>
#include<stdlib.h>

int main()
{
	int r;
	double PI = 3.14159265358979323;
	scanf("%d", &r);
	double m;
	m = PI * r*r;
	printf("%.7lf", m);
	system("pause");
	return 0;
}