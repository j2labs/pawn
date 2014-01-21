.. _install:

Install Guide
=============

::

  $ pip install pawn

Python 2.7 is supported with 3.x in mind. 


.. _install_dependencies:

Dependencies
------------

Pawn depends on install gevent.

We also like to use `ujson <https://pypi.python.org/pypi/ujson>`_ or `msgpack
<https://pypi.python.org/pypi/msgpack-python/>`_, depending on what we're
building.


.. _install_from_github:

Installing from Github
----------------------

The canonical repository for Pawn is `on Github
<https://github.com/j2labs/pawn>`_.

::

  $ git clone https://github.com/j2labs/pawn.git

New releases are first released as a development branch for feedback and then
they are pushed into master around the same time the update is pushed to `Pypi
<https://pypi.python.org/pypi>`_.  The best reason to install from source is to
help us develop Pawn.  See the :doc:`development`.
