# include<stdio.h>
# include<stdlib.h>
# include<time.h>
# include<math.h>

struct Point
{
	int x;
	int y;
};

//随机产生一个点
Point get_xy(Point P)
{
	//以系统时间作为随机种子
	srand((unsigned)time(NULL));
	P.x = rand() % 100;
	P.y = rand() % 100;
	_sleep(1000);
	return P;
}

int main()
{	
	int min = 100000;
	int n,i,j;
	int he1, he2, a, b, c;
	int v;
	Point A, min_A,min_B;
	Point s[100];
	printf("请输入随机生成的点的个数：\n");
	scanf("%d", &n);
	printf("随机生成的 %d 个点为：\n\n",n);
	for (i = 0; i < n; i++)
	{
		A.x = 0;
		A.y = 0;
		A = get_xy(A);
		s[i] = A;
		printf("(%d,%d)", A.x, A.y);
	}
	printf("\n\n");

	for (i = 0; i < n; i++)
	{
		for (j = i + 1; j < n; j++)
		{
			he1 = s[i].x - s[j].x;
			he2 = s[i].y - s[j].y;
			c = pow(he1, 2) + pow(he2, 2);
			v = sqrt(c);
			
			printf("(%d,%d)与(%d,%d)之间的距离是 %t\t ", s[i].x, s[i].y, s[j].x, s[j].y, v);
			if (v < min)
			{
				min = v;
				min_A = s[i];
				min_B = s[j];
			}
		}
	}
	printf("\n\n最近对为：(%d,%d)，(%d,%d),距离是 %d ", min_A.x, min_A.y,min_B.x,min_B.y,min);
	system("pause");
	return 0;
}