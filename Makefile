OUT := magnetic_time_crystal
TARGET := $(OUT)/nano_magnetisation
CC ?= gcc
CLFAGS += -Os -Wall -Wextra -Wpedantic

$(TARGET).so: $(TARGET).o
	$(CC) -shared -o $(TARGET).so $(TARGET).o

$(TARGET).o: $(TARGET).c
	$(CC) -c $(CLFAGS) -fpic $(TARGET).c -o $(TARGET).o
