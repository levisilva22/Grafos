from typing import Generator
from abc import ABC, abstractmethod

class GraphBase(ABC):
  """
  Generic class for a graph
  ...

  Attributes
  ----------
  n : int
      Cardinality of the set of vertices V.
  m : int
      Cardinality of the set of edges E.
  directed : bool
      Defines if the graph is directed or not.

  """

  def __init__(self, n: int, directed: bool = False) -> None:
    self.n, self.m, self.directed = n, 0, directed

  @abstractmethod
  def addEdge(self, v : int, w : int):
    ''' Adds edge vw to the graph

    Parameters
    ----------
    v : int
      first vertex.
    w : int
      second vertex.
    '''
    pass

  @abstractmethod
  def removeEdge(self, v: int, w: int):
    ''' Removes edge vw from the graph

    Parameters
    ----------
    v : int
      first vertex.
    w : int
      second vertex.
    '''
    pass

  '''def getNeighbors(self, v : int, mode : str = "*", closed : bool = False) -> Generator[int, None, None]:
    Provides the neighbors of vertex v.

    Parameters
    ----------
    v : int
      vertex.
    mode : str
      Only for directed graph. "-" if input neighborhood, "+" if output neighborhood and "*" if any.
    closed : bool
      Defines if it is a closed or open interval. True if the neighboorhood should include v or False if it should exclude.
    iterateOverNode : bool
      Defines if the iterator gives the pair of vertices (False) or a pair consisting of v and a node

    Yields
    ----------
    int
      neighbor of vertex v.

    
    pass'''
  
  """  @abstractmethod
  def isNeighbor(self, v: int, w: int) -> bool:
    '''Checks if v and w are adjacent

    Parameters
    ----------
    v : int
      first vertex.
    w : int
      second vertex.

    Returns
    ----------
    bool
      True if v and w are adjacent, False otherwise.
    '''
    pass
  """
  def V(self) -> Generator[int, None, None]:
    """
    Retorna a lista de vértices.
    """
    for i in range(1, self.n+1):
      yield i

  def E(self, iterateOverNode = False) -> Generator[tuple[int,int], None, None] | Generator[tuple[int, object], None, None]:
    """
    Retorna a lista de arestas vw
    """

    for v in self.V():
      for w in self.getNeighbors(v, mode = "+" if self.directed else "*"):
        count = True

        if not self.directed: # avoid double counting
          wint = int(w) # assures int, even if it's an object/node
          count = v < wint

        if count:
          yield (v,w)



class GraphAdjMatrix(GraphBase):
  def __init__(self, n, directed = False):
    super().__init__(n, directed)
    self.M = [None]*(self.n)
    for i in range(0, self.n):
      self.M[i] = [None]*(self.n)

  def addEdge(self, v: int, w: int):
    self.M[v][w] = w
    if not self.directed:
      self.M[w][v] = v
    self.m += 1

  def removeEdge(self, v: int, w: int):
    self.M[v][w] = 0
    if not self.directed:
      self.M[w][v] = 0
    self.m -= 1

'''
def isNeighbor(self, v, w):
    """

    Parameters
    ----------
    w : object
    """
    return self.M[v][w] == w

  
  def getNeighbors(self, v, mode = "*", closed = False):
    if closed:
      yield v

    w = 1

    while w <= self.n:
      if self.directed:
        if mode == "*" and (self.isNeighbor(v, w) or self.isNeighbor(w, v)):
            yield w
        elif mode == "+" and self.isNeighbor(v, w):
            yield w
        elif mode == "-" and self.isNeighbor(w, v):
            yield w
      else:
        if self.isNeighbor(v, w):
          yield w

      w += 1
'''