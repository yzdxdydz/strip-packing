# Steinberg Algorithm for Strip Packing Problem with two heuristics

This project implements the Steinberg algorithm for solving the strip packing problem in Python. (see [A. Steinberg, 1997](https://epubs.siam.org/doi/10.1137/S0097539793255801)) We also provide two heuristics: ''removing gaps'' and ''dropping hanging rectangles''. See documentation and examples. 

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/my_project.git
cd my_project
pip install -r requirements.txt
```

## Usage
To execute the packing algorithm, follow these steps:

1. Import the `SteinbergPacking` class from the `src/steinberg` module.
```python
from src.steinberg import SteinbergPacking
```
2. Create an instance of the `SteinbergPacking` class with the desired parameters. For example for original algorithm.
```python
sp = SteinbergPacking(width=10, without_gaps=False, drop_hanging_element=False)
```
3. Call the `get_packing` method, passing in the list of elements to be packed.
```python
elements = [[1, 1], [1, 1], [10, 8], [3, 1], [9, 1], [2, 1], [1, 1], [3, 1]]
#Optimal height H_opt = 10 can be provided with the packing 
# [9, 9], [8, 9], [0, 0], [5, 9], [0, 8], [3, 9], [9, 8], [0, 9].  
sp.get_packing(elements)
```
4. Calculate the height, plot the packing and save it to file.
```python
from random import randint
colors = []
for _ in elements:
    colors.append('#%06X' % randint(0, 0xFFFFFF))
sp.plot_packing(colors, "figure-1.png")
print("Height: ", sp.max_height())
```

5. Then Steinberg algorithm provides height H_1=18.25. The plot is 
![Alt text](examples/original-7.png?raw=true "Steinberg")

6. For ''Removing gaps'' algorithm,
```python
sp = SteinbergPacking(width=10, without_gaps=True, drop_hanging_element=False)
sp.get_packing(elements)
sp.plot_packing(colors, "figure-2.png")
print("Height: ", sp.max_height())
```

7. ''Removing gaps'' algorithm provides height H_2=13.0.
![Alt text](examples/no-gaps-7.png?raw=true "Removing gaps")

8. To ''Drop hanging elements'',
```python
sp = SteinbergPacking(width=10, without_gaps=True, drop_hanging_element=True)
sp.get_packing(elements)
sp.plot_packing(colors, "figure-3.png")
print("Height: ", sp.max_height())
```

9. ''Drop hanging elements'' algorithm provides height H_3=12.0.
![Alt text](examples/dropped-7.png?raw=true "DropAll")

## Documentation
For detailed information on the algorithm and how to use it, please refer to the documentation [strip-packing.pdf](https://github.com/yzdxdydz/strip-packing/blob/main/docs/strip-packing.pdf)