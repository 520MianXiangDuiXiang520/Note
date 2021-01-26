#include<iostream>
#include<thread>
#include<mutex>
#include<list>
#include <condition_variable>
#include<Windows.h>
using namespace std;

// 作为临界资源
typedef list<int> LISTINT;
list<int> q;
LISTINT::iterator i;

mutex LOCK;
condition_variable condition;  // 信号量

void printList()
{
	for (i = q.begin(); i != q.end(); ++i)
		cout << *i << " ";
	cout << endl;
}

void func1()
{
    // 生产者线程，要求队列中元素最多只能有20个	
	while (1)
	{
		unique_lock<mutex> lck(LOCK);

		q.push_back(1);  // 向队列尾部加入元素（以1充当信号）
		this_thread::sleep_for(chrono::milliseconds(60));
		cout << "生产者" << q.size() << "当前队列元素：";
		printList();

		condition.notify_all();  // 唤醒消费者线程
		if (q.size() >= 20) 
		{
			// 如果队列中元素大于20（缓冲区满），生产者阻塞，唤醒消费者
			condition.notify_all();
			condition.wait(lck);
		}
	}
}

void func2()
{
	// 作为消费者线程，队列中最少要有10个元素
	while (1)
	{
		unique_lock<mutex> lck(LOCK);
		if (q.size() == 0) {
			// 判断队列中是否有元素可取
			condition.notify_all();
			condition.wait(lck);
		}
		condition.notify_all();
		
		if(q.size()>0)
			q.pop_front();
		this_thread::sleep_for(chrono::milliseconds(20));
		cout << "消费者" << q.size() << "当前队列元素：";
		printList();
	}
}

int main()
{
	thread t1(func1);
	thread t2(func2);
	t1.join();
	t2.join();
	system("pause");
	return 0;
}

