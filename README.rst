Delt
====

Is this your current implementation of "debugging" your build environment?

.. code-block:: yaml

    before_script:
      - python --version
      - pip --version
      - pip freeze
      - apt list
      - openssl version

* Requires manual effort determine differences between builds.
* Requires parsing unstructured information in plain-text.
* Requires wading through previous builds to find historical information.
* When your Continuous Integration provider's offerings and environments change
  you need to manually update **all** your project configurations.
* Changes that don't affect the build status go unnoticed.
* No notifications of changes or commit statuses.

Example using Delt
------------------

**There has to be a better way!** Integrating Delt into your builds is just one line of bash.
Here's an example using CircleCI:

.. code-block:: yaml

    install:
      - install your dependencies...

    before_script:
      - pip install -U delt && delt store && delt upload

    script:
      - run your tests...

And then navigating to ``delt.io`` for this build you'll see:

.. code-block:: json

    {
      "apt": {
        "packages": {
          "acl": "2.2.52-2",
          "adduser": "3.113+nmu3",
          "...": "..."
        },
        "version": "1.0.9.8.4"
      },
      "build": {
        "branch": "js",
        "build_id": "circleci-40.1",
        "commit": "1bbc83d08e800b8d5eacd1e422415c1277077a26",
        "committed_at": "2019-03-20 03:20:10",
        "project_host": "github",
        "project_name": "delt",
        "project_owner": "delt-io",
        "pull_request": 32,
        "service": "circleci",
        "tag": null,
        "url": "https://circleci.com/gh/delt-io/delt/40"
      },
      "circleci": {
        "job_name": "build",
        "workflow_id": "4dec9617-3cf0-403d-b08a-fdaf85fb79aa"
      },
      "delt": {
        "version": "0.1.0"
      },
      "env": {
        "BASH_ENV": "/tmp/.bash_env-5c91b1706932e90008bd343b-0-build",
        "DEBIAN_FRONTEND": "noninteractive",
        "GPG_KEY": "0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D",
        "HOME": "/home/circleci",
        "HOSTNAME": "64c5b693690f",
        "LANG": "C.UTF-8",
        "NO_PROXY": "127.0.0.1,localhost,circleci-internal-outer-build-agent",
        "PATH": [
          "/home/circleci/repo/venv/bin",
          "/usr/local/bin",
          "/usr/local/sbin",
          "/usr/local/bin",
          "/usr/sbin",
          "/usr/bin",
          "/sbin",
          "/bin"
        ],
        "PWD": "/home/circleci/repo",
        "SHLVL": "1",
        "SSH_AUTH_SOCK": "/tmp/circleci-258802883/ssh_auth_sock",
        "_": "/home/circleci/repo/venv/bin/delt"
      },
      "git": {
        "version": "2.1.4"
      },
      "os": {
        "id": "debian",
        "version": "8"
      },
      "pip": {
        "packages": {},
        "version": "9.0.1"
      },
      "python": {
        "executable": "",
        "implementation": "cpython",
        "version": "3.6.1"
      },
      "virtualenv": {
        "path": "/home/circleci/repo/venv"
      }
    }

* Differences are determined automatically by Delt.
* Information is consistently structured and differences are highlighted.
* All historical information is in one location.
* Set once and forget about it. Updates and improvements to Delt will affect all your projects.
* All changes are stored and can be tracked regardless of build status.
* Notifies you of changes via pull request comments and commit statuses.

Viewing Diffs
-------------

Using ``delt diff [build-id2] [build-id2]`` or viewing the diffs directly on the website you
can check the differences between the two builds.

 .. code-block:: diff
 
    $ delt diff circleci-40.1 circleci-41.1
 
    67c67
    <         "version": "3.6.4"
    ---
    >         "version": "3.6.1"

See our documentation on how to integrate with Project Hosts such as GitHub and GitLab and
Continuous Integration providers such as AppVeyor, Azure Pipelines, CircleCI, GitLab Runner, Semaphore, and Travis.

What Information does Delt Track?
---------------------------------

- Operating system information (e.g. Ubuntu 16.04.3)
- Service-specific information (e.g. Travis OSX image)
- System packages and versions (e.g. ``apt``, ``brew``)
- Language information, packages and versions (eg ``python``/``pip``, ``nodejs``/``npm``)
- Environment variables (e.g. ``PATH``, ``LD_LIBRARY_PATH``)

License
-------

Apache-2.0
