#include <iostream>
using namespace std;
void  GreedActiveManage(int n,int s[],int f[],bool A[]);
const int n = 11;
int main()
{
    int s[12]={0,1,3,0,5,3,5,6,8,8,2,12},f[12]={0,4,5,6,7,8,9,10,11,12,13,14};
    bool A[n+1];
    GreedActiveManage(n,s,f,A);
    cout<<"最大相容活动安排为："<<endl;
    for(int i=1;i<=n;i++)
    {
       if(A[i])
        {
            cout<<"活动"<<i<<" "<<"活动时间为"<<"("<<s[i]<<","<<f[i]<<")"<<endl;
        }
    }
    return 0;
}
void GreedActiveManage(int n,int s[],int f[],bool A[])
{
    A[1]=true;
    int j=1;
    for (int i=2;i<=n;i++)
    {
		if(s[i]>=f[j])
		{
			A[i]=true ;
			j=i;
		}
		else
		{
			A[i]=false;
		}
    }
}
