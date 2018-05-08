pine
====

A benchmark utility to make requests to a REST API.

Installation
************

On Python 3.6, ``pip install pine`` will do it.

Under normal circumstances you would just do ``pip install pine``.

On Python 3.7, there is an additional step required before running the
same command. Until PyYAML supports Python 3.7 in a released version,
you will need to install PyYAML from GitHub::

    pip install git+https://github.com/yaml/pyyaml.git
    pip install pine

This will install the ``pine`` script for you to use. If you're installing
this inside a virtualenv, it'll be in the ``/bin`` folder of that virtualenv.
If you're installing this system-wide, that probably depends on the system,
but on Ubuntu this ends up in ``/usr/local/bin/pine``. In any case, you should
end up with a ``pine`` executable which you can run.

Usage
*****

``pine`` takes three named arguments, one of which is required. It also
takes the names of specific tests to run. See `names`_ for details.

-c
^^

``pine`` must receive the path to a configuration file in the ``-c`` (or
``--config``) argument. This is a YAML file which outlines the tests
for ``pine`` to run. See `Configuration`_ for details on this file.

``pine -c tests.yaml`` will make pine run all of the tests in tests.yaml.

-o
^^

By default, ``pine`` writes the test results in JSON format to standard
output, aka stdout, aka it prints them to the screen. If you'd like these
results written to a file, the ``-o`` (or ``--output``) argument takes a
file name to create. You can also specify a directory for the output file
to be written to and ``pine`` will generate a file in that directory using
the run id it knows about from `-i`_. Note that in either case it will
overwrite any prior contents of that file.

``pine -c tests.yaml -o results.json`` will make pine run all of the tests
in tests.yaml and then write them to results.json.

-i
^^

``pine`` identifies each run by writing some identifier in the results output.
By default, it writes a timestamp in the form ``%Y%m%d%H%M%S%f``, which comes
out like ``20180308094325628253``. However, you may wish to identify test
runs with a value that makes sense with what you're testing.

For example, if you're running pine as part of a continuous delivery pipeline
you will be running tests against a certain commit hash, which is a good
identifier for your test results.

``pine -c tests.yaml -o results.json -i 47d8b22`` will make pine run all of
the tests in tests.yaml and then write them to results.json with the id
47d8b22.

names
^^^^^

``pine`` supports running only certain tests of a configuration if you
specify the names of tests on the command line. For example, running
``pine -c tests.yaml create_thing delete_thing`` will run only the
create_thing and delete_thing tests from within tests.yaml.

-h
^^

Running ``pine -h`` or ``pine --help`` will display information about pine's
argument, similar to what is outlined above.

Configuration
*************

``pine`` uses `YAML <http://yaml.org/>`_ for configuration. It supports a
``default`` section for some configuration-wide values, and then arbitrarily
named sections for individual tests. For example::

    details:
        name: "my api tests"
        version: "1.0"
    defaults:
        root: "https://app.com/api"
        warmup: 1
        iterations: 20
    get_all_things:
        description: "Get all of the things"
        url: "/thing"
        method: "get"
        headers: {"X-Auth-Token": "{X_AUTH_TOKEN}"}

details
^^^^^^^

The following details are used when creating the test's results, used for
identifying this run's results as compared to others.

name
++++

The name of this suite of tests, which shows up in the results output.

The default value is the name of your configuration file, without any path
or extension. For example, if you passed ``-c /etc/pine/things.yaml`` on
the command line and did not specify ``name`` in the ``details`` section,
``name`` would become ``things``.

version
+++++++

When looking back on test results, it can be useful to know what version
of the test you were actually looking at. By versioning your config file
you can identify when things changed, perhaps helping you figure out why
results may look different independent of actual performance changes.

defaults
^^^^^^^^

The following defaults can be entered in order to apply to the tests that
follow.

root
++++

Each test must specify a ``url``, and by entering a ``root`` default value
it allows you to specify shorter URLs later. If you specify a default
``root: https://website.com``, you can later specify ``url: /resource``
instead of needing to specify the full ``url: https://website.com/resource``.

Both ``root`` and ``url`` support templated values which will be
formatted using environment variables. For example, if you would like
to use the ``DEPLOYMENT`` environment variable to fill your ``root``,
``root: https://{DEPLOYMENT}.website.com/api`` will allow you to do this.

warmup
++++++

When running benchmarks, it may be beneficial to make some requests before
counting the results, such as to eliminiate requests to a cold cache that
may skew results as the cache begins to help. For example, if you set
``warmup: 3``, pine will make three requests to the test's ``url`` before
it starts counting the response times.

iterations
++++++++++

This specifies the amount of requests to make to the test's ``url``. All of
these requests are counted in the resulting statistics, so if you set
``warmup: 1`` and ``iterations: 10`` your results will be calculated for the
ten runs after the warmup, not the eleven total requests that were made.


tests
^^^^^

Each configuration file contains one or more named tests. In the above
example, ``get_all_things`` is the name of one test. Each test supports
the following options.

description
+++++++++++

This string describes what the test does. This is for your convenience
and is output in the results.

url
+++

This is the URL the request will be made to. If you do not have a ``root``
specified in the ``default`` section, this must be a fully formed URL. If
you do have a ``root`` specified, this can be a fragment of the URL that will
be joined with that ``root`` as the above example does.

As with ``root``, ``url`` supports templated values which will be formatted
using environment variables. For example, if you would like
to use the ``VERSION`` environment variable to fill your ``url``,
``url: /api/{VERSION}/status`` will allow you to do this.

method
++++++

This is the HTTP method to use to call this URL, and should be lowercase.
Acceptable values include ``get``, ``post``, ``put``, ``delete``, ``head``,
``options``, and ``patch``.

headers
+++++++

This is an optional dictionary of header keys and values to send in
the request. Of special note here is that the values support replacement
with environment variables, such as to use a password or authentication
secret.

If you would like the environment variable ``PASSWORD`` to be included
in a header value, specify that value as ``{PASSWORD}`` and it will be
replaced.

json
++++

This is an optional dictionary of JSON to send in the request body.

Output
******

``pine`` writes its output in JSON format with three top-level keys:
``results``, ``name``, and ``id``. The ``name`` is gathered from the
``details`` section of your configuration file, or lacking that setting,
it is derived from the argument passed in ``-c`` for the configuration
file name. The ``id`` is what was specified in the ``-i`` argument to
``pine`` (or the default timestamp) and identifies this particular run
of tests. ``results`` contains a list of dictionaries with details
on each individual test, as follows.

::

    {"results": [
        {"times": [1.580882219500005, 1.8884545513215, 1.52546876846],
         "timeouts": 0, "failures": [], "name": "get_all_things",
         "description": "Get all of the things",
         "mean": 1.668359371049998,
         "median": 1.580882219500005,
         "stdev": 0.0969358463985873},
     ],
     "name": "some_benchmark_tests",
     "version": "1.0",
     "id": "7155eb"}

.. note:: ``pine`` does not determine success or failure of any test,
           though it does separate timeouts and responses other than
           ``200 OK`` and only calculates statistics on responses that
           had a ``200 OK`` status.

           For example, if 10/20 responses were ``500 INTERNAL SERVER ERROR``,
           you would still receive statistics about the 10 responses that
           succeeded. How you use that information is up to you.

times
^^^^^

This is a list of the response times.

timeouts
^^^^^^^^

This is the count of requests which timed out.

failures
^^^^^^^^

This is a list of HTTP status codes that came back from requests that were
not a ``200 OK``.

name
^^^^

This is the name of the individual test.

description
^^^^^^^^^^^

This is the description of the test.

mean
^^^^

This is the mean of response times for all successful responses.

median
^^^^^^

This is the median of response times for all successful responses.

stdev
^^^^^

This is the standard deviation across response times for all successful
responses.
