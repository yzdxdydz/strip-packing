from copy import deepcopy

from src.strip_packing import StripPacking


class SteinbergPacking(StripPacking):
    """
    A class for implementing the Steinberg strip packing algorithm.

    Inherits from StripPacking.

    Reference:
        A. Steinberg,
        "A strip-packing algorithm with absolute performance bound 2",
        SIAM J. Comput. 26:2 (1997), 401–409.
    """

    def __init__(self, strip_width: int,
                 without_gaps=False, dpop_hanging_element=False,
                 round_value=6):
        """
        Initialize SteinbergPacking class with a given strip width.

        Args:
            strip_width (int): The width of the strip for packing.
            without_gaps (bool, optional):
                Whether to remove gaps after packing.
                Defaults to False.
            dpop_hanging_element (bool, optional):
                Whether to drop hanging elements after packing.
                Defaults to False.
            round_value (int, optional):
                Number of decimal places to round heights.
                Defaults to 6.
        """
        super().__init__(strip_width)
        self.without_gaps = without_gaps
        self.dpop_hanging_element = dpop_hanging_element
        self.round_value = round_value

    def get_packing(self, elements):
        """
        Perform the packing algorithm on the given elements.

        Args:
            elements (list of lists):
                A list where each element is a list containing
                two integers [width, height].
                Represents the dimensions of items to be packed.

                Example:
                    [[width1, height1], [width2, height2], ...]

        Modifies:
            self.height (int or None):
                Sets this attribute to the estimated height of
                the packed elements. If the packing is not feasible,
                sets `self.height` to None.
            self.packing (list):
                Sets this attribute to the final packing configuration
                after applying the algorithm.

        Returns:
            None
        """
        self.packing = []

        sum_area = sum(el[0]*el[1] for el in elements)
        max_width = max(el[0] for el in elements)
        max_height = max(el[1] for el in elements)
        estimate_height = (
            (sum_area
             + 4*max_width*max_height
             - max_height*self.width) / (2*max_width)
            if (2 * max_width >= self.width
                and sum_area <= max_height * self.width)
            else 2*sum_area / self.width
        )
        self.height = max(max_height,
                          round(estimate_height, self.round_value)
                          + (self.round_value
                             if (round(estimate_height, self.round_value)
                                 < estimate_height)
                             else 0)
                          )

        if (max_width > self.width or
                max_height > self.height or
                2 * sum_area > round(self.width * self.height
                                     - max(2 * max_width - self.width, 0)
                                     * max(2 * max_height - self.height, 0),
                                     self.round_value)):
            print("Packing probem cannot be solved")
            self.height = None
            return

        self.__steinberg([0, 0], self.width, self.height,
                         deepcopy(elements))

        if len(self.packing) == 0:
            self.height = None
            print("Steinberg algorithm failed")

        if self.dpop_hanging_element:
            self.__dpop_hanging_elements()
        if self.without_gaps:
            self.__remove_gaps()

    def __remove_gaps(self):
        """
        Remove gaps between packed elements in the packing.

        Modifies:
            self.packing (list):
                Sets this attribute to the packing configuration
                after gaps removal.

        Returns:
            None
        """
        if len(self.packing) == 0:
            return

        components = [
            [[packing_el],
             packing_el[0][1],
             packing_el[0][1] + packing_el[1][1]
             ]
            for packing_el in self.packing
        ]

        merged = True
        while merged:
            merged = False
            current_count = len(components)
            for i in range(current_count):
                if merged:
                    break
                for j in range(current_count):
                    if i == j:
                        continue
                    if components[j][1] \
                            <= components[i][1] \
                            <= components[j][2] or \
                            components[j][1] \
                            <= components[i][2] \
                            <= components[j][2]:
                        components[i][0] = deepcopy(components[i][0]
                                                    + components[j][0])
                        components[i][1] = min(components[i][1],
                                               components[j][1])
                        components[i][2] = max(components[i][2],
                                               components[j][2])
                        del components[j]
                        merged = True
                        break

        components.sort(key=lambda x: x[1])
        gaps = []
        for i in range(len(components)):
            gaps.append((0 if i == 0 else gaps[i - 1])
                        + components[i][1]
                        - (0 if i == 0 else components[i - 1][2]))
        self.packing = [
            [[packing_el[0][0], packing_el[0][1] - gaps[i]], packing_el[1]]
            for i in range(len(components))
            for packing_el in components[i][0]
        ]

    def __dpop_hanging_elements(self):
        """
        Drop hanging elements from the packing.

        Modifies:
            self.packing (list):
                Sets this attribute to the packing configuration
                after hanging elements drop.

        Returns:
            None
        """
        self.packing.sort(key=lambda x: x[0][1])
        one_falls = True
        while one_falls:
            one_falls = False
            for i in range(len(self.packing)):
                y_max = 0
                for j in range(len(self.packing)):
                    if i != j and\
                            min(self.packing[i][0][0]
                                + self.packing[i][1][0],
                                self.packing[j][0][0]
                                + self.packing[j][1][0]
                                ) \
                            - max(self.packing[i][0][0],
                                  self.packing[j][0][0]) > 0 and \
                            self.packing[j][0][1] \
                            + self.packing[j][1][1] \
                            <= self.packing[i][0][1]:
                        y_max = max(self.packing[j][0][1]
                                    + self.packing[j][1][1],
                                    y_max)
                if y_max != self.packing[i][0][1]:
                    self.packing[i][0][1] = y_max
                    one_falls = True

    def __steinberg(self, container_origin, container_width,
                    container_height, remained_elements):
        """
        Implement the Steinberg packing algorithm
        for the container recursively.

        Args:
            container_origin (list):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (float):
                Width of the container.
            container_height (float):
                Height of the container.
            remained_elements (list):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Returns:
            None
        """
        if len(remained_elements) == 0:
            return

        remained_elements.sort(key=lambda x: x[0], reverse=True)
        if remained_elements[0][0] >= container_width / 2:
            self.__p1(container_origin, container_width,
                      container_height, remained_elements)
            return

        remained_elements.sort(key=lambda x: x[1], reverse=True)
        if remained_elements[0][1] >= container_height / 2:
            self.__pm1(container_origin, container_width,
                       container_height, remained_elements)
            return

        sum_area = sum(el[0]*el[1] for el in remained_elements)

        if len(remained_elements) > 1:
            remained_elements.sort(key=lambda x: x[0], reverse=True)
            current_sum_area = 0
            for i in range(len(remained_elements) - 1):
                current_sum_area += remained_elements[i][0] \
                                    * remained_elements[i][1]
                if sum_area - container_width * container_height / 4 \
                        <= current_sum_area \
                        <= 3 * container_width * container_height / 8 and \
                        remained_elements[i + 1][0] <= container_width / 4:
                    self.__p3(i, current_sum_area, container_origin,
                              container_width, container_height,
                              remained_elements)
                    return

            remained_elements.sort(key=lambda x: x[1], reverse=True)
            current_sum_area = 0
            for i in range((len(remained_elements)) - 1):
                current_sum_area += remained_elements[i][0] \
                                    * remained_elements[i][1]
                if sum_area - container_width * container_height / 4 \
                        <= current_sum_area \
                        <= 3 * container_width * container_height / 8 and \
                        remained_elements[i + 1][1] <= container_height / 4:
                    self.__pm3(i, current_sum_area, container_origin,
                               container_width, container_height,
                               remained_elements)
                    return

            for i in range(len(remained_elements)):
                for k in range(i):
                    if remained_elements[i][0] \
                            >= container_width / 4 and \
                            remained_elements[k][0] >=\
                            container_width / 4 and \
                            remained_elements[i][1] \
                            >= container_height / 4 and \
                            remained_elements[k][1] \
                            >= container_height / 4 and \
                            2 * (
                            sum_area - remained_elements[i][0]
                            * remained_elements[i][1]
                            - remained_elements[k][0]
                            * remained_elements[k][1]) \
                            <= (container_width
                                - max(remained_elements[i][0],
                                      remained_elements[k][0])) \
                            * container_height:
                        self.__p2(i, k, container_origin, container_width,
                                  container_height, remained_elements)
                        return

            for i in range(len(remained_elements)):
                for k in range(i):
                    if remained_elements[i][0] \
                            >= container_width / 4 and \
                            remained_elements[k][0] \
                            >= container_width / 4 and \
                            remained_elements[i][1] \
                            >= container_height / 4 and \
                            remained_elements[k][1] \
                            >= container_height / 4 and \
                            2 * (
                            sum_area - remained_elements[i][0]
                            * remained_elements[i][1]
                            - remained_elements[k][0] *
                            remained_elements[k][1]) \
                            <= (container_height
                                - max(remained_elements[i][1],
                                      remained_elements[k][1])) \
                            * container_width:
                        self.__pm2(i, k, container_origin, container_width,
                                   container_height, remained_elements)
                        return

        for i in range(len(remained_elements)):
            if sum_area - container_width * container_height / 4 \
                    <= remained_elements[i][0] * remained_elements[i][1]:
                self.__p0(i, container_origin, container_width,
                          container_height, remained_elements)
                return

    def __p1(self, container_origin, container_width,
             container_height, remained_elements):
        """
        Perform the P1 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        packing_last = len(self.packing) - 1
        sum_height = remained_elements[0][1]
        self.packing.append([container_origin, remained_elements[0]])
        for i in range(1, len(remained_elements)):
            if remained_elements[i][0] < container_width / 2:
                del remained_elements[0:i]
                break
            self.packing.append(
                [
                    [container_origin[0],
                     self.packing[packing_last + i][0][1]
                     + self.packing[packing_last + i][1][1]],
                    remained_elements[i]
                ])
            sum_height += remained_elements[i][1]
        else:
            del remained_elements[:]

        if len(remained_elements) == 0:
            return

        remained_elements.sort(key=lambda x: x[1], reverse=True)
        if remained_elements[0][1] <= container_height - sum_height:
            self.__steinberg([container_origin[0],
                              container_origin[1] + sum_height],
                             container_width,
                             container_height - sum_height,
                             remained_elements)
            return

        packing_last = len(self.packing) - 1
        sum_width = remained_elements[0][0]
        self.packing.append([[container_origin[0]
                              + container_width
                              - remained_elements[0][0],
                              container_origin[1]
                              + container_height
                              - remained_elements[0][1]],
                             remained_elements[0]])
        for i in range(1, len(remained_elements)):
            if remained_elements[i][1] <= container_height - sum_height:
                del remained_elements[0:i]
                break
            self.packing.append([[self.packing[packing_last + i][0][0]
                                  - remained_elements[i][0],
                                  container_origin[1] + container_height
                                  - remained_elements[i][1]],
                                 remained_elements[i]])
            sum_width += remained_elements[i][0]
        else:
            del remained_elements[:]

        self.__steinberg([container_origin[0],
                          container_origin[1] + sum_height],
                         container_width - sum_width,
                         container_height - sum_height,
                         remained_elements)

    def __pm1(self, container_origin, container_width,
              container_height, remained_elements):
        """
        Perform the Pm1 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        packing_last = len(self.packing) - 1
        sum_width = remained_elements[0][0]
        self.packing.append([container_origin, remained_elements[0]])
        for i in range(1, len(remained_elements)):
            if remained_elements[i][1] < container_height / 2:
                del remained_elements[0:i]
                break
            self.packing.append(
                [
                    [self.packing[packing_last + i][0][0]
                     + self.packing[packing_last + i][1][0],
                     container_origin[1]],
                    remained_elements[i]
                 ])
            sum_width += remained_elements[i][0]
        else:
            del remained_elements[:]

        if len(remained_elements) == 0:
            return

        remained_elements.sort(key=lambda x: x[0], reverse=True)
        if remained_elements[0][0] <= container_width - sum_width:
            self.__steinberg([container_origin[0] + sum_width,
                              container_origin[1]],
                             container_width - sum_width,
                             container_height,
                             remained_elements)
            return

        packing_last = len(self.packing) - 1
        sum_height = remained_elements[0][1]
        self.packing.append([[container_origin[0]
                              + container_width
                              - remained_elements[0][0],
                              container_origin[1]
                              + container_height
                              - remained_elements[0][1]],
                             remained_elements[0]])
        for i in range(1, len(remained_elements)):
            if remained_elements[i][0] <= container_width - sum_width:
                del remained_elements[0:i]
                break
            self.packing.append([[container_origin[0]
                                  + container_width
                                  - remained_elements[i][0],
                                  self.packing[packing_last + i][0][1]
                                  - remained_elements[i][1]],
                                 remained_elements[i]])
            sum_height += remained_elements[i][1]
        else:
            del remained_elements[:]

        self.__steinberg([sum_width + container_origin[0],
                          container_origin[1]],
                         container_width - sum_width,
                         container_height - sum_height,
                         remained_elements)

    def __p3(self, current_index, current_sum_area, container_origin,
             container_width, container_height, remained_elements):
        """
        Perform the P3 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        width1 = round(max(container_width/2,
                           2*current_sum_area/container_height),
                       self.round_value)
        width2 = container_width - width1
        remained_elements1, remained_elements2 = [], []
        for i in range(len(remained_elements)):
            if i <= current_index:
                remained_elements1.append(remained_elements[i])
            else:
                remained_elements2.append(remained_elements[i])
        self.__steinberg(container_origin, width1,
                         container_height, remained_elements1)
        self.__steinberg([container_origin[0] + width1, container_origin[1]],
                         width2, container_height, remained_elements2)

    def __pm3(self, current_index, current_sum_area,
              container_origin, container_width,
              container_height, remained_elements):
        """
        Perform the Pm3 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        height1 = round(max(container_height/2,
                            2*current_sum_area/container_width),
                        self.round_value)
        height2 = container_height - height1
        remained_elements1, remained_elements2 = [], []
        for i in range(len(remained_elements)):
            if i <= current_index:
                remained_elements1.append(remained_elements[i])
            else:
                remained_elements2.append(remained_elements[i])
        self.__steinberg(container_origin, container_width,
                         height1, remained_elements1)
        self.__steinberg([container_origin[0], container_origin[1] + height1],
                         container_width, height2, remained_elements2)

    def __p2(self, index1, index2, container_origin,
             container_width, container_height, remained_elements):
        """
        Perform the P2 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        if remained_elements[index2][0] > remained_elements[index1][0]:
            index = index1
            index1 = index2
            index2 = index
        self.packing.append([container_origin, remained_elements[index1]])
        self.packing.append(
            [[container_origin[0], container_origin[1]
              + remained_elements[index1][1]], remained_elements[index2]])
        element_width = remained_elements[index1][0]
        if index1 < index2:
            del remained_elements[index2], remained_elements[index1]
        else:
            del remained_elements[index1], remained_elements[index2]
        self.__steinberg([container_origin[0] + element_width,
                          container_origin[1]],
                         container_width - element_width,
                         container_height, remained_elements)

    def __pm2(self, index1, index2, container_origin,
              container_width, container_height, remained_elements):
        """
        Perform the Pm2 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        if remained_elements[index2][1] > remained_elements[index1][1]:
            index = index1
            index1 = index2
            index2 = index
        self.packing.append([container_origin, remained_elements[index1]])
        self.packing.append(
            [[container_origin[0] + remained_elements[index1][0],
              container_origin[1]], remained_elements[index2]])
        element_height = remained_elements[index1][1]
        if index1 < index2:
            del remained_elements[index2], remained_elements[index1]
        else:
            del remained_elements[index1], remained_elements[index2]
        self.__steinberg([container_origin[0],
                          container_origin[1] + element_height],
                         container_width,
                         container_height - element_height,
                         remained_elements)

    def __p0(self, index, container_origin, container_width,
             container_height, remained_elements):
        """
        Perform the P0 phase of the Steinberg packing algorithm
        for the container.

        Args:
            container_origin (list of int):
                The [x, y] coordinates of the bottom-left corner
                of the container where packing starts.
            container_width (int):
                The width of the container.
            container_height (int):
                The height of the container.
            remained_elements (list of lists):
                A list of elements remaining to be packed,
                where each element is [width, height].

        Modifies:
            self.packing (list):
                Appends the packed elements to this attribute.

        Returns:
            None.
        """
        self.packing.append([container_origin, remained_elements[index]])
        element_width = remained_elements[index][0]
        del remained_elements[index]
        self.__steinberg([container_origin[0] + element_width,
                          container_origin[1]],
                         container_width - element_width,
                         container_height, remained_elements)
