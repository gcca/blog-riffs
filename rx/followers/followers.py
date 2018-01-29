import re

from functools import reduce
from pprint import pprint

import rx

import requests


RE_LINK = re.compile(r'<(.+)>; rel="next"')


class Emitter:

  def __init__(self):
    self.__anotherSource = rx.subjects.Subject()
    self.__refreshSource = rx.subjects.Subject()
    self.__startupSource = rx.subjects.Subject()

    self.anotherStream = self.__anotherSource.as_observable()
    self.refreshStream = self.__refreshSource.as_observable()
    self.startupStream = self.__startupSource.as_observable()

  def another(self, index):
    self.__anotherSource.on_next(index)

  def refresh(self):
    self.__refreshSource.on_next(None)

  def startup(self):
    self.__startupSource.on_next(None)


def main():
  emit = Emitter()
  followers_stream = connect(emit.anotherStream,
                             emit.refreshStream,
                             emit.startupStream)
  followers_stream.subscribe(pprint)
  print('\033[32mstartup')
  emit.startup()
  print('\033[33mrefresh')
  emit.refresh()
  print('\033[31manother 2')
  emit.another(2)
  print('\033[34manother 1')
  emit.another(1)
  print('\033[35manother 0')
  emit.another(0)
  print('\033[36manother 1')
  emit.another(1)
  print('\033[37mrefresh')
  emit.refresh()

  emit.refresh()
  emit.refresh()
  emit.refresh()
  emit.refresh()
  emit.refresh()
  emit.refresh()

  emit.refresh()
  emit.refresh()
  emit.refresh()


def connect(another_stream, refresh_stream, startup_stream):
  both_stream = startup_stream.merge(refresh_stream)
  fire_stream = (
    both_stream
      .flat_map(lambda _: rx.Observable.range(0, 3))
      .merge(another_stream)
  )

  return (
    rx.Observable
      .zip(
        fire_stream
      ,
        fire_stream
          .buffer_with_count(30)
          .start_with(None)
          .scan(
            lambda a, l:
              (
                lambda r: (
                  RE_LINK.match(r.headers['Link']).group(1),
                  r.json()
                )
              )(requests.get(a[0]))
            ,
            ('https://api.github.com/users', None)
          )
          .flat_map(lambda t: t[1])
          .map(lambda u: u['login'])
      ,
        lambda i, u: (i, u)
      )
      .buffer(both_stream.merge(another_stream))
      .scan(
        lambda a, e:
          reduce(lambda a, e: a[:e[0]] + [e[1]] + a[e[0]+1:], e, a)
        ,
        3 * [None]
      )
  )


if '__main__' == __name__:
  main()
