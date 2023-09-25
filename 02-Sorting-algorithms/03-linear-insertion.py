numbersList = [36, 67, 84, 76, 43, 64, 95, 100, 19, 80, 62, 61, 89, 53, 79, 74, 51, 17, 29, 72]


def insertion_numbers(numbers):
    for i in range(1, len(numbers)):
        aux = numbers[i]
        j = i - 1
        while j >= 0 and aux < numbers[j]:
            numbers[j + 1] = numbers[j]
            j -= 1
        numbers[j + 1] = aux
    return numbers


insertion_numbers(numbersList)
print(numbersList)
