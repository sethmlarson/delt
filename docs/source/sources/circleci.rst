Using Delt with CircleCI
========================

Installing Delt for CircleCI
----------------------------

Put the following code into your ``before_script`` section of your ``.travis.yml`` file
and you will automatically collect environment information with Delt.

.. code-block:: yaml
    :caption: travis.yml

    install:
      - install your dependencies...

    before_script:
      - pip install -U delt && delt

    script:
      - run your tests...

Environment Values for Travis CI
--------------------------------

.. autoclass:: delt.sources.CircleCISource
