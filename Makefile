# === CONFIGURATION ===
SRC_DIR = src
BUILD_DIR = build

MPY_CROSS = mpy-cross
MPREMOTE = mpremote

# Files that MUST stay as .py for MicroPython to auto-run
ENTRY_PY_FILES = boot.py main.py

.PHONY: all compile flash clean repl

all: compile flash

compile:
	@mkdir -p $(BUILD_DIR)
	@for file in $(SRC_DIR)/*.py; do \
		base=$$(basename $$file); \
		if echo "$(ENTRY_PY_FILES)" | grep -wq "$$base"; then \
			echo "Copying $$file (not compiling)..."; \
			cp $$file $(BUILD_DIR)/$$base; \
		else \
			echo "Compiling $$file to $(BUILD_DIR)/$${base%.py}.mpy..."; \
			$(MPY_CROSS) $$file -o $(BUILD_DIR)/$${base%.py}.mpy; \
		fi \
	done

flash:
	@for file in $(BUILD_DIR)/*; do \
		echo "Flashing $$file..."; \
		$(MPREMOTE) cp $$file :; \
	done

clean:
	rm -rf $(BUILD_DIR)

repl:
	$(MPREMOTE) repl
