CXX = g++
CXXFLAGS = -Wall -std=c++11

TARGET = chat_program
SRC = main.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

test_chat: test_chat.cpp
	$(CXX) $(CXXFLAGS) -o test_chat test_chat.cpp

clean:
	rm -f $(TARGET) 