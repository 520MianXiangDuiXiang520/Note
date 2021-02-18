package main

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteNode(head *ListNode, val int) *ListNode {
    if head.Val == val {
        return head.Next
    }
    sp := head
    for sp.Next != nil && sp.Next.Val != val {
        sp = sp.Next
    }
    sp.Next = sp.Next.Next
    return head

}