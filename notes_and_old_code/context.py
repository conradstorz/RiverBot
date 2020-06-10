import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import NWS_WebScrape


"""https://kenreitz.org/essays/repository-structure-and-python

...
Obviously, these test modules must import your packaged module to test it. 
You can do this a few ways:

    Expect the package to be installed in site-packages.
    or
    Use a simple (but explicit) path modification to resolve the package properly.

I highly recommend the latter. 
Requiring a developer to run setup.py develop to 
test an actively changing codebase also requires 
them to have an isolated environment setup for each instance of the codebase.

To give the individual tests import context, create a tests/context.py file:

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import sample

Then, within the individual test modules, import the module like so:

                                                                from .context import sample

This will always work as expected, regardless of installation method.

Some people will assert that you should distribute 
your tests within your module itself -- I disagree. 
It often increases complexity for your users; 
many test suites often require additional dependencies and runtime contexts.
"""