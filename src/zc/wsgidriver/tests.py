##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import bobo
import zc.wsgidriver

@bobo.query("/")
def blank(title='test title', content='test content'):
    return zc.wsgidriver.html(
        scripts = [
            """
            wsgidriver_x = 1;
            """,
            "/test.js",
            """<script type="text/javascript">
            wsgidriver_y = 2;
            </script>
            """
            ],
        css = ['/test.css'],
        title = title,
        body="<body>%s</body>" % content
        )

@bobo.query("/test.js")
def js():
    return 'wsgidriver_z = 3'

@bobo.query("/test.css", content_type="text/css")
def css():
    return 'body {color: #999; }'

app = bobo.Application(bobo_resources=__name__)

def test_suite():
    return zc.wsgidriver.TestSuite('example.rst', app=app)

