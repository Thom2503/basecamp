def rec_print_folders(n: int, pref: str, root: list) -> None:
    """
    This function prints the contents of a given root folder with indentations.

    :param n: int, which folder
    :param pref: str, folder pref
    :param root: list, folder list
    """
    for i, item in enumerate(root):
        if isinstance(item, list):
            pref = (">" * n)
            # item is a folder, so print the folder name with indentation
            print(f"{pref}>Folder_{n}")
            # call the function recursively on the folder
            rec_print_folders(n+1, pref, item)
        else:
            pref = ("-" * n)
            # item is a file, so print the file name with indentation
            print(f"{pref}- {item}")


def rec_count_files(root: list) -> int:
    """
    The functions counts number of files in a given folder (and all its sub-folders).

    :param root: list, an element either is a file (name) or a list as a sub-folder.
    :return count: int, hoeveel folders er zijn
    """
    count = 0
    for item in root:
        if isinstance(item, list):
            # item is a folder, so call the function recursively on the folder
            count += rec_count_files(item)
        else:
            # item is a file, so increment the counter
            count += 1
    return count


if __name__ == "__main__":
    test_cases = [
        ['file_1', []],
        ['file_1', 'file_2', ['file_1']],
        ['file_1', 'file_2', ['file_3', 'file_4', 'file_5'], ['file_6', ['file_7', 'file_8'], ['file_9'], 'file_9', ['file_10']], []],
        ['file_1', ['file_3', ['file_2', ['file_10', ['file_9', 'file_8']]]], []],
        [[], [[], [[]]]]
    ]

    for case in test_cases:
        rec_print_folders(0, '', case)
        print('Number of files in case: ', case, ' is ', rec_count_files(case))
