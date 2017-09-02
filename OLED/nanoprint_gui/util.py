from collections import namedtuple


class AttrDict(dict):
  """Lets you access dict values like attributes"""
  def __init__(self, *args, **kwargs):
    super(AttrDict, self).__init__(*args, **kwargs)
    self.__dict__ = self


class Vector2D(namedtuple('Vector2D', ('x', 'y'))):
  """Immutable 2d vector lite implementation"""
  __slots__ = ()

  def __abs__(self):
    return type(self)(abs(self.x), abs(self.y))

  def __int__(self):
    return type(self)(int(self.x), int(self.y))

  def __add__(self, other):
    return type(self)(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return type(self)(self.x - other.x, self.y - other.y)

  def __mul__(self, other):
    return type(self)(self.x * other, self.y * other)

  def __div__(self, other):
    return type(self)(self.x / other, self.y / other)

  def dot_product(self, other):
    return self.x * other.x + self.y * other.y

  def distance_to(self, other):
    """ uses the Euclidean norm to calculate the distance """
    return hypot((self.x - other.x), (self.y - other.y))
