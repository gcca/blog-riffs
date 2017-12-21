#include <array>
#include <iostream>
#include <vector>

using namespace std;

vector<array<int, 4>> all = {
  {{ 1000, 62, 'a', 0 }},
  {{ 1200, 17, 'b', 1 }},
  {{  900, 31, 'c', 4 }},
};

vector<array<int, 4>>* get_all() {
  vector<array<int, 4>> *list = new vector<array<int, 4>>();
  for (const auto &item : all)
    if (item[3] == 4)
      list->push_back(item);
  return list;
}

//

auto gameboard = all;
#define PROGRESS_STATUS 4
#define CROWNED 4

vector<array<int, 4>>* get_crowned_pieces_1() {
  vector<array<int, 4>> *crowned_pieces = new vector<array<int, 4>>();
  for (const auto &piece : gameboard)
    if (piece[PROGRESS_STATUS] == CROWNED)
      crowned_pieces->push_back(piece);
  return crowned_pieces;
}

//

class Piece {
public:
  bool is_crowned() const { return true; }
};

vector<Piece> gameboard_pieces;

vector<Piece>* get_crowned_pieces_2() {
  vector<Piece> *crowned_pieces = new vector<Piece>();
  for (const auto &piece : gameboard_pieces)
    if (piece.is_crowned())
      crowned_pieces->push_back(piece);
  return crowned_pieces;
}

//

int main() {
  return 0;
}
