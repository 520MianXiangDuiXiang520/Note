// 13数列排序.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "pch.h"
#include <iostream>
using namespace std;

int main()
{
	int n;
	cin >> n;
	long long s[220];
	for (int i = 0; i < n; i++)
	{
		long long p;
		cin >> p;
		s[i] = p;
	}
	for (int i = 0; i < n; i++)
	{
		int w = n - i - 1;
		for (int j = 0; j < w ; j++)
		{
			if (s[j] > s[j+1])
			{
				long long tem = s[j];
				s[j] = s[j+1];
				s[j+1] = tem;
			}
		}
	}
	for (int k = 0; k < n; k++)
	{
		cout << s[k]<<" ";
	}
	return 0;
}

