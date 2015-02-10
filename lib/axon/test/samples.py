from __future__ import unicode_literals

text_1_o = text_1_0 = text_1_1 = text_1_2 = '''{}'''

#################################

text_2_o = '''
 {
   }
'''
text_2_0 = text_2_1 = text_2_2 = '''{}'''

text_2c_o = '''
 { # comment...
# comments
# ....
   }
'''
text_2c_0 = text_2c_1 = text_2c_2 = '''{}'''

#################################

text_3c_o = '''
# comments...
  {   
# comments
# ....
     
     }
'''
text_3c_0 = text_3c_1 = text_3c_2 = '''{}'''

#################################

text_4_o = text_4_0 = text_4_1 = text_4_2 = '''[]'''

#################################

text_5_o = '''
 [
   ]
'''
text_5_0 = text_5_1 = text_5_2 = '''[]'''

text_5c_o = '''
 [ # comment...
# comments
# ....

   ]
'''
text_5c_0 = text_5c_1 = text_5c_2 = '''[]'''

#################################

text_6_o = '''
 [   
     
     ]
'''
text_6_0 = text_6_1 = text_6_2 = '''[]'''

text_6c_o = '''
# comments...
 [   
# comments
# ....
     
     ]
'''
text_6c_0 = text_6c_1 = text_6c_2 = '''[]'''

#################################

text_7_o = '''aaa{}'''
text_7_0 = '''aaa{}'''
text_7_1 = '''aaa {}'''
text_7_2 = '''aaa:'''

#################################

text_7a_o = '''aaa.bbb{}'''
text_7a_0 = '''aaa.bbb{}'''
text_7a_1 = '''aaa.bbb {}'''
text_7a_2 = '''aaa.bbb:'''

#################################

text_7b_o = """'aaa@bbb'{}"""
text_7b_0 = """'aaa@bbb'{}"""
text_7b_1 = """'aaa@bbb' {}"""
text_7b_2 = """'aaa@bbb':"""

#################################

text_8_o = '''aaa{1 2 3}'''
text_8_0 = '''aaa{1 2 3}'''
text_8_1 = '''aaa {
  1
  2
  3}'''
text_8_2 = '''aaa:
  1
  2
  3'''


#################################

text_8a_o = '''aaa:
    1   2
    3 4
'''
text_8a_0 = '''aaa{1 2 3 4}'''
text_8a_1 = '''aaa {
  1
  2
  3
  4}'''
text_8a_2 = '''aaa:
  1
  2
  3
  4'''

text_8c_o = '''aaa:
    # comments
    # ....
    1   2 # comment
    # comment
    3 4
'''
text_8c_0 = '''aaa{1 2 3 4}'''
text_8c_1 = '''aaa {
  1
  2
  3
  4}'''
text_8c_2 = '''aaa:
  1
  2
  3
  4'''

#################################

text_9_o = '''aaa{a:1 b:2 c:3}'''
text_9_0 = '''aaa{a:1 b:2 c:3}'''
text_9_1 = '''aaa {
  a: 1
  b: 2
  c: 3}'''
text_9_2 = '''aaa:
  a: 1
  b: 2
  c: 3'''

#################################

text_9a_o = '''aaa{'a':1 b:2 'c@d':3}'''
text_9a_0 = '''aaa{a:1 b:2 'c@d':3}'''
text_9a_1 = '''aaa {
  a: 1
  b: 2
  'c@d': 3}'''
text_9a_2 = '''aaa:
  a: 1
  b: 2
  'c@d': 3'''

#################################

text_10_o = '''aaa{a:1 b:2 c:3 4 5 6}'''
text_10_0 = '''aaa{a:1 b:2 c:3 4 5 6}'''
text_10_1 = '''aaa {
  a: 1
  b: 2
  c: 3
  4
  5
  6}'''
text_10_2 = '''aaa:
  a: 1
  b: 2
  c: 3
  4
  5
  6'''

#################################

text_10a_o = '''aaa:
   a:1
   b:2
   c:3
   4    5   6
'''
text_10a_0 = '''aaa{a:1 b:2 c:3 4 5 6}'''
text_10a_1 = '''aaa {
  a: 1
  b: 2
  c: 3
  4
  5
  6}'''
text_10a_2 = '''aaa:
  a: 1
  b: 2
  c: 3
  4
  5
  6'''

text_10c_o = '''
# comments
# ...
aaa:
   # comment
   a:1 # comment
   # comment
   b:2
   # comment
   # comment
   c:3 # comment
   # comment
   4    5   6
'''
text_10c_0 = '''aaa{a:1 b:2 c:3 4 5 6}'''
text_10c_1 = '''aaa {
  a: 1
  b: 2
  c: 3
  4
  5
  6}'''
text_10c_2 = '''aaa:
  a: 1
  b: 2
  c: 3
  4
  5
  6'''

text_10cc_o = '''
# comments
# ...
aaa {
   # comment
   a:1 # comment
   # comment
   b:2
   # comment
   # comment
   c:3 # comment
   # comment
   4    5   6 }
'''
text_10cc_0 = '''aaa{a:1 b:2 c:3 4 5 6}'''
text_10cc_1 = '''aaa {
  a: 1
  b: 2
  c: 3
  4
  5
  6}'''
text_10cc_2 = '''aaa:
  a: 1
  b: 2
  c: 3
  4
  5
  6'''

text_10d_o = '''
# comments
# ...
aaa {
   # comment
a:1 # comment
  # comment
  b:2
   # comment
 # comment
        c:3 # comment
                # comment
   4    
        5   
            6 }
'''
text_10d_0 = '''aaa{a:1 b:2 c:3 4 5 6}'''
text_10d_1 = '''aaa {
  a: 1
  b: 2
  c: 3
  4
  5
  6}'''
text_10d_2 = '''aaa:
  a: 1
  b: 2
  c: 3
  4
  5
  6'''

#################################

text_11_o = '''aaa{bbb{} ccc{}}'''
text_11_0 = '''aaa{bbb{} ccc{}}'''
text_11_1 = '''aaa {
  bbb {}
  ccc {}}'''
text_11_2 = '''aaa:
  bbb:
  ccc:'''

#################################

text_12_o = '''
aaa:
  a: 1
  b:2
  bbb:
  ccc:
    c:1
    ddd:
      '''
text_12_0 = '''aaa{a:1 b:2 bbb{} ccc{c:1 ddd{}}}'''
text_12_1 = '''aaa {
  a: 1
  b: 2
  bbb {}
  ccc {
    c: 1
    ddd {}}}'''
text_12_2 = '''aaa:
  a: 1
  b: 2
  bbb:
  ccc:
    c: 1
    ddd:'''

text_12c_o = '''
# comments
# comments
aaa:
  # comments
  a: 1 # comments
  # comments
  b:2 # comments
  # comments
  bbb:
  
  # comments  
  ccc:
    # comments
    c:1 # comments
    # comments
    ddd:
      '''
text_12c_0 = '''aaa{a:1 b:2 bbb{} ccc{c:1 ddd{}}}'''
text_12c_1 = '''aaa {
  a: 1
  b: 2
  bbb {}
  ccc {
    c: 1
    ddd {}}}'''
text_12c_2 = '''aaa:
  a: 1
  b: 2
  bbb:
  ccc:
    c: 1
    ddd:'''

text_12cc_o = '''
# comments
# comments
aaa {
  # comments
  a: 1 # comments
  # comments
  b:2 # comments
  # comments
  bbb {}
    
  # comments  
  ccc {
    # comments
    c:1 # comments
    # comments
    ddd {}
  }
}
      '''
text_12cc_0 = '''aaa{a:1 b:2 bbb{} ccc{c:1 ddd{}}}'''
text_12cc_1 = '''aaa {
  a: 1
  b: 2
  bbb {}
  ccc {
    c: 1
    ddd {}}}'''
text_12cc_2 = '''aaa:
  a: 1
  b: 2
  bbb:
  ccc:
    c: 1
    ddd:'''

#################################

text_13_o = '''
aaa:
  a: 1 
  b:2 c:    12
  bbb:    
  ccc:
    c:1     d:""
    ddd:
      1 
      2 
      a:1
'''
text_13_0 = '''aaa{a:1 b:2 c:12 bbb{} ccc{c:1 d:"" ddd{1 2 a:1}}}'''
text_13_1 = '''aaa {
  a: 1
  b: 2
  c: 12
  bbb {}
  ccc {
    c: 1
    d: ""
    ddd {
      1
      2
      a: 1}}}'''
text_13_2 = '''aaa:
  a: 1
  b: 2
  c: 12
  bbb:
  ccc:
    c: 1
    d: ""
    ddd:
      1
      2
      a: 1'''

text_13c_o = '''
# comments
aaa:
  # comments
  a: 1 # comments
  # comments
  b:2 c:    12
  # comments
  bbb:    
  # comments
  ccc:
    # comments
    c:1     d:""
    # comments
    ddd:
      1 # comments
      # comments
      2 # comments
      a:1
'''
text_13c_0 = '''aaa{a:1 b:2 c:12 bbb{} ccc{c:1 d:"" ddd{1 2 a:1}}}'''
text_13c_1 = '''aaa {
  a: 1
  b: 2
  c: 12
  bbb {}
  ccc {
    c: 1
    d: ""
    ddd {
      1
      2
      a: 1}}}'''
text_13c_2 = '''aaa:
  a: 1
  b: 2
  c: 12
  bbb:
  ccc:
    c: 1
    d: ""
    ddd:
      1
      2
      a: 1'''


#################################

text_14_o = '''
aaa:
  a: 1
  b: 2
  c: c:
    e: 1
    f: f:
      r: 2
      s: 3
  d: 4
'''
text_14_0 = '''aaa{a:1 b:2 c:c{e:1 f:f{r:2 s:3}} d:4}'''
text_14_1 = '''aaa {
  a: 1
  b: 2
  c: c {
    e: 1
    f: f {
      r: 2
      s: 3}}
  d: 4}'''
text_14_2 = '''aaa:
  a: 1
  b: 2
  c: c:
    e: 1
    f: f:
      r: 2
      s: 3
  d: 4'''

text_14c_o = '''\
aaa:
  # comments
  a: 1 # comments
  b: 2 # comments
  # comments
  c: c:
    # comments
    e: 1
    # comments
    f: f:
      # comments
      r: 2 # comments
      s: 3 # comments
  # comments
  d: 4
'''
text_14c_0 = '''aaa{a:1 b:2 c:c{e:1 f:f{r:2 s:3}} d:4}'''
text_14c_1 = '''aaa {
  a: 1
  b: 2
  c: c {
    e: 1
    f: f {
      r: 2
      s: 3}}
  d: 4}'''
text_14c_2 = '''aaa:
  a: 1
  b: 2
  c: c:
    e: 1
    f: f:
      r: 2
      s: 3
  d: 4'''

#################################

text_15_o = '''aaa:
  1 2
  bbb {1 2 3}
  3 4
'''
text_15_0 = '''aaa{1 2 bbb{1 2 3} 3 4}'''
text_15_1 = '''aaa {
  1
  2
  bbb {
    1
    2
    3}
  3
  4}'''
text_15_2 = '''aaa:
  1
  2
  bbb:
    1
    2
    3
  3
  4'''

text_15c_o = '''aaa:
  # comments
  1 2 # comments
  # comments
  # comments
  bbb {1 2 3} # comments
  # comments
  3 4
'''
text_15c_0 = '''aaa{1 2 bbb{1 2 3} 3 4}'''
text_15c_1 = '''aaa {
  1
  2
  bbb {
    1
    2
    3}
  3
  4}'''
text_15c_2 = '''aaa:
  1
  2
  bbb:
    1
    2
    3
  3
  4'''

#################################

text_16_o = '''aaa{1}'''
text_16_0 = '''aaa{1}'''
text_16_1 = '''aaa {1}'''
text_16_2 = '''aaa:
  1'''

#################################

text_17_o = '''(1)'''
text_17_0 = '''(1)'''
text_17_1 = '''(1)'''
text_17_2 = '''(1)'''

text_17l_o = '''[1]'''
text_17l_0 = '''[1]'''
text_17l_1 = '''[1]'''
text_17l_2 = '''[1]'''

text_18_o = '''(1 2)'''
text_18_0 = '''(1 2)'''
text_18_1 = '''( 1
  2)'''
text_18_2 = '''( 1
  2)'''

text_19_o = '''[1 2]'''
text_19_0 = '''[1 2]'''
text_19_1 = '''[ 1
  2]'''
text_19_2 = '''[ 1
  2]'''

text_20_o = '''(1 a{1})'''
text_20_0 = '''(1 a{1})'''
text_20_1 = '''( 1
  a {1})'''
text_20_2 = '''( 1
  a:
    1)'''

text_21_o = '''{a: 1}'''
text_21_0 = '''{a:1}'''
text_21_1 = '''{a: 1}'''
text_21_2 = '''{a: 1}'''

text_22_o = '''{a: 1 b: 2}'''
text_22_0 = '''{a:1 b:2}'''
text_22_1 = '''{ a: 1
  b: 2}'''
text_22_2 = '''{ a: 1
  b: 2}'''

text_23_o = '''aaa{a: {c:3} b: {d:4}}'''
text_23_0 = '''aaa{a:{c:3} b:{d:4}}'''
text_23_1 = '''aaa {
  a: {c: 3}
  b: {d: 4}}'''
text_23_2 = '''aaa:
  a: {c: 3}
  b: {d: 4}'''

text_24_o = '''aaa{a: {c:3 d:4} b: {d:4 e:5}}'''
text_24_0 = '''aaa{a:{c:3 d:4} b:{d:4 e:5}}'''
text_24_1 = '''aaa {
  a: {
    c: 3
    d: 4}
  b: {
    d: 4
    e: 5}}'''
text_24_2 = '''aaa:
  a: {
    c: 3
    d: 4}
  b: {
    d: 4
    e: 5}'''

text_25_o = '''aaa{a: [3 4] b: [4 5]}'''
text_25_0 = '''aaa{a:[3 4] b:[4 5]}'''
text_25_1 = '''aaa {
  a: [
    3
    4]
  b: [
    4
    5]}'''
text_25_2 = '''aaa:
  a: [
    3
    4]
  b: [
    4
    5]'''

text_26_o = '''[{c:3 d:4} {d:4 e:5}]'''
text_26_0 = '''[{c:3 d:4} {d:4 e:5}]'''
text_26_1 = '''[ { c: 3
    d: 4}
  { d: 4
    e: 5}]'''
text_26_2 = '''[ { c: 3
    d: 4}
  { d: 4
    e: 5}]'''

text_27_o = '''p:
'''
text_27_0 = '''p{}'''
text_27_1 = '''p {}'''
text_27_2 = '''p:'''

text_28_o = '''{"123":123}'''
text_28_0 = '''{"123":123}'''
text_28_1 = '''{"123": 123}'''
text_28_2 = '''{"123": 123}'''

