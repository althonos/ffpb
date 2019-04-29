``ffpb``
========

**Not smart. Not comprehensive. Not guaranteed to work.**

|Source| |PyPI| |Travis| |Format| |License| |Changelog| |Downloads|

.. |PyPI| image:: https://img.shields.io/pypi/v/ffpb.svg?style=flat-square&maxAge=300
   :target: https://pypi.python.org/pypi/ffpb

.. |Travis| image:: https://img.shields.io/travis/althonos/ffpb.svg?style=flat-square&maxAge=3600
   :target: https://travis-ci.org/althonos/ffpb/branches

.. |Format| image:: https://img.shields.io/pypi/format/ffpb.svg?style=flat-square&maxAge=300
   :target: https://pypi.python.org/pypi/ffpb

.. |Versions| image:: https://img.shields.io/pypi/pyversions/ffpb.svg?style=flat-square&maxAge=300
   :target: https://travis-ci.org/althonos/ffpb/

.. |License| image:: https://img.shields.io/pypi/l/ffpb.svg?style=flat-square&maxAge=300
   :target: https://choosealicense.com/licenses/mit/

.. |Source| image:: https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=3600&style=flat-square
   :target: https://github.com/althonos/ffpb/

.. |Changelog| image:: https://img.shields.io/badge/keep%20a-changelog-8A0707.svg?maxAge=2678400&style=flat-square
   :target: http://keepachangelog.com/

.. |Downloads| image:: https://img.shields.io/pypi/dw/ffpb.svg?color=darkblue&style=flat-square&maxAge=3600
   :target: https://pepy.tech/project/ffpb

``ffpb`` is an FFmpeg progress formatter. It will attempt to display a nice
progress bar in the output, based on the raw ``ffmpeg`` output, as well as an
adaptative ETA timer.


Showcase
--------

.. image:: https://github.com/althonos/ffpb/raw/master/static/showcase.v1.gif

(*yes, my laptop can't encode shit*)


Usage
-----

``ffpb`` is is not even self-aware. Any argument given to the ``ffpb`` command
is transparently given to the `ffmpeg` binary on your system, without any form
of validation. So if you know how to use the FFmpeg CLI, you know how to use
``ffpb`` !


Installation
------------

Install from PyPI:

.. code:: console

    $ pip install --user ffpb


Alternatively, download a development version from the GitHub ``master`` branch:

.. code:: console

   $ pip install https://github.com/althonos/ffpb/archive/master.zip
