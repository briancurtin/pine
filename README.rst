pine
====

A benchmark utility to make requests to a REST API.

Pine makes requests to URLs a bunch of times and computes some statistics
about how those requests were responded to. This is ideally useful to run
on every change to your codebase so you can identify changes early.

Pine isn't a load testing tool. If you're trying to solve C10K, this won't
help you. Pine (currently) runs requests serially.

Usage
=====

``pine -c myconfig.yaml`` is the simplest way to begin. This will run your
configuration and output the results to stdout. If you'd like to write
the output to a file, ``-o myoutputfile.json`` will do it. If you'd like
to specify a particular run ID, other than the default of the current
timestamp, ``-i 32a63ab`` will do it. That's useful for tracking the
commit hash of what you're testing.

Run ``pine -h`` for complete details.

Configuration
=============

Pine uses YAML for configuration. See
`conf/example.yaml <https://github.com/briancurtin/pine/blob/master/conf/example.yaml>`_
for an example.

Requirements
============

Pine uses aiohttp on Python 3.7.
