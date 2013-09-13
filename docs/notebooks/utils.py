from IPython.display import HTML, display, display_html
from axon import loads, dumps

def test_cv(text):
    vals = loads(text)
    text1 = dumps(vals)
    text2 = dumps(vals, pretty=1)
    text3 = dumps(vals, pretty=2)
    template = '''\
    <table>
    <tr><td colspan=2 style="background-color:#d0d0d0;"><b>Compact form</b></td></tr>
    <tr><td colspan=2><pre>%s</pre></td></tr>
    <tr><td style="background-color:#d0d0d0;"><b>Expression formatted</b></td>
        <td style="background-color:#d0d0d0;"><b>Statement indented<b></td></tr>
    <tr><td><pre>%s</pre></td><td><pre>%s</pre></td></tr>
    </table>
    '''
    return HTML(template % (text1, text2, text3))
    
def test_av(text):
    vals = loads(text)
    text1 = dumps(vals)
    text2 = dumps(vals, pretty=1)
    template = '''\
    <table>
    <tr><tdstyle="background-color:#d0d0d0;"><b>Compact form</b></td></tr>
    <tr><td><pre>%s</pre></td></tr>
    <tr><td style="background-color:#d0d0d0;"><b>Expression formatted</b></td></tr>
    <tr><td><pre>%s</pre></td></tr>
    </table>
    '''
    return HTML(template % (text1, text2))
