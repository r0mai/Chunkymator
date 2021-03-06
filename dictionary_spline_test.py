#!/usr/bin/env python

import unittest
from dictionary_spline import *


class JsonSchemaCheckerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty_and_non_empty_jsons_should_not_have_same_shape(self):
        dict1 = {}
        dict2 = {'a':5}

        self.assertFalse(jsonSchemaCheck([dict1, dict2]))

    def test_jsons_with_different_keys_should_not_have_same_shape(self):
        dict1 = {'a':5}
        dict2 = {'b':5}

        self.assertFalse(jsonSchemaCheck([dict1, dict2]))

    def test_jsons_with_same_keys_should_have_same_shape(self):
        dict1 = {'a':5}
        dict2 = {'a':6}

        self.assertTrue(jsonSchemaCheck([dict1, dict2]))

    def test_equal_recursive_jsons_should_have_same_shape(self):
        dict_ = {'a': {'b':5}}

        self.assertTrue(jsonSchemaCheck([dict_, dict_]))

    def test_same_shape_with_different_leaves_should_have_same_shape(self):
        dict1 = {'a': {'b':5}}
        dict2 = {'a': {'b':6}}

        self.assertTrue(jsonSchemaCheck([dict1, dict2]))

    def test_different_type_leaves_should_not_have_same_shape(self):
        dict1 = {'a': {'b':5}}
        dict2 = {'a': {'b':'five'}}

        self.assertFalse(jsonSchemaCheck([dict1, dict2]))

class DictionarySplineTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_values_of_controls_should_match_in_one_parameter(self):
        vector = [1, 2, 3, 4]
        times = [1, 2, 3, 4]

        matrix = [vector]

        v = DictionarySpline(times, matrix)
        results = [v(i) for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i][0], vector[i])

    def test_values_of_controls_should_match_in_two_parameters(self):
        vector1 = [1, 2, 3, 4]
        vector2 = [2, 3, 4, 5]
        times = [1, 2, 3, 4]

        matrix = [vector1, vector2]

        v = DictionarySpline(times, matrix)
        results = [v(i) for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i][0], vector1[i])
            self.assertAlmostEqual(results[i][1], vector2[i])

    def test_values_of_float_controls_should_match(self):
        vector = [1.0, 2.0, 3.0, 4.0]
        times = [1, 2, 3, 4]

        matrix = [vector]

        v = DictionarySpline(times, matrix)
        results = [v(i) for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i][0], vector[i])

    def test_integer_controls_should_remain_integers(self):
        vector = [10, 20, 30, 40]
        times = [1, 2, 3, 4]

        matrix = [vector]

        v = DictionarySpline(times, matrix)
        results = [v(i) for i in times]

        for v in results:
            self.assertTrue(isinstance(v[0], (int)))

    def test_strings_should_not_be_interpolated(self):
        vector = ["a", "b", "c", "d"]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for result in results:
            self.assertEqual(result, ["a"])

    def test_tuples_should_be_interpolated_piecewise(self):
        vector = [(1, 10), (2, 20), (3, 30), (4, 40)]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for i in range(4):
            self.assertTrue(isinstance(results[i][0], tuple))
            self.assertAlmostEqual(results[i][0][0], vector[i][0])
            self.assertAlmostEqual(results[i][0][1], vector[i][1])

    def test_tuples_should_be_interpolated_piecewise_even_if_other_params_are_present(self):
        vector1 = [(1, 10), (2, 20), (3, 30), (4, 40)]
        vector2 = [100, 200, 300, 400]
        times = [1, 2, 3, 4]
        matrix = [vector1, vector2]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for i in range(4):
            self.assertTrue(isinstance(results[i][0], tuple))
            self.assertAlmostEqual(results[i][0][0], vector1[i][0])
            self.assertAlmostEqual(results[i][0][1], vector1[i][1])
            self.assertAlmostEqual(results[i][1], vector2[i])

    def test_recursive_tuples_should_be_recursively_interpolated(self):
        vector = [
            ((1, 10), 100), ((2, 20), 200), ((3, 30), 300), ((4, 40), 400)]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for i in range(4):
            self.assertTrue(isinstance(results[i][0], tuple))
            self.assertTrue(isinstance(results[i][0][0], tuple))
            self.assertAlmostEqual(results[i][0][0][0], vector[i][0][0])
            self.assertAlmostEqual(results[i][0][0][1], vector[i][0][1])
            self.assertAlmostEqual(results[i][0][1], vector[i][1])

    def test_scalar_dictionaries_should_be_interpolated_regularly(self):
        vector = [{'x': 1}, {'x': 2}, {'x': 3}, {'x': 4}]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i][0]['x'], vector[i]['x'])

    def test_non_scalar_dictionaries_should_be_interpolated_correctly(self):
        vector = [
            {'x': 1, 'y': 10, 'z': 100},
            {'x': 2, 'y': 20, 'z': 200},
            {'x': 3, 'y': 30, 'z': 300},
            {'x': 4, 'y': 40, 'z': 400}]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i][0]['x'], vector[i]['x'])
            self.assertAlmostEqual(results[i][0]['y'], vector[i]['y'])
            self.assertAlmostEqual(results[i][0]['z'], vector[i]['z'])

    def test_recursive_dictionaries_should_be_interpolated_correctly(self):
        vector = [
            {'x': 1, 'y': 10, 'z': 100, 'd': {'a': 5}},
            {'x': 2, 'y': 20, 'z': 200, 'd': {'a': 6}},
            {'x': 3, 'y': 30, 'z': 300, 'd': {'a': 7}},
            {'x': 4, 'y': 40, 'z': 400, 'd': {'a': 8}}]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i) for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i][0]['x'], vector[i]['x'])
            self.assertAlmostEqual(results[i][0]['y'], vector[i]['y'])
            self.assertAlmostEqual(results[i][0]['z'], vector[i]['z'])
            self.assertAlmostEqual(
                results[i][0]['d']['a'], vector[i]['d']['a'])

    def test_multiple_elements_in_recursive_dictionaries_should_be_interpolated_correctly(self):
        vector = [
            {'x': 1, 'y': 10, 'z': 100, 'd': {'a': 5, 'b': -1, 'c': -10}},
            {'x': 2, 'y': 20, 'z': 200, 'd': {
                'a': 6, 'b': -2, 'c': -20}},
            {'x': 3, 'y': 30, 'z': 300, 'd': {
                'a': 7, 'b': -3, 'c': -30}},
            {'x': 4, 'y': 40, 'z': 400, 'd': {'a': 8, 'b': -4, 'c': -40}}]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i)[0] for i in times]

        for i in range(4):
            self.assertAlmostEqual(results[i]['d']['a'], vector[i]['d']['a'])
            self.assertAlmostEqual(results[i]['d']['b'], vector[i]['d']['b'])
            self.assertAlmostEqual(results[i]['d']['c'], vector[i]['d']['c'])

    def test_equal_elements_should_create_equal_spline(self):
        vector = [1, 1, 1, 1]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix)

        results = [v(i)[0] for i in times]

        self.assertSequenceEqual(results, vector)
        for i in range(3):
            intermediate = i + 0.5
            self.assertEqual(v(i)[0], 1)

    def test_should_create_dummy_spline_if_dummy_is_passed(self):
        vector = [1, 2, 3, 4]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix, DummySpline)

        results = [v(i)[0] for i in times]

        self.assertSequenceEqual(
            results, [vector[0] for i in range(len(vector))])

    def test_interpolating_function_should_be_passed_recursively(self):
        vector = [
                {'x': {'a': 1}},
                {'x': {'a': 2}},
                {'x': {'a': 3}},
                {'x': {'a': 4}}]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix, DummySpline)

        results = [v(i)[0] for i in times]

        self.assertSequenceEqual(
                results, [vector[0] for i in range(len(vector))])

    def test_interpolating_function_should_be_passed_recursively_more(self):
        vector = [
                {'x': {'a': {'b': 1}}},
                {'x': {'a': {'b': 2}}},
                {'x': {'a': {'b': 3}}},
                {'x': {'a': {'b': 4}}}]
        times = [1, 2, 3, 4]
        matrix = [vector]
        v = DictionarySpline(times, matrix, DummySpline)

        results = [v(i)[0] for i in times]

        self.assertSequenceEqual(
                results, [vector[0] for i in range(len(vector))])

    def test_differently_shaped_trees_should_cause_exception(self):
        vector = [
            {'x': 1, 'y': 10},
            {'x': 1},
            {'x': 1},
            {'x': 1}]
        times = [1, 2, 3, 4]
        matrix = [vector]

        self.assertRaises(Exception, DictionarySpline, times, matrix)


class ConstraintSplineTest(unittest.TestCase):

    def setUp(self):
        self.times = [10, 20, 30, 40]

    def double(self, x):
        return 2*x

    def test_if_no_constraint_is_added_spline_should_only_forward(self):
        c = ConstraintSpline(DummySpline, self.times, [1, 2, 3, 4])
        values = [c(i) for i in self.times]

        for v in values:
            self.assertEqual(v, 1)

    def test_if_no_constraint_is_added_spline_should_only_forward_float(self):
        c = ConstraintSpline(DummySpline, self.times, [1.0, 2.0, 3.0, 4.0])
        values = [c(i) for i in self.times]

        for v in values:
            self.assertEqual(v, 1.0)

    def test_if_constraint_is_int_type_of_values_should_be_int(self):
        c = ConstraintSpline(DummySpline, self.times, [1.0, 2.0, 3.0, 4.0], constraint=int)
        values = [c(i) for i in self.times]

        for v in values:
            self.assertTrue(isinstance(v, (int)))

    def test_if_function_is_provided_function_should_be_used(self):
        c = ConstraintSpline(DummySpline, self.times, [1, 2, 3, 4], constraint=self.double)
        values = [c(i) for i in self.times]

        for v in values:
            self.assertEqual(v, self.double(1))

if __name__ == "__main__":
    unittest.main()
