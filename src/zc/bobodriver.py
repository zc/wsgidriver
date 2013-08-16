import bobo
import boboserver
import doctest
import manuel.capture
import manuel.doctest
import os
import re
import selenium.webdriver
import sys
import threading
import time
import wsgiref.simple_server
import zc.customdoctests.js
import zope.testing.setupstack
import zope.testing.wait

here = os.path.dirname(__file__)

def setUp(test, resources):
    if not isinstance(resources, basestring):
        resources = '\n'.join(_resource(r) for r in resources)
    browser = selenium.webdriver.Chrome()
    zope.testing.setupstack.register(test, browser.quit)
    port = start_bobo_server(resources)
    server = 'http://localhost:%s/' % port
    zope.testing.setupstack.register(
        test, lambda : browser.get(server + 'stop'))

    test.globs.update(
        port = port,
        server = server,
        browser = browser
        )
    test.globs['JS'] = browser.execute_script
    test.globs['wait'] = zope.testing.wait.wait


tearDown = zope.testing.setupstack.tearDown

class RequestHandler(wsgiref.simple_server.WSGIRequestHandler):

    def log_request(self, *args):
        pass

def start_bobo_server(resources, port=0, daemon=True):
    if not isinstance(resources, basestring):
        resources = '\n'.join(_resource(r) for r in resources)
    app = bobo.Application(bobo_resources=resources)
    server = wsgiref.simple_server.make_server('', port, app,
        handler_class=RequestHandler)

    @bobo.query("/stop")
    def stop():
        thread = threading.Thread(target=server.shutdown)
        thread.setDaemon(True)
        thread.start()
        return ''

    app.handlers.append(stop.bobo_response)

    if daemon is None:
        import logging
        logging.basicConfig()
        server.serve_forever()
    else:
        thread = threading.Thread(target=server.serve_forever)
        thread.setDaemon(daemon)
        thread.start()

    return server.server_port

def _resource(r):
    if '=' in r:
        route, path = r.split('=')
        if not os.path.isabs(path):
            path = os.path.join(
                os.path.dirname(sys._getframe(3).f_globals['__file__']),
                path,
                )
            return 'boboserver:static(%r, %r)' % (route, path)
    else:
        return r

def html(css=(), scripts=(), title="test", body="<body></body>"):
    return blank_html_template % dict(
        title=title,
        body=body,
        links = ''.join(link_template % link for link in css),
        scripts = ''.join(
            (script if script.startswith('<')
             else (script_template % script if '\n' in script
                   else script_src_template % script)
            ) for script in scripts),
        )

blank_html_template = """
<!doctype html>
<html><head>
  <title>%(title)s</title>
%(links)s
%(scripts)s
</head>%(body)s</html>
"""

link_template = """
  <link
     rel="stylesheet" type="text/css"
     href="%s"
     >
"""

script_src_template = """
  <script
    src="%s"
    ></script>
"""

script_template = """
  <script type="text/javascript">
    %s
  </script>
"""

def manuels(optionflags):
    return (
        manuel.doctest.Manuel(parser=zc.customdoctests.js.parser,
                              optionflags=optionflags) +
        manuel.doctest.Manuel(parser=zc.customdoctests.js.eq_parser,
                              optionflags=optionflags) +
        manuel.doctest.Manuel(optionflags=optionflags) +
        manuel.capture.Manuel()
        )
