import copy
import Packing
import Examples
from Steinberg import RunSteinberg

stripWidth, elements = Examples.Example7()
colors = Examples.GenerateColors(len(elements))
packing, stripHeight = RunSteinberg(stripWidth, copy.deepcopy(elements), False, False)
print("Calculated height: ", Packing.MaxHeight(packing))
Packing.PlotPacking(packing, stripWidth, stripHeight, colors)

packing, stripHeight = RunSteinberg(stripWidth, copy.deepcopy(elements), True, False)
print("Calculated height: ", Packing.MaxHeight(packing))
Packing.PlotPacking(packing, stripWidth, stripHeight, colors)

packing, stripHeight = RunSteinberg(stripWidth, copy.deepcopy(elements), False, True)
print("Calculated height: ", Packing.MaxHeight(packing))
Packing.PlotPacking(packing, stripWidth, stripHeight, colors)












