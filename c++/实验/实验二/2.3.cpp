#include<iostream>
using namespace std;

void max1(int a,int b=0)
{
	if(a>b)
	{
		cout<<"������"<<endl;
	}
	else
	{
		cout<<"С����"<<endl;
	}
}

int main()
{
	int a;
	cout<<"������һ������"<<endl;
	cin>>a;
	max1(a);
	return 0;
}
