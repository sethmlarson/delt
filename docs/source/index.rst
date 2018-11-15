Delt Documentation
==================

Delt is designed to gather information about your Continuous Integration provider's environment
and archive and compare that information to following runs to better understand changes
to your Continuous Integration environment.

This allows for faster debugging and finer control of your Continuous Integration environment.

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  getting-started
  sources/appveyor
  sources/azure-pipelines
  sources/circleci
  sources/gitlab-runner
  sources/semaphore
  sources/travis

Features
--------

* Gather information from the system, package managers, languages,
  libraries, services, and environment variables to build a coherent
  picture of the build environment.

* Tag, upload and archive each build environment for future comparisons and historical record.

* Comparisons between build environments happen sequentially and important changes
  are made clear within Pull Requests and the web interface for ``delt.io``.

* Optionally set commit statuses when certain environment values change requiring commit privileges to approve.

* Provide a seamless API into build environment and result information.

* Does not require code viewing permissions to integrate into a repository.

* Delt is open-source under the ``Apache-2.0`` license.
