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

"""modeled.visa.ask

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass, string_types

__all__ = ['Asker']

from moretools import cached

import modeled
from modeled import mtuple, mlist

from .write import Writer


class Asker(modeled.typed.base, Writer):
    def __init__(self, minstrument):
        Writer.__init__(self, minstrument)

        self.tuple = Tuple(minstrument)
        self.list = List(minstrument)

    def __getitem__(self, mtype):
        typedcls = type(self)[mtype]
        return typedcls(self.minstrument)

    def _ask(self, string, *args, **options):
        if args:
            string = string % args
        timeout = options.get('timeout')
        if timeout is not None:
            with self.minstrument(timeout=timeout):
                return self.minstrument.visa.ask(string)
        return self.minstrument.visa.ask(string)

    def __call__(self, string, *args, **options):
        result = self._ask(string, *args, **options)
        try:
            mtype = self.mtype
        except AttributeError:
            return result

        if not isinstance(result, mtype):
            result = mtype(result)
        return result


class TupleType(Asker.type):
    @cached
    def __getitem__(cls, sep_and_mtypes):
        if isinstance(sep_and_mtypes[0], string_types):
            sep = sep_and_mtypes[0]
            mtypes = sep_and_mtypes[1:]
        else:
            sep = ','
            mtypes = sep_and_mtypes
        typedcls = Asker.type.__getitem__(cls, mtuple[mtypes])
        typedcls.sep = sep
        return typedcls


class Tuple(with_metaclass(TupleType, Asker)):
    sep = ','

    def __init__(self, minstrument):
        Writer.__init__(self, minstrument)

    def __call__(self, string, *args, **options):
        result = self._ask(string, *args, **options)
        result = result.split(self.sep)
        try:
            mtype = self.mtype
        except AttributeError:
            return tuple(result)

        return mtype(result)


class ListType(Asker.type):
    @cached
    def __getitem__(cls, sep_and_mtype):
        try:
            sep, mtype = sep_and_mtype
        except TypeError:
            mtype = sep_and_mtype
            sep = ','
        typedcls = Asker.type.__getitem__(cls, mlist[mtype])
        typedcls.sep = sep
        return typedcls


class List(with_metaclass(ListType, Asker)):
    sep = ','

    def __init__(self, minstrument):
        Writer.__init__(self, minstrument)

    def __call__(self, string, *args, **options):
        result = self._ask(string, *args, **options)
        result = result.split(self.sep)
        try:
            mtype = self.mtype
        except AttributeError:
            return result

        return mtype(result)
