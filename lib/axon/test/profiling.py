# coding: utf-8

import pstats, cProfile

import test_vs_json as test

cProfile.runctx("test.run()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
