#include<iostream>
using namespace std;

int main()
{
	cout<<"������ͼ������"<<endl<<"1.Բ��"<<endl<<"2.����"<<endl<<"3.������"<<endl;
	int type;
	cin>>type;
	int r,a,b;
	double sq=0;
	const double PI=3.14159;
	switch(type)
	{
	case(1):
		{
			cout<<"������Բ�İ뾶"<<endl;
			cin>>r;
			sq=PI*r*r;
			cout<<"Բ������ǣ�"<<sq<<endl;
		}break;
	case(2):
		{
			cout<<"��������εĳ�����"<<endl;
			cin>>a>>b;
			sq=a*b;
			cout<<"���ε�����ǣ�"<<sq<<endl;
		}break;
	case(3):
		{
			cout<<"�����������εı߳�"<<endl;
			cin>>r;
			sq=r*r;
			cout<<"�����ε�����ǣ�"<<sq<<endl;
		}break;
	}
	
	return 0;
}
