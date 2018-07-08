#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2017 Martin Larralde (martin.larralde@ens-cachan.fr)
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

from __future__ import unicode_literals
from __future__ import print_function

import re
import chardet
import os
import sys
import collections

if sys.version_info < (3, 0):
    import Queue as queue
    input = raw_input
else:
    import queue

import sh
import progressbar


class AbsoluteTimeETA(progressbar.AbsoluteETA):

    def _calculate_eta(self, progress, data, value, elapsed):
        return elapsed + progressbar.ETA._calculate_eta(
            self, progress, data, value, elapsed)


class ProgressNotifier(collections.Callable):

    _DURATION_RX = re.compile("Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}")
    _PROGRESS_RX = re.compile("time=(\d{2}):(\d{2}):(\d{2})\.\d{2}")
    _SOURCE_RX = re.compile("from '(.*)':")

    @staticmethod
    def _seconds(hours, minutes, seconds):
        return (int(hours)*60 + int(minutes))*60 + int(seconds)

    def __init__(self):
        self.lines = []
        self.line_acc = []
        self.duration = None
        self.source = None
        self.started = False
        self.pbar = progressbar.ProgressBar(widgets=[
            lambda w, d: self.source, ' ',
            progressbar.AnimatedMarker(
                markers="—/|\\",
            ),
            progressbar.Bar(
                marker='█',
                fill='░',
                left=' ╢',
                right='╟ ',
            ),
            progressbar.Percentage(
                '%(percentage)3d% % '
            ),
            progressbar.Timer(
                format='(%(elapsed)s / '
            ),
            AbsoluteTimeETA(
                format='%(eta)s)',
                format_finished='%(elapsed)s',
                format_not_started='--:--:--'
            ),
        ])

    def newline(self):
        self.lines.append(''.join(self.line_acc))
        self.line_acc = []

    def __call__(self, char, stdin):

        if type(char) != unicode:
            encoding = chardet.detect(char)['encoding']
            char = unicode(char, encoding)

        if char not in '\r\n':
            self.line_acc.append(char)
            if self.line_acc[-6:] == list('[y/N] '):
                print(''.join(self.line_acc), end='')
                stdin.put(input()+'\n')
                self.newline()
            return

        self.newline()

        self.get_duration(self.lines[-1])
        self.get_source(self.lines[-1])
        self.get_progress(self.lines[-1])

    def get_duration(self, line):
        search = self._DURATION_RX.search(line)
        if search is not None:
            self.duration = self._seconds(*search.groups())

    def get_source(self, line):
        search = self._SOURCE_RX.search(line)
        if search is not None:
            self.source = search.group(1)

    def get_progress(self, line):
        search = self._PROGRESS_RX.search(line)
        if search is not None:
            current = self._seconds(*search.groups())

            if not self.started:
                self.pbar.start(max_value=self.duration)
                self.started = True

            self.pbar.update(current)


def main(argv=None):
    argv = argv or sys.argv[1:]

    if {'-h', '-help', '--help'}.intersection(argv):
        sh.ffmpeg(help=True, _fg=True)
        return 0

    notifier = ProgressNotifier()

    try:

        sh.ffmpeg(
            sys.argv[1:],
            _in=queue.Queue(),
            _err=notifier,
            _out_bufsize=0,
            _err_bufsize=0,
            #_in_bufsize=0,
            _no_out=True,
            _no_pipe=True,
            _tty_in=True,
            #_fg=True,
            #_bg=True,
        )

    except sh.ErrorReturnCode as err:
        print(notifier.lines[-1])
        return err.exit_code

    else:
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
