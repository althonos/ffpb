#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2017-2018 Martin Larralde (martin.larralde@ens-cachan.fr)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

"""A progress bar for `ffmpeg` using `tqdm`.
"""

from __future__ import unicode_literals
from __future__ import print_function

import re
import os
import signal
import sys

if sys.version_info < (3, 0):
    import Queue as queue
    input = raw_input
else:
    import queue
    unicode = str

import chardet
import sh
import tqdm


class ProgressNotifier(object):

    _DURATION_RX = re.compile("Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}")
    _PROGRESS_RX = re.compile("time=(\d{2}):(\d{2}):(\d{2})\.\d{2}")
    _SOURCE_RX = re.compile("from '(.*)':")
    _FPS_RX = re.compile("(\d{2}\.\d{2}|\d{2}) fps")

    @staticmethod
    def _seconds(hours, minutes, seconds):
        return (int(hours) * 60 + int(minutes)) * 60 + int(seconds)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.pbar is not None:
            self.pbar.close()

    def __init__(self, file=None):
        self.lines = []
        self.line_acc = []
        self.duration = None
        self.source = None
        self.started = False
        self.pbar = None
        self.fps = None
        self.file = file or sys.stderr

    def __call__(self, char, stdin):

        if not isinstance(char, unicode):
            encoding = chardet.detect(char)["encoding"]
            char = unicode(char, encoding)

        if char in "\r\n":
            line = self.newline()
            if self.duration is None:
                self.duration = self.get_duration(line)
            if self.source is None:
                self.source = self.get_source(line)
            if self.fps is None:
                self.fps = self.get_fps(line)
            self.progress(line)
        else:
            self.line_acc.append(char)
            if self.line_acc[-6:] == list("[y/N] "):
                print("".join(self.line_acc), end="")
                stdin.put(input() + "\n")
                self.newline()

    def newline(self):
        line = "".join(self.line_acc)
        self.lines.append(line)
        self.line_acc = []
        return line

    def get_fps(self, line):
        search = self._FPS_RX.search(line)
        if search is not None:
            return round(float(search.group(1)))

    def get_duration(self, line):
        search = self._DURATION_RX.search(line)
        if search is not None:
            return self._seconds(*search.groups())
        return None

    def get_source(self, line):
        search = self._SOURCE_RX.search(line)
        if search is not None:
            return os.path.basename(search.group(1))
        return None

    def progress(self, line):
        search = self._PROGRESS_RX.search(line)
        if search is not None:

            total = self.duration
            current = self._seconds(*search.groups())
            unit = " seconds"

            if self.fps is not None:
                unit = " frames"
                current *= self.fps
                total *= self.fps

            if self.pbar is None:
                self.pbar = tqdm.tqdm(
                    desc=self.source,
                    file=self.file,
                    total=total,
                    dynamic_ncols=True,
                    unit=unit,
                    ncols=0,
                )

            self.pbar.update(current - self.pbar.n)


def main(argv=None, stream=sys.stderr):
    argv = argv or sys.argv[1:]

    if {"-h", "-help", "--help"}.intersection(argv):
        sh.ffmpeg(help=True, _fg=True)
        return 0

    try:

        with ProgressNotifier(file=stream) as notifier:

            sh.ffmpeg(
                argv,
                _in=queue.Queue(),
                _err=notifier,
                _out_bufsize=0,
                _err_bufsize=0,
                # _in_bufsize=0,
                _no_out=True,
                _no_pipe=True,
                _tty_in=True,
                # _fg=True,
                # _bg=True,
            )

    except sh.ErrorReturnCode as err:
        print(notifier.lines[-1], file=stream)
        return err.exit_code

    except KeyboardInterrupt:
        print("Exiting.", file=stream)
        return signal.SIGINT + 128  # POSIX standard

    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
