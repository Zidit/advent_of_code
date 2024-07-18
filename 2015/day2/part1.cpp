
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

    std::string tmp = s;
    std::replace( tmp.begin(), tmp.end(), 'x', ' ');
    std::istringstream iss(tmp);

    iss >> x;
    iss >> y;
    iss >> z;

    return 2 * (x*y + y*z + z*x) + min(min(x*y, y*z ), z*x);
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
