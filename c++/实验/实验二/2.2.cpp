#include<iostream>
using namespace std;

void max1(int a,int b,int c)
{
	int max;
	if(a>b)
	{
		max=a;
	}
	else
	{
		max=b;
	}
	if(max<c)
	{
		max=c;
	}
	cout<<"最大值："<<max;
}

void max1(int a,int b)
{
	int max;
	if(a>b)
	{
		max=a;
	}
	else
	{
		max=b;
	}
	cout<<"最大值："<<max;
}
void max1(double a,double b,double c)
{
	double max;
	if(a>b)
	{
		max=a;
	}
	else
	{
		max=b;
	}
	if(max<c)
	{
		max=c;
	}
	cout<<"最大值："<<max;
}

void max1(double a,double b)
{
	double max;
	if(a>b)
	{
		max=a;
	}
	else
	{
		max=b;
	}
	cout<<"最大值："<<max;
}

int main()
{
	cout<<"两个整数"<<endl;
	int a,b;
	cin>>a>>b;
	max1(a,b);
	cout<<"三个整数"<<endl;
	int x,y,z;
	cin>>x>>y>>z;
	max1(x,y,z);

	cout<<"两个双精度"<<endl;
	double a1,b1;
	cin>>a1>>b1;
	max1(a1,b1);
	cout<<"三个双精度"<<endl;
	double x1,y1,z1;
	cin>>x1>>y1>>z1;
	max1(x1,y1,z1);
	return 0;
}
