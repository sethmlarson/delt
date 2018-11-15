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

**There has to be a better way!** Integrating Delt into your builds is just one line of bash.
Here's an example using Travis:

.. code-block:: yaml

    install:
      - install your dependencies...

    before_script:
      - pip install -U delt && delt

    script:
      - run your tests...

And then navigating to ``delt.io`` for this build you'll see:

.. code-block:: json

    {
      "apt.version": "",
      "apt.packages": {
        "openssl": "1.0.2k",
        "...": "..."
      },
      "delt.version": "1.0.0",
      "env": {
        "USER": "travis",
        "HOME": "/home/travis",
        "PATH": [
          "/usr/local/bin",
          "/usr/bin",
          "/bin"
        ],
        "...": "..."
      },
      "python.version": "3.6.6",
      "python.impl": "cpython",
      "pip.version": "18.1",
      "pip.packages": {
        "pytest": "3.10.1",
        "...": "..."
      },
      "openssl.version": "1.0.2k-fips",
      "os.id": "ubuntu",
      "os.version": "14.04.5",
      "travis.allow_failure": false,
      "travis.trigger": "push",
      "travis.build_stage": null,
      "travis.secure_env_vars": false,
      "travis.os_name": "linux",
      "travis.dist": "trusty",
      "travis.sudo": false,
      "travis.infra": "ec2",
      "travis.python.version": "3.6"
    }

* Differences are determined automatically by Delt.
* Information is consistently structured and differences are highlighted.
* All historical information is in one location.
* Set once and forget about it. Updates and improvements to Delt will affect all your projects.
* All changes are stored and can be tracked regardless of build status.
* Notifies you of changes via pull request comments and commit statuses.

See our documentation on how to integrate with Project Hosts such as GitHub and GitLab and
Continuous Integration providers such as AppVeyor, Azure Pipelines, CircleCI, GitLab Runner, Semaphore, and Travis.

What Information does Delt Track?
---------------------------------

- Operating system information (e.g. Ubuntu 16.04.3)
- Service-specific information (e.g. Travis OSX image)
- System packages and versions (e.g. ``apt``, ``brew``)
- Language information, packages and versions (eg ``python``/``pip``, ``nodejs``/``npm``)
- Environment variables (e.g. ``PATH``, ``LD_LIBRARY_PATH``)
