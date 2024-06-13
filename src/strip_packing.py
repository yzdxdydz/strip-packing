from abc import ABC, abstractmethod


class StripPacking(ABC):
    """
    Abstract base class for strip packing algorithms.

    This class provides the framework for implementing various strip
    packing algorithms where elements (rectangular items) are packed
    into a strip with a fixed width and varying height. It defines
    common methods for printing packing information, calculating the
    maximum height, and visualizing the packing result.

    Attributes:
        width (int):
            The width of the strip for packing.
        packing (list):
            A list to store the packed elements.
            Each element is represented as a list of two lists:
            the first list contains the [x, y] coordinates
            of the bottom-left corner of the element,
            and the second list contains its [width, height].
        height (float): The estimated height of the packing.
            This attribute is expected to be set by subclasses
            when implementing the packing algorithm.
    """

    def __init__(self, strip_width: int):
        """
        Initialize the StripPacking class with a given strip width.

        Args:
            strip_width (int):
                The width of the strip for packing.

        Initializes:
            self.width (int):
                Sets the strip width.
            self.packing (list):
                Initializes as an empty list to hold the packing
                result. Expected to be set by the packing algorithm.
            self.height (int or None):
                Initializes as None. Expected to be set by
                the packing algorithm.
        """
        from copy import deepcopy
        self.width = strip_width
        self.packing = []
        self.height = None

    def print_info(self):
        """
        Print the packing information to the console.
        """
        if len(self.packing) == 0:
            print("Packing is not ready. Run \"get_packing\" first")
            return
        packing_height = 0
        for packing_el in self.packing:
            packing_height = max(packing_el[0][1] + packing_el[1][1],
                                 packing_height)
            print("X=", packing_el[0][0], ", Y=", packing_el[0][1],
                  ", Width=", packing_el[1][0], ", Height=", packing_el[1][1])
        print("Algorithm height=", packing_height)

    def max_height(self):
        """
        Calculate the maximum height of the packing.

        Returns:
            float: The maximum height of the packing.
        """
        return max(packing_el[0][1] + packing_el[1][1]
                   for packing_el in self.packing)

    def plot_packing(self, colors, file_name):
        """
        Plot and save the visual representation of the packing.

        Args:
            colors (list of str):
                A list of colors for the packed elements.
                Each color in the list corresponds to
                an element in the `packing`.
            file_name (str): The name of the file
            where the plot will be saved.

        Example:
            colors = ['red', 'blue', 'green', ...]
            file_name = 'packing_result.png'
        """
        from matplotlib import patches, pyplot as plt
        self.packing.sort(key=lambda x: x[1][0])
        self.packing.sort(key=lambda x: x[1][1])
        figure, axis = plt.subplots(1)
        axis.set_xlim(0, self.width)
        axis.set_ylim(0, max(self.height, self.max_height()))
        for i in range(len(self.packing)):
            axis.add_patch(patches.Rectangle(
                tuple(self.packing[i][0]),
                self.packing[i][1][0], self.packing[i][1][1],
                linewidth=0.5, edgecolor='black', facecolor=colors[i]))
        plt.savefig(file_name)

    @abstractmethod
    def get_packing(self, elements):
        """
        Abstract method to calculate the packing of elements.

        This method should be implemented by subclasses to apply
        a specific packing algorithm.

        Args:
            elements (list of lists):
                A list where each element is a list containing two
                integers [width, height]. Represents the dimensions
                of items to be packed.

                Example:
                    [[width1, height1], [width2, height2], ...]

        This method should set the `self.packing` and `self.height`
        attributes to reflect the calculated packing.
        """
        pass
