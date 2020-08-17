#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A suite of tests testing mx_mul.py utility. """
import mock
import pytest

from mx_mul import *

matrices_passable = [[1]], [[1, 2, 3]], [[3], [2], [1]], [[0]], [[0.7]], [[-5]], [[-0.08]], [[-1], [5], [3.14]]
matrices_impassable = [], [[]], [0], [["not int"]], [""], "no numbers", 666, 7.45
example1 = ([[3, 4, 2]], [[13, 9, 7, 15], [8, 7, 4, 6], [6, 4, 0, 3]], [[83, 63, 37, 75]])
example2 = ([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]], [[58, 64], [139, 154]])
example_str = ([[1, 2, 3], [4, 5, 6]], "1 2 3\n4 5 6"),
examples_fail = ([[1, 3], [1, 0, 0]], [[0, 0, 5, 1], [7, 5, 0, 4]])


def _prepare_inputs(a, b):
    list_of_inputs = [len(a[0]), len(a), len(b[0]), len(b)]
    for row in a:
        list_of_inputs.append(" ".join([str(cell) for cell in row]))
    for row in b:
        list_of_inputs.append(" ".join([str(cell) for cell in row]))
    return list_of_inputs


class TestMatrixClass:
    @pytest.mark.parametrize("values", matrices_passable)
    def test_instantiate_should_pass(self, values):
        matrix = Matrix(values)
        assert isinstance(matrix, Matrix)

    @pytest.mark.parametrize("values", matrices_impassable)
    def test_instantiate_should_fail(self, values):
        with pytest.raises(TypeError):
            matrix = Matrix(values)
            assert not isinstance(matrix, Matrix)

    @pytest.mark.parametrize("values,expect", example_str)
    def test_string_representations(self, values, expect):
        assert str(Matrix(values)) == expect

    @pytest.mark.parametrize("values", example1)
    def test_matrix_equality(self, values):
        assert Matrix(values) == Matrix(values)
        assert Matrix(values) is not Matrix(values)

    @pytest.mark.parametrize("values", example1)
    def test_matrix_non_equality(self, values):
        assert Matrix(values) != Matrix([[1, 3, 1]])
        assert Matrix(values) != Matrix([[1]])

    @pytest.mark.parametrize("a,b,c", [example1, example2])
    def test_dot_method_should_pass(self, a, b, c):
        result = Matrix(a).dot(Matrix(b))
        assert result == Matrix(c)

    @pytest.mark.parametrize("a,b", examples_fail)
    def test_dot_method_should_fail(self, a, b):
        with pytest.raises(TypeError):
            c = Matrix(a).dot(Matrix(b))
            assert not isinstance(c, Matrix)

    @pytest.mark.parametrize("a,b,c", [example1, example2])
    def test_mul_method_should_pass(self, a, b, c):
        assert Matrix(a) * Matrix(b) == Matrix(c)

    @pytest.mark.parametrize("a,b", examples_fail)
    def test_mul_method_should_fail(self, a, b):
        with pytest.raises(TypeError):
            c = Matrix(a) * Matrix(b)
            assert not isinstance(c, Matrix)


class TestMatrixCalculatorConsoleInterface:
    @pytest.mark.parametrize("a,b,c", [example1, example2])
    def test_read_matrices_values_should_pass(self, a, b, c):
        list_of_inputs = _prepare_inputs(a, b)
        with mock.patch('builtins.input', side_effect=list_of_inputs):
            a_result, b_result = MatrixCalculatorConsoleInterface().read_matrices_values(['A', 'B'])
            assert all([len(a[0]) == len(a_result[0]), len(a) == len(a_result)])
            assert all([len(b[0]) == len(b_result[0]), len(b) == len(b_result)])
            assert all(row == a[i] for i, row in enumerate(a_result))
            assert all(row == b[i] for i, row in enumerate(b_result))

    @pytest.mark.parametrize("a,b", [examples_fail])
    def test_read_matrices_values_should_fail(self, a, b):
        list_of_inputs = _prepare_inputs(a, b)
        with pytest.raises(ValueError):
            with mock.patch('builtins.input', side_effect=list_of_inputs):
                a_result, b_result = MatrixCalculatorConsoleInterface().read_matrices_values(['A', 'B'])

    @pytest.mark.parametrize("values,expect", example_str)
    def test_show_result(self, values, expect, capsys):
        captured = capsys.readouterr()
        assert captured.out == ""
        cal = MatrixCalculatorConsoleInterface()
        cal.show_result(str(Matrix(values)))
        captured = capsys.readouterr()
        assert captured.out == "Result:\n{}\n".format(expect)


class TestMatrixCalculator:
    @pytest.mark.parametrize("a,b,c", [example1, example2])
    def test_multiplication_should_pass(self, a, b, c, capsys):
        list_of_inputs = _prepare_inputs(a, b)
        with mock.patch('builtins.input', side_effect=list_of_inputs):
            MatrixCalculator().multiplication()
            captured = capsys.readouterr()
            assert "Result:\n{}\n".format(str(Matrix(c))) in captured.out
