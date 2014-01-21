.. _development:

Developer's Guide
=================

The primary goal is to make it easy to build servers.  Easy enough that it
becomes easy to experiment with ideas and prototype things.  Ideas come in all
kinds of shapes, and thus you can build all kinds of pawns.

With that goal in mind, there is a clean canvas waiting for brush strokes.


.. _development_contributors:

List of Contributors
--------------------

::

  $ cd pawn
  $ git shortlog -sn

James Dennis


.. _development_get_the_code:

Get the code
------------

Please see the :ref:`install_from_github` section of the :doc:`install`
page for details on how to obtain the pawn source code.


.. _development_tests:

Tests
-----

Using py.test

::

  $ py.test tests/


.. _writing_documentation:

Writing Documentation
---------------

:doc:`Documentation <index>` is essential to helping other people understand, 
learn, and use pawn.

Pawn uses the .rst (reStructuredText) format for all of our documentation. You
can read more about .rst on the `reStructuredText Primer
<http://sphinx-doc.org/rest.html>`_ page.


.. _installing_documentation:

Installing Documentation
---------------

Just as you verify your code changes in your local environment before 
committing, you also verify that your documentation builds and displays
properly in your local environment.

First, install `Sphinx <http://sphinx-doc.org/latest/install.html>`_:

::

  $ pip install sphinx

Next, run the Docs builder:

::

  $ cd docs
  $ make html

The docs will be placed in the `./_build` folder and you can view them from 
any standard web browser. (Note: the `./_build` folder is included in the 
`.gitignore` file to prevent the compiled docs from being included with your
commits).

Each time you make changes and want to see them, re-run the Docs builder and 
refresh the page.

Once the documentation is up to your standards, go ahead and commit it. As with 
code changes, please be descriptive in your documentation commit messages as it 
will help others understand the purpose of your adjustment.
