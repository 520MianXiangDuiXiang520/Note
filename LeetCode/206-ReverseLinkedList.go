// 反转链表

package main

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func reverseList(head *ListNode) *ListNode {
    if head == nil {
        return head
    }
    pre := head
    this := head.Next
    if this == nil {
        return head
    }
    if this.Next == nil {
        pre.Next = nil
        this.Next = pre
        return this
    }
    next := head.Next.Next
    pre.Next = nil
    for this != nil {
        this.Next = pre
        pre = this
        this = next
        if next != nil {
            next = next.Next
        }
        
    }
    return pre
}