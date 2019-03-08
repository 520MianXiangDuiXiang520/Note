#include <iostream>
#include<cmath>
#include<string>
using namespace std;

int main()
{
	string s;
	cin >> s;
	int len;
	long long p=0;
	len = s.length();
	int num[100];
	for (int i = 0; i < len; i++)
	{
		if (s[i] >= 'A'&&s[i] <= 'F')
		{
			num[i] = s[i] - 'A' + 10;
		}
		else
		{
			num[i] = s[i] - '0';
		}
	}
	for (int j = 0; j<len; j++)
	{
		p = p + pow(16, len-j-1) * num[j];
	}
	cout << p;
	return 0;
}