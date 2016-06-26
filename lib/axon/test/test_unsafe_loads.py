# coding: utf-8

from __future__ import unicode_literals, print_function
import unittest
import axon
from axon.odict import OrderedDict

class C(object):
    pass

class D(object):
    pass

class E(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def instance_maker(cls):
    def make_instance(attrs, vals=None):
        inst = cls.__new__(cls)
        for name, value in attrs.items():
            setattr(inst, name, value)
        return inst
    return make_instance

def reducer_maker(cls):
    def type_reducer(o):
        attrs = []
        for name in o.__dict__:
            if name.startswith('_'):
                continue
            attrs.append((axon.as_name(name), getattr(o, name)))

        return axon.node(axon.as_name(cls.__name__), attrs, None)
    return type_reducer


axon.factory('C', instance_maker(C))
axon.factory('D', instance_maker(D))
axon.factory('E', instance_maker(E))

axon.reduce(C, reducer_maker(C))
axon.reduce(D, reducer_maker(D))
axon.reduce(E, reducer_maker(E))

class Base(object):
    #
    def __str__(self):
        return '%s: %r' % (self.__class__.__name__, self.__dict__)
    #
    __repr__ = __str__

class Graph(Base):
    def __init__(self, nodes, edges):
        self.nodes = list(nodes) if nodes else []
        self.edges = list(edges) if edges else []
            
            
class Node(Base):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge(Base):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
        
@axon.factory('graph')
def create_graph2(attrs, args):
    return Graph(**attrs)

@axon.factory('node')
def create_node2(attrs, args):
    return Node(*args)

@axon.factory('edge')
def create_edge(attrs, args):
    return Edge(*args)

@axon.reduce(Graph)
def reduce_graph(graph):
    return axon.node('graph', {'nodes':graph.nodes, 
                               'edges':graph.edges}, None)

@axon.reduce(Node)
def reduce_node(node):
    return axon.node('node', None, [node.x, node.y])

@axon.reduce(Edge)
def reduce_edge(edge):
    return axon.node('edge', None, [edge.p1, edge.p2])


class UnsafeLoadsTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_usafe_1(self):
        v = C()
        v.a = 1
        v.b = 2
        v.c = 3
        text = axon.dumps([v])
        #display(text)
        v1 = axon.loads(text, mode='strict')[0]
        self.assertEqual(v.a, v1.a)
        self.assertEqual(v.b, v1.b)
        self.assertEqual(v.c, v1.c)
    #
    def test_usafe_2(self):
        v = C()
        v.a = 1
        v.b = 2
        v.c = 3
        w = D()
        w.a = 'a'
        w.b = [1,2]
        w.c = 2
        text = axon.dumps([v, w])
        v1, w1 = axon.loads(text, mode='strict')
        self.assertEqual(v.a, v1.a)
        self.assertEqual(v.b, v1.b)
        self.assertEqual(v.c, v1.c)
        self.assertEqual(w.a, w1.a)
        self.assertEqual(w.b, w1.b)
        self.assertEqual(w.c, w1.c)
    #
    def test_usafe_3(self):
        v = E(1, 2, 3)
        text = axon.dumps([v])
        v1 = axon.loads(text, mode='strict')[0]
        self.assertEqual(v.a, v1.a)
        self.assertEqual(v.b, v1.b)
        self.assertEqual(v.c, v1.c)
    #
    def test_usafe_4(self):
        v = C()
        v.x = 1
        v.y = lst = []
        for i in range(3):
            w = D()
            w.z = i
            lst.append(w)
        text = axon.dumps([v])
        #self.assertEqual(text, 'C{x:1 y:[D{z:0} D{z:1} D{z:2}]}')
        v1 = axon.loads(text, mode='strict')[0]
        self.assertEqual(v1.x, 1)
        self.assertEqual(len(v1.y), 3)
        self.assertEqual(all([type(z) is D for z in v1.y]), True)
        self.assertEqual(all([z.z==z1.z for z,z1 in zip(v1.y, lst)]), True)
    #
    def test_usafe_5(self):
        vs = []
        v = C()
        v.x = 1
        v.y = lst = []
        for i in range(3):
            w = D()
            w.z = i
            lst.append(w)
            vs.append(w)
        vs.append(v)
        text = axon.dumps(vs, crossref=1, pretty=1)
#         self.assertEqual(text, '''\
# &1 D:
#   z: 0
# &2 D:
#   z: 1
# &3 D:
#   z: 2
# C:
#   x: 1
#   y: [*1 *2 *3]''')
        self.assertEqual(vs[-1].y[0], vs[0])
        self.assertEqual(vs[-1].y[1], vs[1])
        self.assertEqual(vs[-1].y[2], vs[2])
    #
#     def test_usafe_6(self):
#         text = """\
# graph {
#   nodes: [
#     &1 node {
#       1 1}
#     &2 node {
#       1 2}
#     &3 node {
#       2 1}
#     &4 node {
#       2 2}]
#   edges: [
#     edge {
#       *1
#       *2}
#     edge {
#       *1
#       *3}
#     edge {
#       *2
#       *3}
#     edge {
#       *1
#       *4}
#     edge {
#       *3
#       *4}]}
# """
#         obs = axon.loads(text, mode='strict')
#         text2 = axon.dumps(obs, crossref=1, sorted=0)
#         obs2 = axon.loads(text2, mode='strict')
#         print(axon.dumps(obs2, crossref=1, sorted=0))
#         self.assertEqual(obs2[0].nodes[0] is obs2[0].edges[0].p1, True)
#         self.assertEqual(obs2[0].nodes[1] is obs2[0].edges[0].p2, True)
#         self.assertEqual(obs2[0].nodes[2] is obs2[0].edges[1].p2, True)
#         self.assertEqual(obs2[0].nodes[2] is obs2[0].edges[2].p2, True)
#         self.assertEqual(obs2[0].nodes[2] is obs2[0].edges[4].p1, True)
#         self.assertEqual(obs2[0].nodes[3] is obs2[0].edges[3].p2, True)
#         self.assertEqual(obs2[0].nodes[3] is obs2[0].edges[4].p2, True)
#
        


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnsafeLoadsTestCase))
    return suite
