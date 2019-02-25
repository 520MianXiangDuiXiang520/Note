// 十进制转十六进制.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。


#include "pch.h"
#include <iostream>
using namespace std;

int main()
{
	int n,a,b,c,i;
	char s[30];
	c = 0;
	cin >> n;
	if (n == 0)
		cout << "0" << endl;
	else
	{
		while (n != 0)
		{
			a = n / 16;
			b = n - a * 16;
			if (b >= 10)
				b = 'A' + b - 10;
			else
				b = '0'+b;

			s[c++] = b;
			n = a;
		}
		
	}
	for (i = c - 1; i >= 0; i--)
		cout << s[i];
	return 0;
}

