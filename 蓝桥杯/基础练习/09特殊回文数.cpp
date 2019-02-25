//123321是一个非常特殊的数，它从左边读和从右边读是一样的。输入一个正整数n， 编程求所有这样的五位和六位十进制数，满足各位数字之和等于n 。
#include<iostream>
using namespace std;

int main()
{
	int n;
	int i, j, k;
	cin >> n;
	for (i = 1; i <= 9; i++)
		for (j = 0; j <= 9; j++)
			for (k = 0; k <= 9; k++)
				if (i + j + k + i + j == n)
					cout << i << j << k << j << i << endl;
	for (i = 1; i <= 9; i++)
		for (j = 0; j <= 9; j++)
			for (k = 0; k <= 9; k++)
				if (i + j + k + i + j+k == n)
					cout << i << j << k << k<<j << i << endl;

	return 0;
}