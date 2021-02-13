``ffpb`` |stars|
================

.. |stars| image:: https://img.shields.io/github/stars/althonos/ffpb.svg?style=social&maxAge=3600&label=Star
   :target: https://github.com/althonos/ffpb/stargazers

**Not smart. Not comprehensive. Not guaranteed to work.**

|Source| |PyPI| |AppVeyor| |Format| |License| |Changelog| |Downloads|

.. |PyPI| image:: https://img.shields.io/pypi/v/ffpb.svg?style=flat-square&maxAge=300
   :target: https://pypi.python.org/pypi/ffpb

.. |AppVeyor| image:: https://img.shields.io/appveyor/build/althonos/ffpb.svg?style=flat-square&maxAge=3600
   :target: https://ci.appveyor.com/project/althonos/ffpb

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

.. |Downloads| image:: https://img.shields.io/badge/dynamic/json?style=flat-square&color=303f9f&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fffpb
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

Using as a library
^^^^^^^^^^^^^^^^^^

`ffpb` can be used as a library: use the ``ffpb.main`` function:

.. code:: python

    ffpb.main(argv=None, stream=sys.stderr, encoding=None, tqdm=tqdm):


argv
    The arguments to pass to ``ffmpeg``, as an argument list.
stream
    The stream to which to write the progress bar and the output messages.
encoding
    The encoding of the terminal, used to decode the ``ffmpeg`` output.
    Defaults to ``locale.getpreferredencoding()``, or *UTF-8* is locales are
    not available.
tqdm
    The progress bar factory to use. A subclass of
    `tqdm.tqdm <https://tqdm.github.io/docs/tqdm/#tqdm-objects>`_ is expected.
    Check `althonos/ffpb#19 <https://github.com/althonos/ffpb/issues/19>`_ to
    see how you can use this to wrap ``ffpb`` in your own UI.

Installation
------------

Install from PyPI:

.. code:: console

    $ pip install --user ffpb


Alternatively, download a development version from the GitHub ``master`` branch:

.. code:: console

   $ pip install https://github.com/althonos/ffpb/archive/master.zip

Or if you use an Arch-based distro, `download from the AUR`__

.. __: https://aur.archlinux.org/packages/ffpb/
