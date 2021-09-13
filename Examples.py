def Example1():
    return 30, [[5, 3], [5, 3], [2, 4], [30, 8], [10, 20], [20, 10], [5, 5], [5, 5], [10, 10], [10, 5], [6, 4], [1, 10],
                [8, 4], [6, 6], [20, 14]]

def Example2():
    return 30, [[20, 6], [3, 10], [7, 10], [20, 12], [10, 8], [30, 10]]

def Example3():
    return 2, [[1, 1], [1, 1], [2, 1]]

def Example4():
    return 12, [[4, 3], [4, 9], [1, 12], [2, 3], [2, 7], [2, 2], [5, 2], [5, 6], [5, 4]]

def Example5():
    return 25, [[10, 8], [10, 8], [12, 4], [12, 4], [25, 3]]

def Example6():
    return 10, [[3, 3], [7, 2], [7, 1], [9, 3], [5, 4], [4, 4], [7, 1]]

def Example7():
    return 10, [[1, 1], [1, 1], [10, 8], [3, 1], [9, 1], [2, 1], [1, 1], [3, 1]]

def RandomExample():
    from random import randint
    stripWidth = randint(3, 100)
    elements = []
    count = randint(3, 100)
    for i in range(count):
        elements.append([randint(1, stripWidth), randint(1, 100)])
    return stripWidth, elements

def RandomExampleWithOptimum():
    from random import randint
    stripWidth = randint(10, 100)
    stripHeight = randint(10, 100)
    count = randint(3, 100)
    elements = [[stripWidth, stripHeight]]
    steps = 0
    while len(elements) < count and steps < 1000:
        steps += 1
        currentCount = len(elements)
        cutIndex = randint(0, currentCount - 1)
        verticalCut = randint(0, 1)
        if verticalCut == 0 and elements[cutIndex][0] > 1:
            cutSize = randint(1, elements[cutIndex][0] - 1)
            remainedSize = elements[cutIndex][0] - cutSize
            elements[cutIndex][0] = cutSize
            elements.append([remainedSize, elements[cutIndex][1]])
        elif verticalCut == 1 and elements[cutIndex][1] > 1:
            cutSize = randint(1, elements[cutIndex][1] - 1)
            remainedSize = elements[cutIndex][1] - cutSize
            elements[cutIndex][1] = cutSize
            elements.append([elements[cutIndex][0], remainedSize])
    return stripWidth, stripHeight, elements

def GenerateColors(count):
    from random import randint
    colors = []
    for i in range(count):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    return colors