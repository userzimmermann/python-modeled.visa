# python-modeled.visa
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# python-modeled.visa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-modeled.visa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-modeled.visa.  If not, see <http://www.gnu.org/licenses/>.

"""modeled.visa.write

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Writer']


class Writer(object):
    def __init__(self, minstrument):
        self.minstrument = minstrument

    def __call__(self, string, *args, **options):
        if args:
            string = string % args
        timeout = options.get('timeout')
        if timeout is not None:
            with self.minstrument(timeout=timeout):
                self.minstrument.visa.write(string)
        else:
            self.minstrument.visa.write(string)


