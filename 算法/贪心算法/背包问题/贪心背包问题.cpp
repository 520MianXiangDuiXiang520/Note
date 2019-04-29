// 贪心背包问题.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <algorithm>
#include"shop.h"

bool mysort(Shop a, Shop b)
{
	return a.vw_ratio > b.vw_ratio;
}

int main()
{
	Shop shoplist[100];
	int w, v,count;
	string n;
	int C;
	int i = 0;
	float s;
	int valuesum = 0;
	cout << "请输入背包容量：  ";
	cin >> C;
	cout << "请输入商品个数：  ";
	cin >> count;
	cout << "请输入商品信息："<<endl;
	cout << "   重量   " << "   价值   " << "   名称   " << endl;
	for (int i = 0; i < count ; i++)
	{
		cin >> w >> v >> n;
		shoplist[i].set(w,v,n);
	}
	cout << "未排序之前：" << endl;
	for (int i = 0; i < 3; i++)
	{
		shoplist[i].print();
	}
	sort(shoplist, shoplist + 3, mysort);
	cout << "排序之后：" << endl;
	for (int i = 0; i < 3; i++)
	{
		shoplist[i].print();
	}
	
	 while (C > 0)
	 {
		 if (shoplist[i].weight < C)
		 {
			 valuesum += shoplist[i].value;
			 C -= shoplist[i].weight;
			 cout << "第" << i << "次选择1个" << shoplist[i].name << "总价值：" << valuesum << "剩余空间："<<C<<endl;
			 i++;
		 }
		 else
		 {
			 s = float(C) / float(shoplist[i].weight);
			 valuesum += s * shoplist[i].value;
			 C -= s * shoplist[i].weight;
			 cout << "第" << i << "次选择"<<s<<"个" << shoplist[i].name << "总价值：" << valuesum << "剩余空间：" << C << endl;
			 i++;
		 }
	 }
	return 0;
}


