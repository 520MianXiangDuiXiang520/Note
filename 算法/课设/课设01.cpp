/* 某个整数序列中，去掉0个以上的数字后，剩余的部分就是原序列的子序列。
 * 例如，{7,4,9}、{10,4}、{10,9}等是{10,7,4,9}的子序列。而序列{10, 4, 7}具有不同于原序列的排列顺序，因而不属于{10,7,4,9}的子序列。
 * 严格递增的子序列称为递增子序列。序列的递增子序列中，最长的序列称为最大递增子序列（LIS）。
 * 例如：{5,20,21,22,8,9,10}的最大递增子序列是{5,8,9,10}。（不唯一）
 * 给出以不同数字组成（无重复数字）的序列时，请编写程序，计算此序列的LIS中按照字典序排在第k个位置的LIS。
 */

#include <iostream>
#include <sstream>
#include <string>
#include <algorithm>
#include <windows.h>
#include <stdlib.h>
#include <fstream>
#include <cstdlib>
using namespace std;

// 数字转换为字符串
string IntToString(int num)
{
    stringstream ss;
    string s;
    ss << num;
    ss >> s;
    return s;
}

// 树节点的结构体定义
struct TreeNode
{
    int value;
    int top = 0;                      //标记child列表中最上面元素的索引（栈顶指针）
    string last = IntToString(value); //标记根节点到当前节点的字符串
    int No = -1;                      //标记当前节点值在测试数组中的索引
    int layer;                        // 标记节点层数
    TreeNode *child[50];              //存储子节点的指针数组
};

// 用于存储所有子序列的栈
struct LisStack
{
    string data[1000];
    int top = 0;
};

struct MyList
{
    int value;
    int power;
};

// 自定义排序规则
bool sort_x(string a, string b)
{
    return a < b;
}

// 求出以每一个元素为根节点后的树的最大深度
int TOP = 0;
MyList mylist[501];
int MAXLAYER = 1;
// 创建邻接矩阵，返回一个二维数组
int **CreateTable(const int N, const int list[])
{
    int index;
    int power[501] = {1};
    for (int i = 0; i < N; i++)
    {
        power[i] = 1;
    }
    for (index = N - 1; index >= 0; index--)
    {
        // 判断在该元素后面如果有比他大的，就加一
        for (int j = index; j < N; j++)
        {
            if (list[j] > list[index])
            {
                power[index] = power[j] + 1;
                if (power[index] > MAXLAYER)
                    MAXLAYER = power[index];
                break;
            }
        }
        MyList newvalue;
        newvalue.value = list[index];
        newvalue.power = power[index];
        mylist[TOP] = newvalue;
        TOP++;
    }
    int **table;
    table = (int **)malloc(N * sizeof(int **));
    for (int i = 0; i < N + 1; i++)
        table[i] = (int *)malloc((N + 1) * sizeof(int));

    // 为右上角赋值
    for (int i = 0; i < N; i++)
    {
        for (int j = i; j < N; j++)
        {

            if (table)
            {
                if (list[j] > list[i])
                    table[i][j] = power[i];
                else
                    table[i][j] = 0;
            }
        }
    }
    // 左下角赋值
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j <= i; j++)
            table[i][j] = 0;
    }
    return table;
}

// 创建节点

TreeNode *AddNewNode(int **table, int n, int list[], int index, TreeNode *root)
{
    for (int i = 0; i < n; i++)
    {
        if (table[index][i] >= 1)
        {
            // 创建一个新节点，值是该节点的值
            TreeNode *newChild = new TreeNode();
            if (newChild)
            {
                newChild->value = list[i];
                newChild->No = i;
                newChild->top = 0;
                newChild->last = root->last;
                newChild->last = newChild->last.append(IntToString(list[i]));
                newChild->layer = root->layer + 1;
                root->child[root->top] = (TreeNode *)malloc(sizeof(TreeNode));
                root->child[root->top] = newChild;
                root->top++;
            }
        }
    }
    return root;
}

// 递归为每一个节点创建子节点
void CreateChild(int **table, int list[], int n, TreeNode *root)
{
    for (int i = 0; i < root->top; i++)
    {
        TreeNode *child = AddNewNode(table, n, list, root->child[i]->No, root->child[i]);
        CreateChild(table, list, n, child);
    }
}

// 创建树结构
TreeNode CreateTree(bool isRecursion, int index, TreeNode *root, int n, int list[], int **table)
{
    root->value = list[index];
    root->No = index;
    root->last = IntToString(list[index]);
    root->top = 0;
    root->layer = 1;
    AddNewNode(table, n, list, root->No, root);
    CreateChild(table, list, n, root);
    return *root;
}

// 输出树
void PrintTree(TreeNode *root)
{
    if (root->top != 0)
    {
        for (int x = 0; x < root->top; x++)
        {
            for (int i = 0; i < root->child[x]->layer; i++)
            {
                cout << "* ";
            }
            cout << root->child[x]->value << endl;
            PrintTree(root->child[x]);
        }
    }
}

// 得到所有递增子序列
LisStack LisList;
void GetAllIS(TreeNode *root)
{
    if (root->top != 0)
    {
        for (int i = 0; i < root->top; i++)
        {

            GetAllIS(root->child[i]);
        }
    }
    else
    {
        LisList.data[LisList.top] = root->last;
        LisList.top++;
    }
}

// 得到第K的最长递增子序列
string *GetLisKth(int k, bool isK)
{
    int MaxLength = 0;
    for (int i = 0; i < LisList.top; i++)
    {
        if (LisList.data[i].length() > MaxLength)
        {
            MaxLength = LisList.data[i].length();
        }
    }

    string LIS[100];
    int top = 0;
    for (int i = 0; i < LisList.top; i++)
    {
        if (LisList.data[i].length() == MaxLength)
        {
            LIS[top] = LisList.data[i];
            top++;
        }
    }
    sort(LIS, LIS + top, sort_x);
    if (isK)
    {
        if (k > top - 1)
        {
            cout << "最长子序列只有" << top << "个，输入范围应该是（0-" << top - 1 << "),是否全部输出（y/s）";
            string yors;
            cin >> yors;
            if (yors == "y" || yors == "Y")
            {
                cout << "所有最大递增子序列如下：" << endl;
                for (int i = 0; i < top; i++)
                {
                    cout << LIS[i] << "   ";
                }
                cout << endl;
            }
            else if (yors == "n" || yors == "N")
            {
                cout << "请重新输入k：";
                int k2;
                cin >> k2;
                if (k2 <= top)
                    cout << "第" << k << "个最大递增子序列是：" << LIS[k2];
                else
                    cout << "输入有误！！！" << endl;
            }
            else
                cout << "输入有误！！！" << endl;
        }
        else
            cout << "第" << k << "个最大递增子序列是：" << LIS[k] << "   top=" << top;
    }
    else
    {
        cout << "所有最大递增子序列如下：" << endl;
        for (int i = 0; i < top; i++)
        {
            cout << LIS[i] << "   ";
        }
        cout << endl;
    }
    return LIS;

    /**/
}

void Show()
{
    cout << endl;
    cout << "                          ------------------------------------------------------------------" << endl
         << endl;
    cout << "                                                  ** 算法课设 **" << endl
         << endl;

    cout << "                                  1. 从文件读取数据" << endl;
    cout << "                                  2. 输入数据" << endl;
    cout << "                                  3. 退出" << endl
         << endl;
    cout << "                               请选择你要进行的操作：";
}

int Return()
{
    int b;
    cout << endl
         << "输入任意数字返回上一级" << endl;
    cin >> b;
    return b;
}

void Show3(int list[], int N, int **table, TreeNode *root, int k, TreeNode TreeList[])
{
    cout << endl;
    cout << "                          ------------------------------------------------------------------" << endl
         << endl;
    cout << "                                                  ** 算法课设 **" << endl
         << endl;

    cout << "                                  1. 输出测试数组" << endl;
    cout << "                                  2. 输出邻接矩阵" << endl;
    cout << "                                  3. 显示树结构" << endl;
    cout << "                                  4. 输出所有最长递增子序列" << endl;
    cout << "                                  5. 输出第K个最长递增子序列" << endl;
    cout << "                                  6. 退出" << endl
         << endl;
    cout << "                              请选择你要进行的操作：";

    int chose3 = 0;
    cin >> chose3;
    switch (chose3)
    {
    case 1:
    {
        // 输出测试数组
        system("cls");
        cout << endl
             << "测试数组为：" << endl;
        for (int i = 0; i < N; i++)
        {
            cout << list[i] << "   ";
        }
        if (Return())
        {
            system("cls");
            Show3(list, N, table, root, 1, TreeList);
        }
    };
    break;
    case 2:
    {
        // 输出邻接矩阵
        system("cls");
        cout << endl
             << "邻接矩阵为：" << endl
             << endl;
        cout << "  | ";
        for (int i = 0; i < N; i++)
        {
            cout << list[i] << "   ";
        }
        cout << endl
             << "--+------------------------------" << endl;
        for (int i = 0; i < N; i++)
        {
            cout << list[i] << " | ";
            for (int j = 0; j < N; j++)
            {
                cout << table[i][j] << "   ";
            }
            cout << endl;
        }
        if (Return())
        {
            system("cls");
            Show3(list, N, table, root, 1, TreeList);
        }
    };
    break;
    case 3:
    {
        // 显示树结构
        system("cls");
        cout << root->value << endl;
        for (int i = 0; i < N - MAXLAYER; i++)
        {
            cout << "以第" << i << "个元素建立的树为：" << endl
                 << "-" << TreeList[i].value << endl;
            PrintTree(&TreeList[i]);
        }
        if (Return())
        {
            system("cls");
            Show3(list, N, table, root, 1, TreeList);
        }
    };
    break;
    case 4:
    {
        // 输出所有最长递增子序列
        system("cls");
        GetLisKth(1, false);
        if (Return())
        {
            system("cls");
            Show3(list, N, table, root, 1, TreeList);
        }
    };
    break;
    case 5:
    {
        // 输出第K个最长递增子序列
        system("cls");
        cout << "请输入K：";
        int ik;
        cin >> ik;
        GetLisKth(ik, true);
        if (Return())
        {
            system("cls");
            Show3(list, N, table, root, 1, TreeList);
        }
    };
    break;
    case 6:
    {
        exit(1);
    };
    break;
    }
}

void ShowLis(int list[], int n)
{
    int **table;
    TreeNode Root;
    TreeNode pp;
    TreeNode TreeList[501];
    int TreeNum = 0;
    table = CreateTable(n, list);
    for (int index = 0; index < n; index++)
    {
        if (mylist[n - index - 1].power == MAXLAYER)
        {
            pp = CreateTree(false, index, &Root, n, list, table);
            TreeList[TreeNum] = pp;
            TreeNum++;
            GetAllIS(&pp);
        }
    }
    Show3(list, n, table, &pp, 1, TreeList);
}

void CinShow()
{
    int N = 0;
    int list[500];
    cout << endl;
    cout << "                          ------------------------------------------------------------------" << endl
         << endl;
    cout << "                                                  ** 输入数据 **" << endl
         << endl;
    cout << "  请输入要测试的数组长度：";
    cin >> N;
    cout << "  请输入测试数组，按空格隔开：" << endl;
    for (int i = 0; i < N; i++)
    {
        cin >> list[i];
    }
    system("cls");
    ShowLis(list, N);
}

void File()
{
    ifstream examplefile("File.txt");
    if (!examplefile.is_open())
    {
        cout << "Error opening file";
        exit(1);
    }
    int N;
    int list[501] = {0};
    examplefile >> N;
    for (int i = 1; i < N + 1; i++)
    {
        examplefile >> list[i - 1];
    }
    ShowLis(list, N);
}

int main()
{
    system("color 8E");
    Show();
    int c1 = 0;
    cin >> c1;
    switch (c1)
    {
    case 1:
    {
        // 从文件中获取数组信息
        system("cls");
        File();
    };
    break;
    case 2:
    {
        system("cls");
        CinShow();
    };
    break;
    case 3:
    {
        exit(1);
    };
    break;
    }
    return 0;
}
