#include<iostream>
using namespace std;

int main()
{
	cout<<"请输入图形类型"<<endl<<"1.圆形"<<endl<<"2.矩形"<<endl<<"3.正方形"<<endl;
	int type;
	cin>>type;
	int r,a,b;
	double sq=0;
	const double PI=3.14159;
	switch(type)
	{
	case(1):
		{
			cout<<"请输入圆的半径"<<endl;
			cin>>r;
			sq=PI*r*r;
			cout<<"圆的面积是："<<sq<<endl;
		}break;
	case(2):
		{
			cout<<"请输入矩形的长，宽"<<endl;
			cin>>a>>b;
			sq=a*b;
			cout<<"矩形的面积是："<<sq<<endl;
		}break;
	case(3):
		{
			cout<<"请输入正方形的边长"<<endl;
			cin>>r;
			sq=r*r;
			cout<<"正方形的面积是："<<sq<<endl;
		}break;
	}
	
	return 0;
}
