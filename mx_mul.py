#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Utility . """
from typing import List, Union


class Matrix:
    """ Represents mathematical matrix and its operations"""

    def __init__(self, values: List[List[Union[int, float]]]):
        if not (
                isinstance(values, List) and
                all([isinstance(row, List) and len(row) == len(values[0]) for row in values]) and
                all([isinstance(cell, (int, float)) for row in values for cell in row]) and
                (len(values) > 0 and len(values[0]) > 0)
        ):
            raise TypeError("Incorrect input types in the 'values' list")

        self.values = values

    def dot(self, other: 'Matrix') -> 'Matrix':
        """ Performs matrix multiplication of this and the other matrix

        Args:
            other: Other matrix instance

        Returns:
            New matrix instance that is a result of multiplication
        """
        result_values = self._initialize_empty_matrix_values(others_columns=len(other.values[0]))
        for i in range(len(self.values)):  # i is row index of the result
            for j in range(len(other.values[0])):  # j is column index of the result
                result_values[i][j] = sum(
                    [a * [row[j] for row in other.values][index] for index, a in enumerate(self._row(i))])
        return Matrix(result_values)

    def _initialize_empty_matrix_values(self, others_columns):
        return [[0 for x in range(others_columns)] for x in range(len(self.values))]

    def _row(self, index):
        return self.values[index]

    def __str__(self):
        rows = []
        for row in self.values:
            rows.append(" ".join([str(cell) for cell in row]))
        return "\n".join(rows)

    def __mul__(self, other):
        return self.dot(other)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               len(self.values) == len(other.values) and \
               len(self.values[0]) == len(other.values[0]) and \
               all([row == other.values[i] for i, row in enumerate(self.values)])

    def __ne__(self, other):
        return not self.__eq__(other)


class MatrixCalculatorConsoleInterface:
    """ Manages user interactions via command line interface """

    def read_matrices_values(self, labels: List[str]) -> List[List[List[Union[int, float]]]]:
        """ Prompt user via console for typing matrix parameters such as width, height and individual values

        Args:
            labels: List of labels, each assigned to one matrix prompted

        Returns:
            List of matrix values (2D lists of integers or floats)
        """
        matrix_parameters = []
        for label in labels:
            width, height = self._prompt_for_dimensions(label)
            matrix_parameters.append((label, width, height))
        return self._prompt_for_values(matrix_parameters)

    def _prompt_for_dimensions(self, label):
        print("Matrix {}:".format(label))
        width = self._read_attribute('width: ')
        height = self._read_attribute('height: ')
        print('')
        return width, height

    def _prompt_for_values(self, matrices):
        result_matrices = []
        for label, width, height in matrices:
            print("Matrix {} values:".format(label))
            rows = []
            for i in range(height):
                row = self._read_matrix_row(width=width)
                rows.append(row)
            assert True
            result_matrices.append(rows)
            print('')
        return result_matrices

    @classmethod
    def _read_attribute(cls, prompt):
        readout = input(prompt)
        return cls._parse_numeric_value(readout)

    @classmethod
    def _parse_numeric_value(cls, readout):
        try:
            value = int(readout)
        except ValueError:
            try:
                value = float(readout)
            except ValueError:
                raise ValueError("Unexpected format of attribute readout")
        return value

    @classmethod
    def _read_matrix_row(cls, width):
        row_data = []
        row_readout = input()
        split_data = row_readout.split()
        if len(split_data) != width:
            raise ValueError("Incorrect number of values on the row")
        for cell_data in split_data:
            row_data.append(cls._parse_numeric_value(cell_data))
        return row_data

    @staticmethod
    def show_result(result: str):
        """ Display result in the console

        Args:
            result: Result as a text to print
        """
        print("Result:")
        print(result)


class MatrixCalculator:
    """ Represents top level of calculator application """

    def __init__(self, user_interface_class=MatrixCalculatorConsoleInterface):
        self.ui = user_interface_class()

    def multiplication(self):
        """ Perform matrix multiplication of two matrices 'A' and 'B' with data from user interface

        """
        values_a, values_b = self.ui.read_matrices_values(labels=['A', 'B'])
        result = Matrix(values_a).dot(Matrix(values_b))
        self.ui.show_result(str(result))


if __name__ == '__main__':
    calc = MatrixCalculator()
    calc.multiplication()
