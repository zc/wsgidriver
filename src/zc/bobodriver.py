import bobo
import boboserver
import doctest
import manuel.capture
import manuel.doctest
import os
import re
import selenium.webdriver
import socket
import sys
import threading
import time
import wsgiref.simple_server
import zc.customdoctests.js
import zope.testing.setupstack
import zope.testing.wait

here = os.path.dirname(__file__)

remote_name = 'bobodriver'
driver_factory = None
basic_factories = dict(
    chrome = selenium.webdriver.Chrome,
    ie = selenium.webdriver.Ie,
    opera = selenium.webdriver.Opera,
    phantomjs = selenium.webdriver.PhantomJS,
    firefox = selenium.webdriver.Firefox,
    )

def remote(platform, browserName, version, executor):
    def factory():
        return selenium.webdriver.Remote(
            desired_capabilities = dict(
                browserName=browserName,
                platform=platform,
                version=version,
                javascriptEnabled=True,
                name=remote_name,
                ),
            command_executor=executor,
            )
    return factory

def driver_factory_from_string(browser):
    driver_factory = basic_factories.get(browser)
    if driver_factory is None:
        browser = browser.split(',')
        browserName = browser.pop(0)
        version = ''
        platform = 'ANY'
        executor = None
        if browser:
            version = browser.pop(0)
            if browser:
                platform = browser.pop()
                if browser:
                    [executor] = browser
        if not executor:
            executor = os.environ['SELENIUM_REMOTE_COMMAND_EXECUTOR']

        driver_factory = remote(
            platform, browserName, version, executor)

def get_factory_argument(argv=sys.argv, option='-b'):
    global driver_factory
    i = 1
    while i < len(argv):
        if argv[i].startswith(option):
            browser = argv.pop(i)[len(option):]
            if not browser:
                browser = argv.pop(i)
            driver_factory_from_string(browser)
            break
        i += 1

def setUp(test, resources):
    if not isinstance(resources, basestring):
        resources = '\n'.join(_resource(r) for r in resources)

    global driver_factory
    if driver_factory is None:
        browser = os.environ.get("SELENIUM_DRIVER")
        if browser:
            driver_factory_from_string(browser)
        else:
            driver_factory = selenium.webdriver.Chrome

    browser = driver_factory()

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

    if port == 0:
        for port in range(8000, 9000):
            # We don't use ephemeral ports because windows clients, at
            # least in sauce labs, can't seem to use them, so we have
            # to do this the hard way.
            try:
                server = wsgiref.simple_server.make_server(
                    '', port, app, handler_class=RequestHandler)
            except socket.error:
                if port == 8999:
                    raise # dang, ran out of ports
            else:
                break

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

    return port

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
