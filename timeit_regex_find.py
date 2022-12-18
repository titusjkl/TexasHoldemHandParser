import timeit

rpt = 10
nmbr = 100**5


setup = """
import re

string = "Seat 1: Tuxopek ($1.07 in chips)"
output = re.search(".*?\:(.*)\(.*", string)
"""
min_regex = min(timeit.Timer(setup=setup).repeat(repeat=rpt, number=nmbr))

setup = """
import re

string = "Seat 1: Tuxopek ($1.07 in chips)"
name_start = string.find(":") + 2
name_end = string.find("(") - 1
output = string[name_start : name_end]
"""
min_find = min(timeit.Timer(setup=setup).repeat(repeat=rpt, number=nmbr))


print(f"Min Regex: {min_regex} - Min Find: {min_find} - Difference: {min_find-min_regex}")