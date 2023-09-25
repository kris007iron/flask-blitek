numbersList = [36, 67, 84, 76, 43, 64, 95, 100, 19, 80, 62, 61, 89, 53, 79, 74, 51, 17, 29, 72]


def merge_sort(numbers):
    if len(numbers) > 1:
        middle = len(numbers) // 2
        left = numbers[:middle]
        right = numbers[middle:]
        merge_sort(left)
        merge_sort(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                numbers[k] = left[i]
                i += 1
            else:
                numbers[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            numbers[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            numbers[k] = right[j]
            j += 1
            k += 1
    return numbers


print(merge_sort(numbersList))
