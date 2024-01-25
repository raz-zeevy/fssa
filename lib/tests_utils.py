def diff_lines_num(pred_path : str, true_path: str):
    """
    return the number of lines that are different between the two files
    :param path1:
    :param path2:
    :return:
    """
    with open(pred_path, "r") as f1, open(true_path, "r") as f2:
        pred_lines = f1.readlines()
        true_lines = f2.readlines()
        diff = abs(len(pred_lines) - len(true_lines))
        for i in range(min(len(pred_lines), len(true_lines))):
            line_p, line_tr = pred_lines[i], true_lines[i]
            if line_p != line_tr:
                diff += 1
        return diff