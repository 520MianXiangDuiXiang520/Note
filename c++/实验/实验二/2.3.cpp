#include<iostream>
using namespace std;

void max1(int a,int b=0)
{
	if(a>b)
	{
		cout<<"大于零"<<endl;
	}
	else
	{
		cout<<"小于零"<<endl;
	}
}

int main()
{
	int a;
	cout<<"请输入一个整数"<<endl;
	cin>>a;
	max1(a);
	return 0;
}
