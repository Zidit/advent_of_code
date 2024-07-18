
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>

int min(int x, int y)
{
  if (x < y) return x;
  else return y;
}



int paper_needed(std::string const & s)
{
    int result = 0;
    int x, y, z;
    int size;

    std::string tmp = s;
    std::replace( tmp.begin(), tmp.end(), 'x', ' ');
    std::istringstream iss(tmp);

    iss >> x;
    iss >> y;
    iss >> z;

    if (x >= y && x >= z) size = y + z;
    else if (y >= x && y >= z) size = x + z;
    else if (z >= x && z >= y) size = y + x;

    return 2 * size + x*y*z;
}


int main(void)
{

  int output = 0;
  std::ifstream input("input.txt");

  for (std::string line; std::getline(input, line); ) {
    output += paper_needed(line);
  }

  std::cout << output;

}
