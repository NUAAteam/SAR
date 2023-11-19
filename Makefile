CC = clang++
CFLAGS += -Wall
CFLAGS += -Wextra
CFLAGS += -g
CFLAGS += -I/usr/include/qt

LDFLAGS += `pkg-config --libs Qt5Widgets`

TARGET = testmain
OBJS = testmain.o

$(TARGET): $(OBJS)
		$(CC) $(CFLAGS) -o $(TARGET) $(OBJS) $(LDFLAGS)

testmain.o: testmain.cpp testui.hpp
		$(CC) $(CFLAGS) -c testmain.cpp

clean:
		rm -f $(TARGET) $(OBJS)