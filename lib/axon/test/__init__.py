# {{LICENCE}}

from axon.test.test_int import *
from axon.test.test_float import *
from axon.test.test_decimal import *
from axon.test.test_string import *
from axon.test.test_constant import *
from axon.test.test_datetime import *
from axon.test.test_list import *
from axon.test.test_dict import *
from axon.test.test_tuple import *
#from axon.test.test_set import *
from axon.test.test_element import *
from axon.test.test_mapping import *
from axon.test.test_sequence import *
from axon.test.test_instance import *
from axon.test.test_safe_loads import *
from axon.test.test_unsafe_loads import *
from axon.test.test_crossref import *
from axon.test.test_base64 import *
from axon.test.test_errors import *
from axon.test.test_samples import *

def test_all():
    import unittest
    unittest.main(verbosity=2)
