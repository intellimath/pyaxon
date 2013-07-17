# coding: utf-8

from __future__ import print_function, unicode_literals

from axon import *

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

try:
    unichr
except:
    unichr = chr

try:
    unicode = builtins.unicode
except AttributeError:
    unicode = builtins.str

import base64
from random import randint

def u(s):
    if type(s) is unicode:
        return s
    else:
        return unicode(s, 'utf-8')

pretty = False
crossref = False

def test_binary():
    print('Test binary')
    text = ''.join([unichr(randint(1,255)) for i in range(256)])
    bstr = text.encode('utf-8')
    print(bstr)
    text1 = '|'+ unicode(base64.encodestring(bstr), 'ascii')
    #print(text, len(bstr), len(text))
    items = loads(text1)
    print(items[0])
    assert items[0] == bstr
    text2 = dumps(items, crossref = crossref)
    assert text1 == text2
    print(text2)

def test(text, pretty=pretty, score=False):
    from time import time

    text = u(text)
    if not score:
        print(">>> ", text)
        item = loads(text)
        #print(item)
        text = dumps(item, pretty=pretty, crossref=crossref)
        #display(text)
        print(text)
        print(type(item[0]))
    else:
        print("Test Json Benchmark string")
        item = loads(text)
        t1 = time()
        N = 100
        for i in range(N):
            loads(text)
        dt1 = time() - t1
        t1 = time()
        for i in range(N):
            dumps(item, pretty=pretty, crossref=crossref)
        dt2 = time() - t1
        print(dt1/N, dt2/N)

def test_random(pretty=pretty):
    from random import choice, uniform
    from time import time

    alpha = [unicode(chr(i)) for i in range(ord('a'),ord('z')+1)]
    def randstr(n, alpha=alpha):
        return ''.join([choice(alpha) for i in range(n)])
    root = []
    m = 20000
    print('Test random items')
    t1 = time()
    for i in range(m):
        seq11 = sequence('bbb', [
            randint(1,1000),
            randint(1,1000),
            randint(1,1000),
        ])
        seq12 = [
            uniform(1.,1000.),
            uniform(1.,1000.),
            uniform(1.,1000.),
            uniform(1.,1000.),
        ]
        ob1 = {'name':randstr(12), 'age':randint(1,100)}
        seq2 = element('test', {'aaa':randstr(16)},
                [randint(1,10000), randint(1,10000),
                 uniform(1.,10000.), uniform(1.,10000.)])
        root.append(
            mapping(
                'alpha',
                {'name': randstr(8), 'id': randstr(4), 'val': seq11, 'val2':seq12,
                'b': ob1, 'others': seq2, 'flag': bool(randint(0,1))})
        )
    dt = time() - t1
    print('Create object', dt)

    t1 = time()
    text = dumps(root, pretty=pretty, crossref = crossref)
    #print(text)
    dt = time() - t1
    N = len(text)
    print('Dump object', dt)
    print(N)

    t1 = time()
    for o in iloads(text):
        pass
    dt = time() - t1
    print('iLoad text', dt, int(N/float(dt)))

    t1 = time()
    root = loads(text)
    dt = time() - t1
    print('Load text', dt, int(N/float(dt)))

    t1 = time()
    text = dumps(root, pretty=pretty, crossref = crossref)
    dt = time() - t1
    N = len(text)
    print('Dump object again', dt)


def test2():
    #from random import randint
    from time import time

    m = 40000
    root = []
    t1 = time()
    for i in range(m):
        seq1 = sequence('aaa', [123, 456, 45.1256421])
        ob1 = {'name':'belinda', 'age':65}
        seq2 = element('test', {'aaa':'qwewqewqeqw'}, [345, 789])
        root.append(
            mapping(
                'alpha',
                {'name': 'john', 'id': 'a', 'val': seq1,
                'b': ob1, 'others': seq2, 'flag': True})
        )
    dt = time() - t1
    print('Create object', dt)

    t1 = time()
    text = dumps(root, pretty=pretty, crossref = crossref)
    #print(text)
    dt = time() - t1
    N = len(text)
    print('Dump object', dt)
    print(N)

    t1 = time()
    v = [0]
    for o in iloads(text):
        pass
    dt = time() - t1
    print('iLoad text', dt, int(N/float(dt)))

    t1 = time()
    root=loads(text)
    dt = time() - t1
    print('Load text', dt, int(N/float(dt)))

    t1 = time()
    text = dumps(root, pretty=pretty, crossref = crossref)
    dt = time() - t1
    N = len(text)
    print('Dump object again', dt)

task_config = '''
config {
    data {
        type:"natural_fire"
        kind:"monthly"
        period:[5 6 7 8]
        years:[2001 2002 2003 2004 2005 2006 2007 2008]
        attrs:[temp osad]
        attr:count
        attr2:{a:1 b:1}
        [1 2 3]
        {a:1 b:2}
    }
    graph {
        [1 2 3]
        {a:1 b:2}
        type:"scatter"
        schema:"xy-z"
    }
    curve {rbf:{kind: "LS" gamma: 1.0}}
}
'''

json_string = """
{
    web_app: [
        servlet {
            name:"cofaxCDS"
            class:"org.cofax.cds.CDSServlet"
            init_param {
                configGlossary : {
                    installationAt:"Philadelphia PA"
                    adminEmail:"ksm@pobox.com"
                    poweredBy:"Cofax"
                    poweredByIcon:"/images/cofax.gif"
                    staticPath:"/content/static"}
                templateProcessorClass:"org.cofax.WysiwygTemplate"
                templateLoaderClass:"org.cofax.FilesTemplateLoader"
                templatePath:"templates"
                templateOverridePath:""
                defaultListTemplate:"listTemplate.htm"
                defaultFileTemplate:"articleTemplate.htm"
                useJSP:false
                jspListTemplate:"listTemplate.jsp"
                jspFileTemplate:"articleTemplate.jsp"
                cachePackageTagsTrack:200
                cachePackageTagsStore:200
                cachePackageTagsRefresh:60
                cacheTemplatesTrack:100
                cacheTemplatesStore:50
                cacheTemplatesRefresh:15
                cachePagesTrack:200
                cachePagesStore:100
                cachePagesRefresh:10
                cachePagesDirtyRead:10
                searchEngineListTemplate:"forSearchEnginesList.htm"
                searchEngineFileTemplate:"forSearchEngines.htm"
                dataStoreDriver:"com.microsoft.jdbc.sqlserver.SQLServerDriver"
                dataStoreUrl:"jdbc:microsoft:sqlserver://LOCALHOST:1433;DatabaseName:goon"
                dataStoreUser:"sa"
                dataStorePassword:"dataStoreTestQuery"
                dataStoreTestQuery:"SET NOCOUNT ON;select test='test';"
                dataStoreLogFile:"/usr/local/tomcat/logs/datastore.log"
                dataStoreInitConns:10
                dataStoreMaxConns:100
                dataStoreConnUsageLimit:100
                dataStoreLogLevel:"debug"
                maxUrlLength:500
            }
            servlet {
                name:"cofaxEmail"
                class:"org.cofax.cds.EmailServlet"
                init_param {
                    mailHost:"mail1"
                    mailHostOverride:"mail2"
                }
            }
            servlet{
                name:"cofaxAdmin"
                class:"org.cofax.cds.AdminServlet"
            }
            servlet{
                name:"fileServlet"
                class:"org.cofax.cds.FileServlet"
            }
            servlet{
                name:"cofaxTools"
                class:"org.cofax.cms.CofaxToolsServlet"
                init_param {
                    templatePath:"toolstemplates/"
                    log:1
                    logLocation:"/usr/local/tomcat/logs/CofaxTools.log"
                    logMaxSize:""
                    dataLog:1
                    dataLogLocation:"/usr/local/tomcat/logs/dataLog.log"
                    dataLogMaxSize:""
                    removePageCache:"/content/admin/remove?cache:pages&id:"
                    removeTemplateCache:"/content/admin/remove?cache:templates&id:"
                    fileTransferFolder:"/usr/local/tomcat/webapps/content/fileTransferFolder"
                    lookInContext:1
                    adminGroupID:4
                    betaServer:true
                }
            }
        }
        servlet_mapping {
            cofaxCDS:"/"
            cofaxEmail:"/cofaxutil/aemail/*"
            cofaxAdmin:"/admin/*"
            fileServlet:"/static/*"
            cofaxTools:"/tools/*"
        }
        taglib {
            taglib_uri:"cofax.tld"
            taglib_location:"/WEB-INF/tlds/cofax.tld"
        }
    ]
}
"""

def main():
    # samples
    test('0')
    test('-0')
    test('17')
    test('171717171717171717171718181818181818')
    test('-17')
    test('-17.34')
    test('17.34')
    test('-1e-6')
    test('1.734E12')
    test('-1.734e-12')
    test('-17.34$')
    test('-1.0e-6$')
    test('1.734E12$')
    test('1e-12$')
    test("NaN")
    test("Infinity")
    test("-Infinity")
    test('null')
    test('{}')
    test('"abc"')
    test('"a\tbc"')
    test("2010-10-01")
    test("10:10")
    test("10:10:20")
    test("10:10:20.100")
    test("10:10:20.3000")
    test("2010-10-01T10:10")
    test("2010-10-01T10:10:20")
    test(
        '"asasasas1\n # ddddd\\"dddddddd2\n @ sasafgfghgfhg3\n ! xvxcvcxvcv4"'
    )
    test(
        '"asasasas1\n # ddddd\\"dddddddd2\n @ sasafgfghgfhg3\n ! xvxcvcx\\"\\"vcv4"'
    )
    test('"\\u0041\\U0042"')
    test('true')
    test('false')
    test('[1 2 3]')
    test('[ 1 2 3 ]')
    test(
    '''[
        1
        2
        3]''')
    #test("'nn'{1 2 3 *}")
    test('nn {1 2 3}')
    #test("'name example123'{}")
    test('{ a:22 b:32}')
    test('{a:22 b:32}')
    test('''aaa{a:22
    b:32}''')
    test("{a:[11 22 33]}")
    test('hel_lo{}')
    test('hello_world{ a:22 b:"http://www.python.org"}')
#    test('''{
# a:102
#
#ppp:
#{ abb:11 ccc:a}
#}
#''')
    test(
'''{
width:100
height:200
image: { type:"svg"}
}''')
    test('foo{ a:13 b:23 c:[1 2 3]}')

    test('_{1 2 3 a:1 b:"OPT"}')
    test('nn {1 2 3 a:1 b:"OPT"}')
    test('''
    [
        [1 2 3 -7 2.5 3.0]
        [5 6 7 -7 2.5 3.0]
    ]''')
    test('''
    dataset {
        name:"archive_pogoda"
        fields: [id date time T R24 W]
        types: [int date time float float ["W" "E"]]

        [1232 2009-01-12 12:00 -7 2.5 "W"]
        [1234 2009-01-12 18:00 -4 3.5 "E"]
    }
    ''')
    test('{win: ["Windows NT" "Windows XP"] linux: ["ALT Linux" "RedHat"] mac:"OS X"}')
    test('''ABC {
        CDE { b:4 c:4}
        CDE { b:3 c:6}
    }''')
    test('''
    type {
        name:"mytype"
        attribute { name:"x" type:"int" required:true }
        element { name:"folder" multiple:"true" }
    }''')
    test('''
    html{
        h1{"Page title"}
        table{
            width:100
            tr{
                td{"cell 1 1"}
                td{"cell 1 2" "cell 1 2"}
                td{"cell 1 3"}
            }
            tr{
                td{"cell 2 1"}
                td{colspan:2 "cell 2 2"}
            }
        }
    }''')
#     test('''[
#     S{ &id123 1 2 3}
#     U{ *id123 }
#     ]
#     ''')
#     test('''[
#     S{ &id123 1 2 3}
#     U{ aaa: *id123 *id123 }
#     ]
#     ''')
    test('''[tr{} tr{} tr{}]''')
    test('''_{name:"nemo" tr{} tr{} tr{}}''')
    test('''aaa{name:"nemo" age:32 tr{} tr{} tr{}}''')
    test('aaa{}')
    test('aaa{a:1}')
    test(task_config)
    test(json_string)
    #test_binary()

    test2()
    test_random()

if __name__ == '__main__':
    #test2()
    main()

#figure {size:[10.0 9.0] dpi:100
#    lines {
#        line {1.2 2.3 3.4 4.5 style:"" color:""}
#    }
#    polygon {background:"r" foreground:"b"
#        [1.1 2.2] [3.2 1.4] [3.2 4.5]
#    }
#}

