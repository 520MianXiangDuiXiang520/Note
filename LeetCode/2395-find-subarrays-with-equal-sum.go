package main

func findSubarrays(nums []int) bool {
	dict := make(map[int]struct{}, 0)
	size := len(nums)
	for i := 0; i < size-1; i++ {
		sum := nums[i] + nums[i+1]
		if _, ok := dict[sum]; ok {
			return true
		}
		dict[sum] = struct{}{}
	}
	return false
}
