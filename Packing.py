import matplotlib.patches as patches
import matplotlib.pyplot as plt

def OutData(stripWidth, elements):
    file = open("input.txt", "w")
    file.write(str(stripWidth) + "\n")
    for i in range(len(elements)):
        file.write(str(elements[i][0]) + " " + str(elements[i][1]) + "\n")
    file.close()

def OutPacking(packing):
    count = len(packing)
    steinbergHeight = 0
    for i in range(count):
        steinbergHeight = max(packing[i][0][1] + packing[i][1][1], steinbergHeight)
        print("X=", packing[i][0][0], ", Y=", packing[i][0][1],
              ", Width=", packing[i][1][0], ", Height=", packing[i][1][1])
    print("Algorithm height=", steinbergHeight)

def MaxHeight(packing):
    maxTop = 0
    for element in packing:
        currentTop = element[0][1] + element[1][1]
        if maxTop < currentTop:
            maxTop = currentTop
    return maxTop

def PlotPacking(packing, stripWidth, stripHeight, colors):
    packing.sort(key=lambda x: x[1][0])
    packing.sort(key=lambda x: x[1][1])
    maxHeight = MaxHeight(packing)
    stripHeight = maxHeight if maxHeight > stripHeight else stripHeight
    count = len(packing)
    figure, axis = plt.subplots(1)
    axis.set_xlim(0, stripWidth)
    axis.set_ylim(0, stripHeight)
    for i in range(count):
        axis.add_patch(patches.Rectangle(
            tuple(packing[i][0]), packing[i][1][0], packing[i][1][1],
            linewidth=0.5, edgecolor='black', facecolor=colors[i]))
    plt.show()