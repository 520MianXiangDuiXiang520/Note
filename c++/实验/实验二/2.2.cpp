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
	cout<<"���ֵ��"<<max;
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
	cout<<"���ֵ��"<<max;
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
	cout<<"���ֵ��"<<max;
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
	cout<<"���ֵ��"<<max;
}

int main()
{
	cout<<"��������"<<endl;
	int a,b;
	cin>>a>>b;
	max1(a,b);
	cout<<"��������"<<endl;
	int x,y,z;
	cin>>x>>y>>z;
	max1(x,y,z);

	cout<<"����˫����"<<endl;
	double a1,b1;
	cin>>a1>>b1;
	max1(a1,b1);
	cout<<"����˫����"<<endl;
	double x1,y1,z1;
	cin>>x1>>y1>>z1;
	max1(x1,y1,z1);
	return 0;
}
