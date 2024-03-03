import numpy as np

def needs_recoding(values : np.array):
    """
    this function checks if the values need recoding
    :param values: the values to check
    :return: True if the values need recoding, False otherwise
    """
    int_values = []
    for row in values:
        for value in row:
            try:
                int_values.append(int(value))
            except ValueError:
                pass
    return np.amax(int_values) > 100 or np.amin(int_values) < 0
def group_by_precentile(values : np.array, groups_num):
    """
    this function substitute the values with the percentile group they
    belong to according to the groups_num
    :param values:  the values to group
    :param groups_num:  the number of groups to divide the values into
    :return:
    """
    groups = np.percentile(values, np.linspace(0, 100, groups_num + 1))
    groups[-1] += 1
    return np.digitize(values, groups)
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



def clip_values(values : np.array, lower, upper):
    """
    this function clips the values to be between lower and upper
    :param values: the values to clip
    :param lower: the lower bound
    :param upper: the upper bound
    :return: the clipped values
    """
    return np.clip(values, lower, upper)

def invert(values : np.array):
    """
    this function inverts the values
    :param values: the values to invert
    :return: the inverted values
    """
    return values.max() - values + values.min()

if __name__ == '__main__':
    groups = 4
    # example_1 = np.array([1,2,3,4,5,6,7,8,9,10])
    # print(group_by_precentile(example_1, groups))
    # print(group_by_equal_range(example_1, groups))
    example_2 = np.array([1,30,2,2,3,2,2])
    print(group_by_monotonicity(example_2, groups))
    # print(group_by_equal_range(example_2, groups))
    # print(clip_values(example_2,1,3))
    # print(invert(example_2))