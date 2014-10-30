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

"""modeled.visa

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['mInstrument', 'mcommand', 'mcmd']

import visa

from modeled import mobject, mproperty

from .write import Writer
from .ask import Asker

from .command import (command,
  ismodeledvisacommandclass, ismodeledvisacommand,
  ismodeledvisacommandpropertyclass, ismodeledvisacommandproperty)

mcommand = mcmd = command

ismodeledvisacmdclass = ismodeledvisacommandclass
ismodeledvisacmd = ismodeledvisacommand

ismodeledvisacmdpropertyclass = ismodeledvisacommandpropertyclass
ismodeledvisacmdproperty = ismodeledvisacommandproperty


class Type(mobject.type):
    def __new__(mcs, clsname, bases, clsattrs):
        for name, obj in list(clsattrs.items()):
            if ismodeledvisacmd(obj) and not ismodeledvisacmdproperty(obj):
                clsattrs[name] = obj.method()
        return mobject.type.__new__(mcs, clsname, bases, clsattrs)


class Instrument(with_metaclass(Type, mobject)):
    def __init__(self, address, timeout=None):
        mobject.__init__(self)
        self.visa = visa.instrument(address)
        if timeout is not None:
            self.visa.timeout = timeout

        self.write = type(self).Writer(self)
        self.ask = type(self).Asker(self)

    @mproperty(float)
    def timeout(self):
        return self.visa.timeout

    @timeout.setter
    def timeout(self, seconds):
        self.visa.timeout = seconds


Instrument.Writer = Writer
Instrument.Asker = Asker

mInstrument = Instrument


from .ieee488_2 import IEEE488_2
mIEEE488_2 = IEEE488_2
