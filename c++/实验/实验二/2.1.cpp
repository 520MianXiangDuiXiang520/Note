#include<iostream>
using namespace std;

double wendu(double F)
{
	return (F-32)*5/9;
}

int main()
{
	
	double F,C;
	cout<<"�����뻪���¶�"<<endl;
	cin>>F;
	C=wendu(F);
	cout<<"�����¶��ǣ�"<<C<<endl;
	return 0;
}
