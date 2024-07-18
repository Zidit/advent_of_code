
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




int main(void)
{

  int output = 0;
  char c;

  position current =  {0,0};
  std::list<position> houses;
  std::ifstream input("input.txt");

  houses.push_back(current);

  while(input.get(c))
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

  std::cout << current.x << "," << current.y << std::endl;
  std::cout << "Houses visted: " << houses.size();

}
