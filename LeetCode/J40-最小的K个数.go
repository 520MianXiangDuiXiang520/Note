// 快排

package main

import "fmt"

type Nums struct {
	arr []int
}

func getMid(nums *Nums, left, right int) int {
	mid := nums.arr[left]
	for left < right {
		for left < right && nums.arr[right] >= mid {
			right--
		}
		nums.arr[left] = nums.arr[right]
		for left < right && nums.arr[left] < mid {
			left++
		}
		nums.arr[right] = nums.arr[left]
	}
	nums.arr[left] = mid
	return left
}

func quickSort(nums *Nums, left, right, k int) {
	if right-left <= 1 {
		return
	}
	mid := getMid(nums, left, right)
	if mid < k {
		quickSort(nums, mid+1, right, k)
	}
	quickSort(nums, left, mid, k)
}

func quickGetLeastNumbers(nums *Nums, k int) []int {
	quickSort(nums, 0, len(nums.arr)-1, k)
	return nums.arr[:k]
}

func getLeastNumbers(arr []int, k int) []int {
	nums := Nums{
		arr: arr,
	}
	res := quickGetLeastNumbers(&nums, k)
	return res
}

func main() {
	fmt.Println(getLeastNumbers([]int{-1, -3, 9, 0, 1, 2, 1, -9}, 2))
}
