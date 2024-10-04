============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/django-functest/django-functest/issues.

If you are reporting a bug, please include:

* Your Django version.
* Browser name and version if applicable.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

django-functest could always use more documentation, whether as part of the
official django-functest docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/django-functest/django-functest/issues

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up ``django-functest`` for local
development.

1. Fork the ``django-functest`` repo on GitHub.
2. Clone your fork locally::

     $ git clone git@github.com:your_name_here/django-functest.git

3. Create a virtualenv for the project, and then install django-functest into it
   locally for development::

     $ cd django-functest/
     $ pip install -e .

   You also need to install testing and development tools::

     $ pip install -r requirements-dev.txt

4. Create a branch for local development::

     $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests::

     $ pytest

   See ``pytest --help`` for more options on test selection

   You can also use `pre-commit <https://pre-commit.com/>`_ to run all of
   the linters automatically when you commit::

     $ pre-commit install

   It can help to test other Django/Python versions with tox::

     $ tox

   To run the full test suite, you will need to install:

   * Firefox and `geckodriver <https://github.com/mozilla/geckodriver>`_.

   * `chromedriver <https://googlechromelabs.github.io/chrome-for-testing/>`_ (and `older releases <https://developer.chrome.com/docs/chromedriver/downloads>`_)

6. Commit your changes and push your branch to GitHub::

     $ git add .
     $ git commit -m "Your detailed description of your changes."
     $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.


Conduct
-------

Contributors of any kind are expected to act with politeness to all other
contributors, in pull requests, issue trackers etc., and harassing behaviour
will not be tolerated.
