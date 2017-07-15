"""
Function to filter a string using an optional exact match whitelist (include),
 optional whitelist using regex (include_regex),
 exact match blacklist (exclude), and blacklist regex (exclude_regex)

See unittest below for usage examples

Code is from https://github.com/TomFaulkner/pypihole/blob/master/pypihole/,
 see there for changes
"""

import re


def ie_filter(entry: str, **kwargs) -> bool:
    """
    Include and exclude work as a whitelist and a blacklist.
    If include is not None, but is a list, then only whitelisted entries
     will be returned.
    If exclude is not None, but is a list, then anything blacklisted won't be
     returned.
    Both include and exclude can be provided at the same time, however, it
     the exclude list is redundant at that point, unless it overlaps with some
     of the whitelist, in which case whitelisted entries included in the
      blacklist will be excluded.

    :param entry: any string, intended for Query fields
    :return: boolean, whether to include or not

    kwargs:
    :param include: list of items to match and include, must be exact match
    :param exclude: list of items to exclude, must be exact match
    :param include_regex: list of regex strings to match and include
    :param exclude_regex: list of regex strings to match and exclude
    """

    def run_regex(target, patterns):
        for pattern in patterns:
            if re.search(pattern, target):
                return True
        else:
            return False

    def include_test():
        if not include and not include_regex:
            return True
        elif include or include_regex:
            if entry in include:
                return True
            elif run_regex(entry, include_regex):
                return True
            return False

    def exclude_test():
        if not exclude and not exclude_regex:
            return True
        elif exclude or exclude_regex:
            if entry in exclude:
                return False
            elif run_regex(entry, exclude_regex):
                return False
            return True

    include = kwargs.pop('include', [])
    exclude = kwargs.pop('exclude', [])
    include_regex = kwargs.pop('include_regex', [])
    exclude_regex = kwargs.pop('exclude_regex', [])

    if not include and not exclude and not include_regex and not exclude_regex:
        return True
    pass_include = include_test()
    pass_exclude = exclude_test()

    if include or include_regex:
        if pass_include and pass_exclude:
            return True
    elif exclude and pass_exclude:
        return True
    return False
