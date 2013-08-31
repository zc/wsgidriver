WSGI+Webdriver for testing Javascript (and optionally WSGI) UIs
***************************************************************

This package provides some helpers for testing Javascript (and
optionally WSGI) applications using Python, Selenium Webdriver,
Manuel, and WSGI.

The package provides the following functions:

``setUp(test, app)``
  a doctest ``setUp`` function that:

  - Sets up a webdriver, available as a ``browser`` variable.

    By default, a Chrome browser driver is used.  You can override this
    in two ways:

    1. Define a driver in a ``SELENIUM_DRIVER`` environment variable,
       or

    2. In your test script, call the function ``get_factory_argument``
       to parse arguments for a ``-b`` option, typically before
       calling whatever logic normally parses arguments.

       The value of this option is a driver definition.

       The function definition:

       ``get_factory_argument(argv=sys.argv, option='-b')``
           Parse arguments for a browser definition.

    A driver definition can be one of the driver names, ``chrome``
    ``firefox``, ``ie``, ``opera``, or ``phantomjs``.  It can also be
    a remote driver specification.  A remote driver specification is
    of the form::

      browserName,version,platform,command_executor

    For example:

      internet explorer,10,Windows 8

    Items on the right can be omitted.  In the example above, we've
    left off the command executor.  If the command executor isn't
    provided as part of the option, it must be provided via the
    ``SELENIUM_REMOTE_COMMAND_EXECUTOR`` environment variable.

    Note that to use firefox as a remote browser without specifying
    anything else, you'll need to supply a trailing comma to prevent
    it from being treated as a name.

  - Sets up a server to serve a WSGI application.

  - Sets up 2 flavors of Javascript doctest examples:

    ``js>`` examples
        for evaluating Javascript expressions in the browser.

        IMPORTANT NOTE
          This should only be used with expressions.  Using with
          multiple statements is likely to produce errors or strange
          results. This works by simply taking the source provides,
          jamming a ``return`` on the front of it and calling the
          Webdriver ``execute_script`` method.

    ``js!`` examples
        for executing Javascript code in the browser without returning
        anything.  This works find with blocks of code.  The source
        given is passed to the Webdriver ``execute_script`` method.

        IMPORTANT NOTE
          Functions defined in the source using ``function`` statements
          aren't in the Javascript global scope.  To define global
          functions, use something like::

            global_name = function () {...}

    You can also execute Javascript code from Python examples using
    the Webdriver (``browser``) ``execute_script`` method.  When
    invoking Javascript this way, be aware of the following oddities:

    - Functions defined via ``function`` statements can be used within
      the block of code, but aren't global.  To define a global
      function, assign an anonymous function to a global variable.

    - No value is returned unless the block of code includes a return
      statement.

  - Includes the ``wait`` function ``from zope.testing.wait`` that
    waits for a condition.

  The function takes an additional argument (after the test argument),
  named ``app`` that provides a WSGI application object.

``start_server(app, port=0, daemon=True)``
  A function that can be used to run the test server without running tests.

  Arguments:

  ``app``
     A WSGI application object

  ``port``
     The port to listen on. If 0, the default, then the port is
     allocated dynamically and returned.

  ``daemon``
     The daemon mode.  This can be ``True``, ``False``, or ``None``.

     If ``None``, then the server is run in the foreground and blocks
     the caller.

     If ``True`` or ``False``, the server is run in a thread, whose
     daemon mode is set to the value of this parameter.


``html(css=(), scripts=(), title="test", body="<body></body>")``
   Return an HTML page with CSS links, script tags, and the given
   title and body tags.

   This is handy when you want a mostly empty HTML page that loads
   Javascript to be tested.

   ``css``
     An iterable of CSS URLs.

   ``scripts``
     An iterable of script definitions.

     Each definition is one of:

     - script URL

     - script tag (starting wth '<')

     - script Javascript source (containing at least one newline
       character)

   ``title``
      The contents of the page title

   ``body``
      The body of the document.

``manuels(optionflags=0, checker=None)``
  Return a ``manuel`` parser for Python, Javascript and capture.

``TestSuite(*tests, **options)``
  A function that takes one or more doctest/manuel file names
  and Test flags, such as ``setUp``, ``tearDown``, ``optionflags``,
  and ``checker``, and returns a doctest test suite.

  You can pass an ``app`` keyword argument, rather than passing
  ``setUp`` and ``tearDown``.

See the example test included with the package.

Changes
*******

0.1.0 (2013-08-31)
==================

Initial release
