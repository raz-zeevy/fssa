import numpy as np


def safe_convert_to_float(arr, placeholder=np.nan):
    """Converts an array of strings to floats, with empty strings replaced by a placeholder."""
    return np.array([float(x) if x != "" else placeholder for x in arr])

def safe_restore_empty_strings(arr, placeholder=np.nan):
    """Converts an array of floats back to strings, with placeholder values replaced by empty strings."""
    return np.array([str(int(x)) if not np.isnan(x) else "" for x in arr])


# a decorator that uses the save_convert_to_float function to convert the input to float
# and then calls the safe restore empty strings function to convert the output back to strings
def safe_conversion(func):
    def wrapper(*args, **kwargs):
        values = safe_convert_to_float(args[0])
        # Handle non-empty values only for computation
        non_empty_mask = ~np.isnan(values)
        non_empty_values = values[non_empty_mask]

        # Step 2: Apply the original operation to non-empty values
        grouped_values = np.empty(values.shape)
        grouped_values[:] = np.nan
        grouped_values[non_empty_mask] = func(non_empty_values,
                                             *args[1:], **kwargs)

        # Step 3: Convert back to strings, preserving empty strings
        return safe_restore_empty_strings(grouped_values)
    return wrapper


def needs_recoding(values : np.array):
    """
    this function checks if the values need recoding
    :param values: the values to check
    """
    res = {
        "passed": True,
        "entry": "",
        "col_num": -1
    }
    int_values = []
    for row in values:
        row_vals = []
        for value in row:
            try:
                row_vals.append(int(value))
            except ValueError:
                row_vals.append(0)
        int_values.append(row_vals)
    for i, col in enumerate(np.array(int_values).T):
        if np.amax(col) > 100 or np.amin(col) < 0:
            res["passed"] = False
            res["col_num"] = i+1
            return res
    return res
@safe_conversion
def group_by_precentile(values: np.array, groups_num):
    """
    this function substitute the values with the percentile group they
    belong to according to the groups_num
    :param values:  the values to group
    :param groups_num:  the number of groups to divide the values into
    :return:
    """
    actual_values = values[~np.isnan(values)]
    groups = np.percentile(actual_values,
                           np.linspace(0, 100, groups_num + 1))
    groups[-1] += 1
    return np.digitize(values, groups)

@safe_conversion
def group_by_equal_range(values : np.array, groups_num):
    """
    this function substitute the values with the equal range group they
    belong to according to the groups_num
    :param values:  the values to group
    :param groups_num:  the number of groups to divide the values into
    :return:
    """
    groups = np.linspace(values.min(), values.max(), groups_num + 1)
    groups[-1] += 1
    return np.digitize(values, groups)

@safe_conversion
def group_by_monotonicity(values : np.array, groups_num):
    """
    this function substitute the values with the monotonicity group they
    belong to according to the groups_num
    :param values:  the values to group
    :param groups_num:  the number of groups to divide the values into
    :return:
    """
    sorted_unique, first_indices = np.unique(np.sort(values), return_index=True)

    # Step 2: Create a rank array based on the order of appearance in the sorted unique array
    # This will ensure continuous ranks starting from 1
    rank_values = np.zeros_like(values)

    # Step 3: Map the ranks back to the original array's positions
    for rank, value in enumerate(sorted_unique, start=1):
        rank_values[np.where(values == value)] = rank
    groups = np.linspace(rank_values.min(), rank_values.max(), groups_num + 1)
    groups[-1] += 1
    return np.digitize(rank_values, groups)

@safe_conversion
def clip_values(values : np.array, lower, upper):
    """
    this function clips the values to be between lower and upper
    :param values: the values to clip
    :param lower: the lower bound
    :param upper: the upper bound
    :return: the clipped values
    """
    return np.clip(values, lower, upper)

@safe_conversion
def manual_recoding(values: np.array, old_values : str, new_value : str):
    """
    this function recodes the old values to the new value
    :param values:  the values to recode
    :param old_values:  the values to recode
    :param new_value:  the new value to assign to the old values
    :return:
    """
    recoded_values = values.copy()
    new_value = int(new_value)
    # parse old_values to range if there is "-" inside of it
    if "-" in old_values:
        low, high = [int(num) for num in old_values.split("-")]
        recoded_values[(recoded_values >= low) & (recoded_values <= high)] = new_value
    else:
        old_value = int(old_values)
        recoded_values[recoded_values == old_value] = new_value
    return recoded_values


@safe_conversion
def invert(values: np.array, valid_ranges: list = None):
    """
    This function inverts the values, ignoring the missing values that fall
    outside the valid ranges.

    :param values: The values to invert
    :param valid_ranges: A list of tuples representing valid value ranges.
                         Each tuple is (start, end), inclusive.
    :return: The inverted values, with missing values unchanged
    """
    if not valid_ranges:
        return values

    # Convert the input to a copy to avoid modifying the original
    inverted_values = values.copy()

    for start, end in valid_ranges:
        # Get a boolean mask for the current range
        in_range = (values >= start) & (values <= end)

        # Get the min and max for this range
        range_values = values[in_range]
        if range_values.size > 0:
            min_val, max_val = range_values.min(), range_values.max()

            # Invert only values within this range
            inverted_values[in_range] = max_val - range_values + min_val

    return inverted_values

def test_inverting():
    import numpy as np

    # Test Case 1: Simple range inversion
    values = np.array([1, 2, 3, 4, 5])
    valid_ranges = [(1, 5)]
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 1:", output)  # Expected: [5, 4, 3, 2, 1]
    assert output == [5, 4, 3, 2, 1]

    # Test Case 2: Partial valid range
    values = np.array([1, 2, 3, 4, 5])
    valid_ranges = [(2, 4)]
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 2:",
          output)  # Expected: [1, 4, 3, 2, 5]
    assert output == [1, 4, 3, 2, 5]

    # Test Case 3: Multiple valid ranges
    values = np.array([1, 2, 3, 4, 5, 6, 7])
    valid_ranges = [(1, 3), (5, 7)]
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 3:",
          output)  # Expected: [3, 2, 1, 4, 7, 6, 5]
    assert output == [3, 2, 1, 4, 7, 6, 5]

    # Test Case 4: Empty valid range
    values = np.array([1, 2, 3, 4, 5])
    valid_ranges = []
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 4:", output)  # Expected: [1, 2, 3, 4, 5]
    assert output == [1, 2, 3, 4, 5]

    # Test Case 5: No valid values in input
    values = np.array([8, 9, 10])
    valid_ranges = [(1, 5)]
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 5:", output)  # Expected: [8, 9, 10]
    assert output == [8, 9, 10]

    # Test Case 6: Mixed valid and invalid values
    values = np.array([1, 10, 3, 20, 5])
    valid_ranges = [(1, 5)]
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 6:",output)  # Expected: [5, 10, 3, 20, 1]
    assert output == [5, 10, 3, 20, 1]

    # Test Case 7: Single value range
    values = np.array([1, 2, 3, 4, 5])
    valid_ranges = [(3, 3)]
    output = [int(i) for i in invert(values, valid_ranges)]
    print("Test Case 7:", output)  # Expected: [1, 2, 3, 4, 5]
    assert output == [1, 2, 3, 4, 5]

def test_manual_recoding():
    import numpy as np

    # Scenario 1: Single value recoding
    values = np.array([1, 2, 3, 4, 5])
    old_values = "3"
    new_value = "99"
    result = [int(i) for i in manual_recoding(values, old_values, new_value)]
    print("Scenario 1:", result)  # Expected: [1, 2, 99, 4, 5]
    assert np.array_equal(result, [1, 2, 99, 4, 5])

    # Scenario 2: Range recoding
    values = np.array([1, 2, 3, 4, 5])
    old_values = "2-4"
    new_value = "10"
    result = [int(i) for i in manual_recoding(values, old_values, new_value)]
    print("Scenario 2:", result)  # Expected: [1, 10, 10, 10, 5]
    assert np.array_equal(result, [1, 10, 10, 10, 5])

    # Scenario 3: No matching old values
    values = np.array([1, 2, 3, 4, 5])
    old_values = "6"
    new_value = "20"
    result = [int(i) for i in manual_recoding(values, old_values, new_value)]
    print("Scenario 3:", result)  # Expected: [1, 2, 3, 4, 5]
    assert np.array_equal(result, [1, 2, 3, 4, 5])

    # Scenario 4: Recoding entire range of values
    values = np.array([1, 2, 3, 4, 5])
    old_values = "1-5"
    new_value = "0"
    result = [int(i) for i in manual_recoding(values, old_values, new_value)]
    print("Scenario 4:", result)  # Expected: [0, 0, 0, 0, 0]
    assert np.array_equal(result, [0, 0, 0, 0, 0])

    # Scenario 6: Overlapping ranges with single value recoding
    values = np.array([1, 2, 3, 4, 5])
    old_values_1 = "2-4"
    new_value_1 = "10"
    result = manual_recoding(values, old_values_1, new_value_1)
    old_values_2 = "10"
    new_value_2 = "20"
    result = [int(i) for i in manual_recoding(result, old_values_2,
                                              new_value_2)]
    print("Scenario 6:", result)  # Expected: [1, 20, 20, 20, 5]
    assert np.array_equal(result, [1, 20, 20, 20, 5])

    # Scenario 7: Empty array
    values = np.array([])
    old_values = "1-10"
    new_value = "5"
    result = [int(i) for i in manual_recoding(values, old_values, new_value)]
    print("Scenario 7:", result)  # Expected: []
    assert np.array_equal(result, [])

    print("All test cases passed!")

if __name__ == '__main__':
   test_inverting()
   test_manual_recoding()