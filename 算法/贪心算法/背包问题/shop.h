#pragma once
#include <string>
#include<iostream>
using namespace std;

class Shop
{
public:
	string name;
	float vw_ratio;
	int weight;
	int value;
	void set(int w, int v, string n);
	void print();
};