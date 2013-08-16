Bobo+Webdriver for testing Javascript (and optionally bobo) UIs
***************************************************************

This package provides some helpers for testing Javascript applications
using Python, Selenium Webdriver, Manuel, and bobo.

- ``doctest`` setUp function that:

  - Sets up a webdriver, available as a ``browser`` variable.

    Currently, only Chrome is supported.  Support for other drivers
    coming soon.

  - Sets up a bobo server, to serve static files and application or
    testing resources.  By default, this runs on a dynamically
    assigned port.  The address is available in the variable ``server``
  - Sets up a ``JS`` function for evaluating Javascript code on the
    browser.
  - Includes the ``wait`` function ``from zope.testing.wait`` that
    waits for a condition.

  The function takes a bobo resources definition as a string, or as a
  tuble of strings.  In the later case, the values in the tuple are
  either module names, or static file definitions of the form
  ``"route=path"``.  If the path is relative, then it's determined
  from the location of the calling function.

- A ``start_bobo_server`` function that can be used to run the test
  server without running tests.

  start_bobo_server(resources, port=0, daemon=True)

    Start a bobo server.

    Arguments:

    resources
       Resource definitions as a string or tuple as described above.

    port
       The port to listen on. If 0, the default, then the port so
       allocated dynamically and returned.

    daemon
       The daemon mode.  This can be ``True``, ``False``, or ``None``.

       If ``None``, then the server is run in the foureground and blocks
       the caller.

       If ``True`` or ``False``, the server is run in a thread, who's
       deamon mode is set to the value of this parameter.

- A ``html`` method that returns a mostly empty page to be
  painted by Javascript:

  html(css=(), scripts=(), title="test", body="<body></body>")
     Return an HTML page with CSS links, script tags, and the given
     title and body tags.

     css
       An iterable of CSS URLs.

     scripts
       An iterable of script definitions.

       Each definition is one of:

       - script URL

       - script tag (starting wth '<')

       - script Javascript source (containing at least one newline
         character)

     title
        The contents of the page title

     body
        The body of teh document.

- A ``manuels`` function that returns a ``manuel`` parser, created by
  combining Python and Javascript syntax doctest parsers and a capture
  parser.

  manuels(optionflags)
    Return a ``manuel`` parser for Python, Javascript and capture.


Changes
*******

0.1.0 (yyyy-mm-dd)
==================

Initial release
