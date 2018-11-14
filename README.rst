Delt
====

Gather environment information from your CI provider and be
notified of differences across builds

Integrating Delt into your CI
-----------------------------

Integrating Delt into your builds is just one line of bash.
Here's an example using Travis:

.. code-block:: yaml

    install:
      - install your dependencies...

    before_script:
      - pip install -U delt && delt

    script:
      - run your tests...

What Information does Delt Track?
---------------------------------

- Service-specific information (e.g. Travis OSX image)
- Operating system information (e.g. Ubuntu 16.04.3)
- Language information, packages and versions (eg ``python``/``pip``, ``nodejs``/``npm``)
- System packages and versions (e.g. ``apt``, ``brew``)
- Environment variables (e.g. ``PATH``, ``LD_LIBRARY_PATH``)
