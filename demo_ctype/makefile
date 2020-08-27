# Compiler
CC      	:= gcc
# Path
SRC_PATH  := src
BUILD_PATH:= build
BIN_PATH  := bin
# Executable
BIN_NAME	:= main
# Extensions
SRC_EXT 	:= c
# Code lists
# Find all source files in the source directory, sorted by most recently 
# modified.
SRC       := $(shell find $(SRC_PATH) -name '*.$(SRC_EXT)' | sort -k 1nr | cut -f2-)
# Set the OBJect file names, with the source directory stripped from the path,
# and the build path prepended in its place.
OBJ       := $(SRC:$(SRC_PATH)/%.$(SRC_EXT)=$(BUILD_PATH)/%.o)
BUILD 	  := $(SRC:$(SRC_PATH)/%.$(SRC_EXT)=$(BUILD_PATH)/lib%.so)
# Set the dependency files that will be used to add header dependencies.
DEPS      := $(OBJ:.o=.d)
# Flags
C_FLAGS  	:=
INCL_PATH	:= -I include/
LIBS_PATH	:= -L 
LIBS 			:= -lm

PY        := python3
PY_EXT    := py
PY_SRC    := $(shell find $(SRC_PATH) -name '*.$(PY_EXT)' | sort -k 1nr | cut -f2-)

.PHONY: dirs
dirs:
	@echo "Creating directories"
	@mkdir -p $(dir $(OBJ))
	@mkdir -p $(BIN_PATH)

.PHONY: clean
clean:
	@echo "Deleting directories"
	@rm -rf $(BIN_PATH) $(BUILD_PATH)
	@echo "Deleting @(BIN_NAME) symlink"
	@rm -f $(BIN_NAME)

# Make all and run executable
.PHONY: run
run: dirs all
	./$(BIN_PATH)/$(BIN_NAME)

# Checks the executable and symlinks to the output>
.PHONY: all
all: dirs $(BIN_PATH)/$(BIN_NAME)
	@echo "Making symlink: $(BIN_NAME) -> $<"
	@rm -f $(BIN_NAME)
	@ln -s $(BIN_PATH)/$(BIN_NAME) $(BIN_NAME)

# Creation of the executable
$(BIN_PATH)/$(BIN_NAME): $(OBJ)
	@echo "Linking: $@"
	$(CC) $(C_FLAGS) $(OBJ) $(LIBS) -o $@

# Compiling to objects
$(BUILD_PATH)/%.o: $(SRC_PATH)/%.$(SRC_EXT)
	@echo "Compiling: $< -> $@"
	$(CC) $(C_FLAGS) $(INCL) -c $< -o $@

# Compiling to library
.PHONY: lib
lib: dirs $(BUILD)

$(BUILD): $(SRC)
	@echo "Compiling: $< -> $@"
	$(CC) -fPIC -shared -o $@ $^

.PHONY: run_py
run_py: lib
	$(PY) $(PY_SRC)
