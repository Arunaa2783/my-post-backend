#include <iostream>
#include <string>
#include <sstream>

extern "C" int count_words(const char* text) {
    std::istringstream iss(text);
    int count = 0;
    std::string word;
    while (iss >> word) {
        count++;
    }
    return count;
}
