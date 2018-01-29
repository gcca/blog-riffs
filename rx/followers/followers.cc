#include <iostream>
#include <string>

#include <rxcpp/rx.hpp>

using namespace std;

namespace rx = rxcpp;
namespace rxs = rxcpp::subjects;

using another_t = int;
using refresh_t = nullptr_t;
using startup_t = nullptr_t;

class Emitter
{
  rxs::subject<another_t> another_source;
  rxs::subject<refresh_t> refresh_source;
  rxs::subject<startup_t> startup_source;
public:
  rx::observable<another_t> another_stream;
  rx::observable<refresh_t> refresh_stream;
  rx::observable<startup_t> startup_stream;

  Emitter()
  {
    another_stream = another_source.get_observable();
    refresh_stream = refresh_source.get_observable();
    startup_stream = startup_source.get_observable();
  }

  void another(int n)
  {
    another_source.get_subscriber().on_next(n);
  }

  void refresh()
  {
    refresh_source.get_subscriber().on_next(nullptr);
  }

  void startup()
  {
    startup_source.get_subscriber().on_next(nullptr);
  }
};

auto connect(rx::observable<another_t> another_stream,
             rx::observable<refresh_t> refresh_stream,
             rx::observable<startup_t> startup_stream)
{
  return rx::observable<>::just(string("https://api.github.com/users"))
    .combine_latest(
      [](auto b, auto p) {
        return b + p;
      }
    ,
      startup_stream
        .map([](auto) {
          return string("");
        })
        .merge(
          refresh_stream
            .map([](auto) {
              return 1;
            })
            .scan(0, [](int a, int i) {
              return a + i;
            })
            .map([](int i) {
              return string("?since=") + to_string(i);
            })
        )
    );
}

int main()
{

  rxs::subject<int> s;

  s.get_observable().scan(1, [](int a, int i) {
    return a + i;
  });

  s.get_observable().subscribe([](int n) {
    cout << n << endl;
  });

  //s.get_subscriber().on_next(1);


  return 0;

  Emitter emit;

  connect(
    emit.another_stream,
    emit.refresh_stream,
    emit.startup_stream
  )
  .subscribe([](auto url) {

    cout << url << endl;
  });

  cout << "\033[32mstartup" << endl;
  emit.startup();

  cout << "\033[31mrefresh" << endl;
  emit.refresh();

  cout << "\033[33manother(1)" << endl;
  emit.another(1);

  cout << "\033[34manother(2)" << endl;
  emit.another(2);

  cout << "\033[35manother(0)" << endl;
  emit.another(1);

  cout << "\033[36manother(1)" << endl;
  emit.another(0);

  cout << "\033[37mrefresh" << endl;
  emit.refresh();

  return 0;
}
