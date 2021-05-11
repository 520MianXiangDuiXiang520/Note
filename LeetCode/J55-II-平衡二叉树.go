/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */

func getDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }
    depth := 1
    left := getDepth(root.Left)
    right := getDepth(root.Right)
    if left > right {
        depth +=  left
    } else {
        depth += right
    }
    return depth
}
func isBalanced(root *TreeNode) bool {
    if root == nil {
        return true
    }
    left := getDepth(root.Left)
    right := getDepth(root.Right)
   
    return left - right <= 1 && left - right >= -1 && isBalanced(root.Left) && isBalanced(root.Right)
}