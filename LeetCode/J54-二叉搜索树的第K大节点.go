/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
var i, res int
func recover(root *TreeNode) {
    if root == nil {
        return
    }
    recover(root.Right)
    i--
    // fmt.Println(root.Val, i)
    if i == 0 {
        res = root.Val
        return
    }
    recover(root.Left)
}
func kthLargest(root *TreeNode, k int) int {
    i = k
    recover(root)
    return res
}