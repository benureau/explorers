from __future__ import absolute_import, division, print_function, unicode_literals
import abc

class Environment(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def cfg(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, order):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, C):
        check = NotImplemented
        if cls is Environment:
            check = True
            required = ['execute', 'cfg']
            for method in required:
                if not any(method in B.__dict__ for B in C.__mro__):
                    check = NotImplemented
        return check