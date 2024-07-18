
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <list>

typedef struct
{
  int x;
  int y;
} position;

std::list<position> houses;

void move(position &current, char c)
{
  if(c == '<') current.x--;
  else if(c == '>') current.x++;
  else if(c == '^') current.y++;
  else if(c == 'v') current.y--;

  bool visited = false;

  for (std::list<position>::iterator it = houses.begin(); it != houses.end(); ++it)
    if(it->x == current.x && it->y == current.y) visited = true;

  if(!visited)
    houses.push_back(current);
}


int main(void)
{

  int output = 0;
  char c;

  position santa = {0,0};
  position robo = {0,0};

  std::ifstream input("input.txt");

  houses.push_back(santa);

  int turn = 0;

  while(input.get(c))
  {
    if(turn % 2)
      move(santa, c);
    else
      move(robo, c);

    turn++;
  }

  std::cout << "Houses visted: " << houses.size();

}
