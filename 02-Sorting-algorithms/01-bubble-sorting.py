numbers = [36, 67, 84, 76, 43, 64, 95, 100, 19, 80, 62, 61, 89, 53, 79, 74, 51, 17, 29, 72]


def bubble_sorting(elements):
    """
      Bubble sorting functions
      :param elements:
      :return:
      """
    for i in range(len(elements)):
        for j in range(len(elements) - i - 1):
            elements[j + 1], elements[j] = elements[j], elements[j + 1]
    return elements


print(bubble_sorting(numbers))
