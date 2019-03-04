#include<iostream>
#include<string>
using namespace std;

int main()
{
	string str1,str2;
	cout<<"iÇëÊäÈë×Ö·û´®1"<<endl;
	cin>>str1;
	cout<<"ÇëÊäÈë×Ö·û´®2"<<endl;
	cin>>str2;
	if(str1.size()<str2.size())
	{
		string p=str1;
		str1=str2;
		str2=p;
	}
	int max_len=0;
	string max_temp;
	for(int start=0;start<str1.size();start++)
	{
		for(int end=0;end<str1.size();end++)
		{
			string temp=str1.substr(start,end);
			int pos=str2.find(temp);
			if(pos>=0)
			{
				if(temp.size()>max_len)
				{
					max_len=temp.size();
					max_temp=temp;
				}

			}
		}
	}
	cout<<max_temp<<endl;
	return 0;
}