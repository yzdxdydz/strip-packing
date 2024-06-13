def example1():
    return 30, [[5, 3], [5, 3], [2, 4], [30, 8], [10, 20], [20, 10], [5, 5], [5, 5], [10, 10], [10, 5], [6, 4], [1, 10],
                [8, 4], [6, 6], [20, 14]]

def example2():
    return 30, [[20, 6], [3, 10], [7, 10], [20, 12], [10, 8], [30, 10]]

def example3():
    return 2, [[1, 1], [1, 1], [2, 1]]

def example4():
    return 12, [[4, 3], [4, 9], [1, 12], [2, 3], [2, 7], [2, 2], [5, 2], [5, 6], [5, 4]]

def example5():
    return 25, [[10, 8], [10, 8], [12, 4], [12, 4], [25, 3]]

def example6():
    return 10, [[3, 3], [7, 2], [7, 1], [9, 3], [5, 4], [4, 4], [7, 1]]

def example7():
    return 10, [[1, 1], [1, 1], [10, 8], [3, 1], [9, 1], [2, 1], [1, 1], [3, 1]]

def random_example():
    from random import randint
    strip_width = randint(3, 100)
    elements = []
    count = randint(3, 100)
    for i in range(count):
        elements.append([randint(1, strip_width), randint(1, 100)])
    return strip_width, elements


def random_example_with_optimum():
    from random import randint
    strip_width = randint(10, 100)
    strip_height = randint(10, 100)
    count = randint(3, 100)
    elements = [[strip_width, strip_height]]
    steps = 0
    while len(elements) < count and steps < 1000:
        steps += 1
        current_count = len(elements)
        cut_index = randint(0, current_count - 1)
        vertical_cut = randint(0, 1)
        if vertical_cut == 0 and elements[cut_index][0] > 1:
            cut_size = randint(1, elements[cut_index][0] - 1)
            remained_size = elements[cut_index][0] - cut_size
            elements[cut_index][0] = cut_size
            elements.append([remained_size, elements[cut_index][1]])
        elif vertical_cut == 1 and elements[cut_index][1] > 1:
            cut_size = randint(1, elements[cut_index][1] - 1)
            remained_size = elements[cut_index][1] - cut_size
            elements[cut_index][1] = cut_size
            elements.append([elements[cut_index][0], remained_size])
    return strip_width, strip_height, elements

