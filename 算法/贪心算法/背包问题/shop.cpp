#include"shop.h"

void Shop::set(int w, int v, string n)
{
	weight = w;
	value = v;
	name = n;
	vw_ratio = float(v) / float(w);
}

void Shop::print()
{
	cout << name << " : " << "    weight: " << weight << "    value: " << value <<"    VW_ratio: "<<vw_ratio<< endl;
}