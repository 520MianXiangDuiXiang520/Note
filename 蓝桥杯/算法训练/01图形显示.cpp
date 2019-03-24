// 图形显示.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "pch.h"
#include <iostream>
using namespace std;

int main()
{
	int n,i,j;
	cin >> n;
	for (i = 0; i < n; i++)
	{
		for (j = 0; j < n - i; j++)
		{
			cout << "* ";
		}
		cout << endl;
	}

	return 0;
}


