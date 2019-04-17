#include <cmath>
#include <iostream>
#include <algorithm>
#include <ctime>
#include <graphics.h>
#include <conio.h>

using namespace std;

constexpr auto MAXSIZE = 100.0;
constexpr auto MAX = 10000000;
constexpr auto HEIGHT = 800;
constexpr auto WIDTH = 1500;

typedef struct Point
{
    // 二维坐标上的点Point
    double x;
    double y;
} Point;

//计算距离
double Distance(Point a, Point b)
{
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

//按x坐标排序
bool sort_x(Point a, Point b)
{
    return a.x < b.x;
}

float ClosestPair(Point points[], int length, Point &a, Point &b)
{
    double min_len;
    double d1, d2;
    int i = 0, j = 0, k = 0, x = 0;
    Point a1, b1, a2, b2;

    if (length < 2)
        return MAX; //若子集长度小于2，定义为最大距离，表示不可达
    else if (length == 2)
    {
        a = points[0];
        b = points[1];
        min_len = Distance(points[0], points[1]);
    }
    else
    {
        Point *point_left = new Point[length];
        Point *point_right = new Point[length];

        //求中位数用来分割
        sort(points, points + length, sort_x);
        double mid = points[(length - 1) / 2].x;

        for (i = 0; i < length / 2; i++)
            point_left[i] = points[i];
        for (int j = 0, i = length / 2; i < length; i++)
            point_right[j++] = points[i];

        d1 = ClosestPair(point_left, length / 2, a1, b1);
        d2 = ClosestPair(point_right, length - length / 2, a2, b2);

        //记录最近点，最近距离
        if (d1 < d2)
        {
            min_len = d1;
            a = a1;
            b = b1;
        }
        else
        {
            min_len = d2;
            a = a2;
            b = b2;
        }

        Point *point_mid = new Point[length];

        for (i = 0, k = 0; i < length; i++)
            if (abs(points[i].x - mid) <= min_len)
                point_mid[k++] = points[i];

        //sort(point_mid, point_mid + k, sort_y);                                       // 以y排序矩形阵内的点集合

        //只从左半部分取出点和右半部分的点比较
        for (i = 0; i < k; i++)
        {
            if (point_mid[j].x - mid >= 0)
                continue;
            x = 0;
            for (j = i + 1; j < k; j++)
            {
                if (point_mid[j].x - mid < 0)
                {
                    x++;
                    continue;
                }
                if (Distance(point_mid[i], point_mid[j]) < min_len)
                {
                    min_len = Distance(point_mid[i], point_mid[j]);
                    a = point_mid[i];
                    b = point_mid[j];
                }
            }
        }
    }
    return min_len;
}

void SetPoints(Point *points, int length)
{
    srand(unsigned(time(NULL)));
    for (int i = 0; i < length; i++)
    {
        points[i].x = (rand() % WIDTH);
        points[i].y = (rand() % HEIGHT);
    }
}

int main()
{
    int num;         //随机生成的点对个数
    Point a, b;      //最近点对
    double diatance; //点对距离

    cout << "请输入二维点对个数:";
    cin >> num;
    initgraph(WIDTH, HEIGHT);
    setlinecolor(RGB(0, 0, 195));
    setfillcolor(RGB(0, 0, 195));
    setbkcolor(RGB(195, 195, 195));
    cleardevice();
    if (num < 2)
        return -1;
    else
    {
        Point *points = new Point[num];

        SetPoints(points, num);
        for (int i = 0; i < num; i++)
            circle(points[i].x, points[i].y, 5);
        diatance = ClosestPair(points, num, a, b);
    }
    TCHAR s[20];
    _stprintf_s(s, _T("%lf"), diatance); // 高版本 VC 推荐使用 _stprintf_s 函数
    TCHAR title[] = _T("最短距离");

    outtextxy(20, 80, s);
    outtextxy(10, 60, title);
    line(a.x, a.y, b.x, b.y);
    _getch();     // 按任意键继续
    closegraph(); // 关闭绘图窗口
    system("pause");
}
