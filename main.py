from examples import  examples
from src.steinberg_packing import SteinbergPacking

eps = 1e-3
for _ in range(1000):
    width, elements = examples.random_example()
    sp = SteinbergPacking(width, False, False)
    sp.get_packing(elements)
    height1 = sp.height
    height2 = sp.max_height()
    sp = SteinbergPacking(width, True, False)
    sp.get_packing(elements)
    height3 = sp.max_height()
    sp = SteinbergPacking(width, True, True)
    sp.get_packing(elements)
    height4 = sp.max_height()
    if height1 + eps < height2 or height2 + eps < height3 or height3 + eps < height4:
        print("Problem", height1, height2, height3, height4)

for _ in range(1000):
    width, optimum_height, elements = examples.random_example_with_optimum()
    sp = SteinbergPacking(width, False, False)
    sp.get_packing(elements)
    height1 = sp.height
    height2 = sp.max_height()
    sp = SteinbergPacking(width, True, False)
    sp.get_packing(elements)
    height3 = sp.max_height()
    sp = SteinbergPacking(width, True, True)
    sp.get_packing(elements)
    height4 = sp.max_height()
    if height1 + eps < height2 or height2 + eps < height3 or height3 + eps < height4 or height4 + eps < optimum_height or\
        2*optimum_height+eps < height1:
        print("Problem", height1, height2, height3, height4)







