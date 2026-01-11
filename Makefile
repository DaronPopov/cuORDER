CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c11 -Iinclude -IcJSON
LDFLAGS = cJSON/libcjson.a

# Source files
SRCS = src/main.c src/hardware_detector.c src/cuda_resolver.c src/docker_generator.c src/config_parser.c
OBJS = $(SRCS:.c=.o)

# Target executable
TARGET = cuda_env_resolver

.PHONY: all clean install test

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	cp $(TARGET) /usr/local/bin/

test: $(TARGET)
	./test_hardware.sh

# Development dependencies
deps:
	# Install cJSON for JSON parsing
	git clone https://github.com/DaveGamble/cJSON.git
	cd cJSON && make && sudo make install
	rm -rf cJSON

	# Install Docker if not present
	which docker || echo "Please install Docker manually"