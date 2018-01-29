import data

class _request:

  def __init__(self, response):
    self.response = response
    next = response[-1]['id']
    self.headers = {
      'Link': f'<https://api.github.com/users?since={next}>; rel="next", <https://api.github.com/users{{?since}}>; rel="first"'
    }

  def json(self):
    return self.response


def get(url):
  print(' - - - - - GET - - - - -')
  if 'https://api.github.com/users' == url or 'https://api.github.com/users?since=0' == url:
    response = data.a[0]
  elif 'https://api.github.com/users?since=46' == url:
    response = data.b[0]
  else:
    response = [{ 'id': 120, 'login': '' }]
  return _request(response)


