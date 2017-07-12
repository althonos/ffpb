**Not smart. Not comprehensive. Not guaranteed to work.**

`ffpb` is an FFmpeg progress formatter. It will attempt to display a nice
progress bar in the output, based on the raw FFmpeg output, as well as an
adaptative ETA timer.

Usage
-----
``ffpb`` is is not even self-aware. Any argument given to the ``ffpb`` command
is transparently given to the `ffmpeg` binary on your system, without any form
of validation. So if you know how to use the FFmpeg CLI, you know how to use
``ffpb`` !


Installation
------------

Currently, this is not available on PyPI. But it can be installed from GitHub
almost as easily :

.. code:: bash

   pip install https://github.com/althonos/ffpb/archive/master.zip
