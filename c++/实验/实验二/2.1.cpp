#include<iostream>
using namespace std;

double wendu(double F)
{
	return (F-32)*5/9;
}

int main()
{
	
	double F,C;
	cout<<"请输入华氏温度"<<endl;
	cin>>F;
	C=wendu(F);
	cout<<"摄氏温度是："<<C<<endl;
	return 0;
}
