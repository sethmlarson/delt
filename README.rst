Delt
====

Gather environment information from your CI provider and be
notified of differences across builds

Integrating Delt into your CI
-----------------------------

Integrating Delt into your builds is just one line of bash.
Here's an example using Travis

```yaml
install:
  - install your dependencies...

before_script:
  - pip install -U delt && delt

script:
  - run your tests...
```

The next time you run your CI tests you should see output like this:

```bash
bash $ pip install -U delt && delt
Collecting delt
Installing collected packages: delt
Successfully installed delt-1.0.0
Detecting project...
-> Project: delt-io/delt
Gathering environment information...
-> CI Provider: Travis
-> Project Host: GitHub
-> Operating System: Ubuntu 16.04.3
-> Language: Python 3.6.6
-> Package Manager: Aptitude
-> Package Manager: Pip
-> Library: OpenSSL
-> Environment Variables
Tagging and uploading environment...
-> Tag: `gh/delt-io/delt/1/1`
Upload of environment successful :)
```

What Information does Delt Track?
---------------------------------

- Environment variables (e.g. ``PATH``, ``LD_LIBRARY_PATH``)
- Version control information (e.g. ``git``, ``hg``)
- Operating system information (e.g. Ubuntu 16.04.3)
- System packages and versions (e.g. ``apt``, ``brew``)
- Language information, packages and versions (eg ``python``/``pip``, ``nodejs``/``npm``)
- Provider-specific information (e.g. Travis OSX image)
- Library versions (e.g. OpenSSL)

Supported Platforms
-------------------

- Travis
- CircleCI
- AppVeyor
- Semaphore

- GitHub
- GitLab

- Ubuntu/Debian
- macOS
- Windows

