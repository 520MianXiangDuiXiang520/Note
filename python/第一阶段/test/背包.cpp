#include<iostream>
using namespace std;
const int MAX = 1024;
int n; 
int c; 
int value[MAX];
int weight[MAX];
int x[MAX];
int m[MAX][MAX];
void Input()
{
	printf("输入物品个数和背包容量:\n");
    scanf("%d%d", &n, &c);
    for(int i = 1; i <= n; i++)
        scanf("%d%d",&weight[i],&value[i]);
}
void Knapsack()
{
    int jmax = min(c, weight[n] - 1);
    for(int j = 0; j <= jmax;j++)
        m[n][j] = 0;
    for(int j = weight[n]; j <= c;j++)
        m[n][j] = value[n];
    for(int i = n - 1; i > 1;i--)
    {
        jmax = min(c, weight[i] - 1);
        for(int j = 0; j <= jmax;j++)
            m[i][j] = m[i + 1][j];
        for(int j = weight[i]; j <= c;j++)
            m[i][j] = max(m[i + 1][j], m[i + 1][j - weight[i]] + value[i]);
    }
    m[1][c] = m[2][c];
    if(c >= weight[1])
        m[1][c] = max(m[1][c], m[2][c - weight[1]] + value[1]);
}
void Traceback()
{
	int t=c;
    for(int i = 1; i < n; i++)
	{
        if(m[i][t] == m[i + 1][t])
           x[i] = 0;
        else
        {
            x[i] = 1;
            t -= weight[i];
        }
	}
    x[n] = (m[n][t]) ? 1 : 0;
}
void Output()
{
    cout << "最优解为 : " << m[1][c] << endl;
    cout << "选择的物品的序号为 :" << endl;
    for(int i = 1; i <= n; i++)
        if(x[i] == 1)
         cout << i << " ";
    cout << endl;
}
int main()
{
    Input();
    Knapsack();
    Traceback();
    Output();
}
