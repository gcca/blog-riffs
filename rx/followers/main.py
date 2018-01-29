import rx
import requests

from pprint import pprint

class Display:

  def __init__(self):
    self.times = 0

  def startup(self):
    requestStream = rx.Observable.just('https://api.github.com/users')
    responseStream = requestStream.map(lambda uri: requests.get(uri))
    payloadStream = responseStream.map(lambda response: response.json())
    usersStream = payloadStream.flat_map(lambda user: user)
    startStream = usersStream.take(3)
    return startStream
    # return (
      # rx.Observable
        # .just('https://api.github.com/users')
        # .map(lambda uri: requests.get(uri))
        # .map(lambda response: response.json())
        # .flat_map(lambda user: user)
        # .take(3)
    # )

  def refresh(self):
    self.times += 1

    resourceStream = rx.Observable.just('https://api.github.com/users')
    timesStream = rx.Observable.just(self.times)
    queryStream = rx.Observable.zip_list(resourceStream, timesStream).map(tuple)

    requestStream = queryStream.map(lambda q: '%s?since=%d' % q)
    responseStream = requestStream.map(lambda path: requests.get(path))
    payloadStream = responseStream.map(lambda response: response.json())
    usersStream = payloadStream.flat_map(lambda user: user)
    refreshStream = usersStream.take(3)
    return refreshStream
    # return (
      # rx.Observable
        # .zip_list(rx.Observable.just('https://api.github.com/users'),
                  # rx.Observable.just(self.times))
        # .map(tuple)
        # .map(lambda q: '%s?since=%d' % q)
        # .map(lambda path: requests.get(path))
        # .map(lambda response: response.json())
        # .flat_map(lambda user: user)
        # .take(3)
    # )

def main():
  display = Display()
  display.refresh().subscribe(pprint)


if '__main__' == __name__:
  main()
