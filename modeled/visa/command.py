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

"""modeled.visa.command

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

from moretools import cached

import modeled
from modeled import mtuple, mproperty


class command(modeled.typed.base):
    def __init__(self, string):
        self.cmdstring = string

    def method(self, mtype=None):
        string = self.cmdstring
        if mtype is None:
            mtype = self.mtype

        def method(self, *args, **options):
            return self.ask[mtype](string, *args, **options)

        ## method.__name__ = self.name
        return method


class PropertyType(mproperty.type):
    @cached
    def __getitem__(cls, mtype):
        # to disable creation of new __init__ in mproperty.type.__getitem__
        class typedcls(cls):
            pass

        return mproperty.type.__getitem__(cls, mtype, typedcls=typedcls)


class property(with_metaclass(PropertyType, mproperty, command)):
    def __init__(self, cmdstring):
        command.__init__(self, cmdstring)
        mproperty.__init__(self, fget=self.method())


class ListProperty(with_metaclass(PropertyType,
  mproperty.list, property, command
  )):
    def __init__(self, cmdstring):
        command.__init__(self, cmdstring)
        mproperty.list.__init__(self, fget=self.method())


class DictPropertyType(PropertyType, mproperty.dict.type):
    @cached
    def __getitem__(cls, mtypes):
        class typedcls(cls):
            pass

        return PropertyType.__getitem__(cls, mtuple[mtypes])


class DictProperty(with_metaclass(DictPropertyType,
  mproperty.dict, property, command
  )):
    def __init__(self, cmdstring):
        command.__init__(self, cmdstring)
        mproperty.dict.__init__(self,
          fget=self.method(mtype=self.mvaluetype))


property.list = ListProperty
property.dict = DictProperty

command.property = property


def ismodeledvisacommandclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.visa.command`.
    """
    try:
        return issubclass(cls, command)
    except TypeError: # No class at all
        return False


def ismodeledvisacommand(obj):
    """Checks if `obj` is an instance of :class:`modeled.visa.command`.
    """
    return isinstance(obj, command)


def ismodeledvisacommandpropertyclass(cls):
    """Checks if `cls` is a subclass
       of :class:`modeled.visa.command.property`.
    """
    try:
        return issubclass(cls, property)
    except TypeError: # No class at all
        return False


def ismodeledvisacommandproperty(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.visa.command.property`.
    """
    return isinstance(obj, property)
