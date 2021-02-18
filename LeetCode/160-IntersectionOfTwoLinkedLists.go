// 相交链表
// 链表，找环

package main

// 如果命运注定我们有交集，能有同一段未来，那么我们只需要彼此不断努力前进。🦄
// 在到达终点后，我们可以重新来到起点重新出发。😋
// 暂时没有会面也没有关系，在没有遇见你的日子里，我还是在勇敢地独自向前。😉
// 因为我知道，我们注定会在那个初识的地点，相遇并共同走过往后的路。🥰

// 如果命运告诉我们注定无法相遇，我们依然需要坚持着前进。😥
// 终有一天，我们还是会同时到达终点，哪怕我们共同终点，是归于null。

// 隐约雷鸣，阴霾天空，即使天无雨，我亦留此地。  --《万叶集》

func getIntersectionNode(headA, headB *ListNode) *ListNode {
    a, b := headA, headB
    for a != b {
        if a == nil {
            a = headB
        } else {
            a = a.Next
        }
        if b == nil {
            b = headA
        } else {
            b = b.Next
        }
    }
    return a
}