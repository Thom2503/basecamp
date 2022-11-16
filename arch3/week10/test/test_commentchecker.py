from commentchecker import *


def test_check_comments():
    full_path = "/Users/thom2503/Documents/School/basecamp/arch3/week10/functiontest.txt"
    result = check_comments(full_path)

    assert result == [f"File: {full_path} contains a function [function_without_comment()] on line [1] without a preceding comment."], \
            "No correct comment is printed in functiontest.txt"