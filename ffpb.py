#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import re
import sys
import queue
import collections

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
                markers="🌑🌒🌓🌔🌕🌖🌗🌘",
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

        if char not in '\r\n':
            self.line_acc.append(char)
            if self.line_acc[-6:] == list('[y/N] '):
                print(''.join(self.line_acc), end='')
                stdin.put(str(input())+'\n')
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


if __name__ == "__main__":
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
        from pprint import pprint
        print(notifier.lines[-1])
        sys.exit(err.exit_code)

    print()
