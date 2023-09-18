numbers = [36, 67, 84, 76, 43, 64, 95, 100, 19, 80, 62, 61, 89, 53, 79, 74, 51, 17, 29, 72]


def selection_sorting(elements):
    """

    :param elements:
    :return:
    """
    for i in range(len(elements)):
        min_element = i
        for j in range(i+1, len(elements)):
            if elements[min_element] > elements[j]:
                min_element = j
        elements[i], elements[min_element] = elements[min_element], elements[i]
    return elements


print(selection_sorting(numbers))
