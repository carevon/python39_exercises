

_MISSING = object()

class computed_property:
    """Uma `property` cujo valor calculado é cacheado enquanto os atributos-dependência
    informados não mudarem. Dependências que não existem na instância são tratadas como
    inalteradas. Suporta setter, deleter e docstring, a exemplo do `property` embutido.
    """

    def __init__(self, *dependencies):
        self._dependencies = dependencies
        self.fget = None
        self.fset = None
        self.fdel = None
        self.__doc__ = None

    def __call__(self, fget):
        self.fget = fget
        self.__doc__ = fget.__doc__
        return self

    def __set_name__(self, owner, name):
        self._name = name
        self._cache_key = '_computed_' + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        
        current = tuple(getattr(instance, dep, _MISSING) for dep in self._dependencies)
        cache = instance.__dict__.get(self._cache_key)
        if cache is not None and cache[0] == current:
            return cache[1]
        value = self.fget(instance)
        instance.__dict__[self._cache_key] = (current, value)
        return value

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self


if __name__ == '__main__':
    pass