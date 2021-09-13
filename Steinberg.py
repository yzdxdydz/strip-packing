import copy

def RunSteinberg(stripWidth, elements, withoutGaps=False, dropAll=False, roundValue=6):
    sumArea = 0
    count = len(elements)
    for i in range(count):
        sumArea += elements[i][0] * elements[i][1]
    maxWidth = max(elements, key=lambda x: x[0])[0]
    maxHeight = max(elements, key=lambda x: x[1])[1]
    if 2*maxWidth >= stripWidth and sumArea <= maxHeight*stripWidth:
        estimateHeight = (sumArea + 4*maxWidth*maxHeight - maxHeight*stripWidth) / (2*maxWidth)
    else:
        estimateHeight = 2*sumArea / stripWidth
    stripHeight = round(estimateHeight, roundValue) + roundValue if round(estimateHeight, roundValue) < estimateHeight \
        else round(estimateHeight, roundValue)
    stripHeight = max(maxHeight, stripHeight)
    packing = []
    if maxWidth > stripWidth or maxHeight > stripHeight or \
            2 * sumArea > round(stripWidth * stripHeight - max(2 * maxWidth - stripWidth, 0) *
                                max(2 * maxHeight - stripHeight, 0), roundValue):
        print("Cannot be solved")
        return packing, 0
    packing = Steinberg([0, 0], stripWidth, stripHeight, elements, packing, roundValue)
    if len(packing) == 0:
        stripHeight = 0
    if dropAll:
        packing = DropPacking(packing)
    if withoutGaps:
        packing = RemoveGaps(packing)
    return packing, stripHeight

def RemoveGaps(packing):
    count = len(packing)
    if count == 0:
        return packing
    components = []
    for i in range(count):
        components.append([[packing[i]], packing[i][0][1], packing[i][0][1]+packing[i][1][1]])
    merged = True
    while merged:
        merged = False
        currentCount = len(components)
        i = 0
        while i < currentCount and not merged:
            j = 0
            while j < currentCount and not merged:
                if i == j:
                    j += 1
                    continue
                if components[j][1] <= components[i][1] <= components[j][2] or \
                        components[j][1] <= components[i][2] <= components[j][2]:
                    components[i][0] = copy.deepcopy(components[i][0] + components[j][0])
                    components[i][1] = min(components[i][1], components[j][1])
                    components[i][2] = max(components[i][2], components[j][2])
                    del components[j]
                    merged = True
                j += 1
            i += 1
    components.sort(key=lambda x: x[1])
    gaps = []
    sumGap = 0
    countOfComponents = len(components)
    for i in range(countOfComponents):
        if i == 0:
            gap = components[i][1]
        else:
            gap = components[i][1] - components[i-1][2]
        sumGap += gap
        gaps.append(sumGap)
    newPacking = []
    for i in range(countOfComponents):
        for packingElement in components[i][0]:
            newPacking.append([[packingElement[0][0], packingElement[0][1] - gaps[i]], packingElement[1]])
    return newPacking

def DropPacking(packing):
    packing.sort(key=lambda x: x[0][1])
    count = len(packing)
    someoneFalls = True
    while someoneFalls:
        someoneFalls = False
        for i in range(count):
            maxY = 0
            for j in range(count):
                if i != j and min(packing[i][0][0] + packing[i][1][0], packing[j][0][0] + packing[j][1][0]) - \
                        max(packing[i][0][0], packing[j][0][0]) > 0\
                        and packing[j][0][1] + packing[j][1][1] <= packing[i][0][1]:
                    maxY = packing[j][0][1] + packing[j][1][1] if packing[j][0][1] + packing[j][1][1] > maxY \
                        else maxY
            if maxY != packing[i][0][1]:
                packing[i][0][1] = maxY
                someoneFalls = True
    return packing

def Steinberg(containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    count = len(elements)
    if count == 0:
        return packing

    elements.sort(key=lambda x: x[0], reverse=True)
    if elements[0][0] >= containerWidth/2:
        return P1(containerOrigin, containerWidth, containerHeight, elements, packing, roundValue)

    elements.sort(key=lambda x: x[1], reverse=True)
    if elements[0][1] >= containerHeight/2:
        return Pm1(containerOrigin, containerWidth, containerHeight, elements, packing, roundValue)

    sumArea = 0
    for i in range(count):
        sumArea += elements[i][0] * elements[i][1]

    if count > 1:
        p3Enable = False
        elements.sort(key=lambda x: x[0], reverse=True)
        currentSumArea = 0
        i = 0
        while i < count - 1 and not p3Enable:
            currentSumArea += elements[i][0]*elements[i][1]
            p3Enable =\
                sumArea - containerWidth*containerHeight/4 <= currentSumArea <= 3*containerWidth*containerHeight/8\
                and elements[i+1][0] <= containerWidth/4
            i += 1
        if p3Enable:
            return P3(i-1, currentSumArea, containerOrigin, containerWidth, containerHeight, elements, packing,
                      roundValue)

        pm3Enable = False
        elements.sort(key=lambda x: x[1], reverse=True)
        currentSumArea = 0
        i = 0
        while i < count - 1 and not pm3Enable:
            currentSumArea += elements[i][0]*elements[i][1]
            pm3Enable = \
                sumArea - containerWidth*containerHeight/4 <= currentSumArea <= 3*containerWidth*containerHeight/8\
                and elements[i + 1][1] <= containerHeight/4
            i += 1
        if pm3Enable:
            return Pm3(i - 1, currentSumArea, containerOrigin, containerWidth, containerHeight, elements, packing,
                       roundValue)

        p2Enable = False
        i = 0
        while i < count and not p2Enable:
            k = 0
            while k < i and not p2Enable:
                p2Enable = \
                    elements[i][0] >= containerWidth/4 and elements[k][0] >= containerWidth/4 and \
                    elements[i][1] >= containerHeight/4 and elements[k][1] >= containerHeight/4 and \
                    2*(sumArea - elements[i][0]*elements[i][1] - elements[k][0]*elements[k][1]) <= \
                    (containerWidth - max(elements[i][0], elements[k][0]))*containerHeight
                k += 1
            i += 1
        if p2Enable:
            return P2(i-1, k-1, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue)

        pm2Enable = False
        i = 0
        while i < count and not pm2Enable:
            k = 0
            while k < i and not pm2Enable:
                pm2Enable = \
                    elements[i][0] >= containerWidth/4 and elements[k][0] >= containerWidth/4 and \
                    elements[i][1] >= containerHeight/4 and elements[k][1] >= containerHeight/4 and \
                    2*(sumArea - elements[i][0]*elements[i][1] - elements[k][0]*elements[k][1]) <= \
                    (containerHeight - max(elements[i][1], elements[k][1]))*containerWidth
                k += 1
            i += 1
        if pm2Enable:
            return Pm2(i-1, k-1, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue)

    p0Enable = False
    i = 0
    while i < count and not p0Enable:
        p0Enable = sumArea - containerWidth*containerHeight/4 <= elements[i][0]*elements[i][1]
        i += 1
    if p0Enable:
        return P0(i-1, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue)
    return packing

def P1(containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    count = len(elements)
    packingLast = len(packing) - 1
    sumHeight = elements[0][1]
    packing.append([containerOrigin, elements[0]])
    i = 1
    while i < count and elements[i][0] >= containerWidth / 2:
        packing.append([[containerOrigin[0], packing[packingLast + i][0][1] + packing[packingLast + i][1][1]],
                        elements[i]])
        sumHeight += elements[i][1]
        i += 1
    del elements[0:i]
    count = len(elements)
    if count == 0:
        return packing
    elements.sort(key=lambda x: x[1], reverse=True)
    if elements[0][1] <= containerHeight - sumHeight:
        packing = Steinberg([containerOrigin[0], containerOrigin[1] + sumHeight],
                            containerWidth,
                            containerHeight - sumHeight,
                            elements, packing, roundValue)
        return packing
    else:
        packingLast = len(packing) - 1
        sumWidth = elements[0][0]
        packing.append([[containerOrigin[0] + containerWidth - elements[0][0],
                         containerOrigin[1] + containerHeight - elements[0][1]],
                       elements[0]])
        i = 1
        while i < count and elements[i][1] > containerHeight - sumHeight:
            packing.append([[packing[packingLast + i][0][0] - elements[i][0],
                            containerOrigin[1] + containerHeight - elements[i][1]],
                            elements[i]])
            sumWidth += elements[i][0]
            i += 1
        del elements[0:i]
        packing = Steinberg([containerOrigin[0], containerOrigin[1] + sumHeight],
                                        containerWidth - sumWidth,
                                        containerHeight - sumHeight,
                                        elements, packing, roundValue)
        return packing

def Pm1(containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    count = len(elements)
    packingLast = len(packing) - 1
    sumWidth = elements[0][0]
    packing.append([containerOrigin, elements[0]])
    i = 1
    while i < count and elements[i][1] >= containerHeight / 2:
        packing.append([[packing[packingLast + i][0][0] + packing[packingLast + i][1][0], containerOrigin[1]],
                        elements[i]])
        sumWidth += elements[i][0]
        i += 1
    del elements[0:i]
    count = len(elements)
    if count == 0:
        return packing
    elements.sort(key=lambda x: x[0], reverse=True)
    if elements[0][0] <= containerWidth - sumWidth:
        packing = Steinberg([containerOrigin[0] + sumWidth, containerOrigin[1]],
                            containerWidth - sumWidth,
                            containerHeight,
                            elements, packing, roundValue)
        return packing
    else:
        packingLast = len(packing) - 1
        sumHeight = elements[0][1]
        packing.append([[containerOrigin[0] + containerWidth - elements[0][0],
                         containerOrigin[1] + containerHeight - elements[0][1]],
                        elements[0]])
        i = 1
        while i < count and elements[i][0] > containerWidth - sumWidth:
            packing.append([[containerOrigin[0] + containerWidth - elements[i][0],
                             packing[packingLast + i][0][1] - elements[i][1]],
                            elements[i]])
            sumHeight += elements[i][1]
            i += 1
        del elements[0:i]
        packing = Steinberg([sumWidth + containerOrigin[0], containerOrigin[1]],
                            containerWidth - sumWidth,
                            containerHeight - sumHeight,
                            elements, packing, roundValue)
        return packing

def P3(currentIndex, currentSumArea, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    count = len(elements)
    width1 = round(max(containerWidth/2, 2*currentSumArea/containerHeight), roundValue)
    width2 = containerWidth - width1
    elements1, elements2 = [], []
    for i in range(count):
        if i <= currentIndex:
            elements1.append(elements[i])
        else:
            elements2.append(elements[i])
    packing = Steinberg(containerOrigin, width1, containerHeight, elements1, packing, roundValue)
    packing = Steinberg([containerOrigin[0] + width1, containerOrigin[1]], width2, containerHeight,
                                    elements2, packing, roundValue)
    return packing

def Pm3(currentIndex, currentSumArea, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    count = len(elements)
    height1 = round(max(containerHeight/2, 2*currentSumArea/containerWidth), roundValue)
    height2 = containerHeight - height1
    elements1, elements2 = [], []
    for i in range(count):
        if i <= currentIndex:
            elements1.append(elements[i])
        else:
            elements2.append(elements[i])
    packing = Steinberg(containerOrigin, containerWidth, height1, elements1, packing, roundValue)
    packing = Steinberg([containerOrigin[0], containerOrigin[1] + height1], containerWidth, height2,
                                    elements2, packing, roundValue)
    return packing

def P2(index1, index2, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    if elements[index2][0] > elements[index1][0]:
        index = index1
        index1 = index2
        index2 = index
    packing.append([containerOrigin, elements[index1]])
    packing.append([[containerOrigin[0], containerOrigin[1] + elements[index1][1]], elements[index2]])
    elementWidth = elements[index1][0]
    if index1 < index2:
        del elements[index2], elements[index1]
    else:
        del elements[index1], elements[index2]
    packing = Steinberg([containerOrigin[0] + elementWidth, containerOrigin[1]],
                                    containerWidth - elementWidth, containerHeight, elements, packing, roundValue)
    return packing

def Pm2(index1, index2, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    if elements[index2][1] > elements[index1][1]:
        index = index1
        index1 = index2
        index2 = index
    packing.append([containerOrigin, elements[index1]])
    packing.append([[containerOrigin[0] + elements[index1][0], containerOrigin[1]], elements[index2]])
    elementHeight = elements[index1][1]
    if index1 < index2:
        del elements[index2], elements[index1]
    else:
        del elements[index1], elements[index2]
    packing = Steinberg([containerOrigin[0], containerOrigin[1] + elementHeight], containerWidth,
                        containerHeight - elementHeight, elements, packing, roundValue)
    return packing

def P0(index, containerOrigin, containerWidth, containerHeight, elements, packing, roundValue):
    packing.append([containerOrigin, elements[index]])
    elementWidth = elements[index][0]
    del elements[index]
    packing = Steinberg([containerOrigin[0] + elementWidth, containerOrigin[1]],
                                    containerWidth - elementWidth, containerHeight, elements, packing, roundValue)
    return packing