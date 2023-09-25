numbersList = [36, 67, 84, 76, 43, 64, 95, 100, 19, 80, 62, 61, 89, 53, 79, 74, 51, 17, 29, 72]


def fast_sorting(numbers):
    if len(numbers) <= 1:
        return numbers
    else:
        pivot = numbers.pop()
    greater = []
    lower = []
    for number in numbers:
        if number > pivot:
            greater.append(number)
        else:
            lower.append(number)
    return fast_sorting(lower) + [pivot] + fast_sorting(greater)


print(fast_sorting(numbersList))
