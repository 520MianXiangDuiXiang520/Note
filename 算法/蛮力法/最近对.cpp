// 最近对.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "pch.h"
#include <iostream>
#include <time.h>
#include <math.h>
#include <graphics.h>
#include <conio.h>
using namespace std;

class Point
{
  public:
	int x;
	int y;
	void Print()
	{
		cout << x << ":" << y << endl;
	}
};
//随机产生一个点
Point get_xy(Point P)
{
	P.x = rand() % 1500;
	P.y = rand() % 800;
	return P;
}

int main()
{
	Point P;
	Point s[100];
	int min = 100000;
	int n, i, j;
	int he1, he2, a, b, c;
	int v;
	Point A, min_A, min_B;
	cout << "请输入随机生成的点的个数" << endl;
	cin >> n;
	initgraph(1500, 800);
	for (i = 0; i < n; i++)
	{
		A.x = 0;
		A.y = 0;
		A = get_xy(A);
		s[i] = A;
		circle(A.x, A.y, 5);
	}

	for (i = 0; i < n; i++)
	{
		for (j = i + 1; j < n; j++)
		{
			he1 = s[i].x - s[j].x;
			he2 = s[i].y - s[j].y;
			c = pow(he1, 2) + pow(he2, 2);
			v = sqrt(c);
			if (v < min)
			{
				min = v;
				min_A = s[i];
				min_B = s[j];
			}
		}
	}
	setlinecolor(RGB(255, 144, 144));
	setfillcolor(RGB(255, 144, 0));
	fillcircle(min_A.x, min_A.y, 5);
	fillcircle(min_B.x, min_B.y, 5);
	line(min_A.x, min_A.y, min_B.x, min_B.y);
	//printf("\n\n最近对为：(%d,%d)，(%d,%d),距离是 %d ", min_A.x, min_A.y, min_B.x, min_B.y, min);
	_getch();	 // 按任意键继续
	closegraph(); // 关闭绘图窗口
	return 0;
}
