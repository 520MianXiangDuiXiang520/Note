package main

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func trimBST(root *TreeNode, low int, high int) *TreeNode {
	for {
		if root == nil {
			return nil
		}
		if root.Val < low {
			root = root.Right
		} else if root.Val > high {
			root = root.Left
		} else {
			break
		}
	}
	root.Left = trimBST(root.Left, low, high)
	root.Right = trimBST(root.Right, low, high)
	return root
}
