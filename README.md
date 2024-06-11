# Steinberg's algorithm for the Strip Packing Problem with two heuristics
Steinberg's algorithm is an approximation algorithm with approximation ratio 2 (see [A. Steinberg, 1997](https://epubs.siam.org/doi/10.1137/S0097539793255801)). 

We also apply two heuristics: ''removing gaps'' and ''dropping rectangles''.

Let us consider a strip of width W=10 and eight rectangles [1, 1], [1, 1], [10, 8], [3, 1], [9, 1], [2, 1], [1, 1], [3, 1]. 

Optimal height H_opt = 10 can be provided with the packing [9, 9], [8, 9], [0, 0], [5, 9], [0, 8], [3, 9], [9, 8], [0, 9].  

Steinberg algorithm provides height H_1=18.25.

![Alt text](Figure_1.png?raw=true "Steinberg")

''Removing gaps'' algorithm provides height H_2=13.0. 

![Alt text](Figure_2.png?raw=true "RemovingGaps")

''Dropping rectangles'' algorithm provides height H_3=12.0. 

![Alt text](Figure_3.png?raw=true "RemovingGaps")

For a description and comparison of the given algorithms, see [StripPacking.pdf](https://github.com/yzsources/StripPacking/blob/main/StripPacking.pdf).

For an implementation, see [StripPacking](https://github.com/yzsources/StripPacking).
