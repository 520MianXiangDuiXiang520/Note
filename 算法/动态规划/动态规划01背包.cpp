#include<iostream>
using namespace std;
int m[10][50];
int x[10] = { -1 };

int Mymin(int a,int b)
{
	if (a < b)
		return a;
	else
		return b;
}

int Mymax(int a, int b)
{
	if (a > b)
		return a;
	else
		return b;
}

int Knapsack(int v[], int w[], int c, int n)
{
	int jMax = Mymin(w[n] - 1, c);
	for (int j = 0; j <= jMax; j++)
		m[n][j] = 0;
	for (int j = w[n]; j <= c; j++)
		m[n][j] = v[n];

	for (int i = n - 1; i > 1; i--)
	{
		jMax = Mymin(w[i] - 1, c);
		for (int j = 0; j <= jMax; j++)
			m[i][j] = m[i + 1][j];
		for (int j = w[i]; j <= c; j++)
			m[i][j] = Mymax(m[i + 1][j], m[i + 1][j - w[i]] + v[i]);
	}
	
	if (c >= w[1])
		m[1][c] = Mymax(m[1][c], m[2][c - w[1]] + v[1]);
	return m[1][c];
}
void Traceback(int w[], int c, int n)
{
	for (int i = 1; i < n; i++) {
		if (m[i][c] == m[i + 1][c])
			x[i] = 0;
		else {
			x[i] = 1;
			c -= w[i];
		}
	}
	x[n] = m[n][c] ? 1 : 0;
}

int main() {
	int weight[6] = { 0,2,2,6,5,4 };
	int value[6] = { 0,6,3,5,4,6 };
	int c = 10;
	cout << "总价值最大为：" << Knapsack(value, weight, c, 5) << endl;
	Traceback(weight, c, 5);
	cout << "最优值的解：";
	for (int i = 1; i < 5 + 1; i++)
		cout << x[i] << " ";
	cout << endl;
	return 0;
}