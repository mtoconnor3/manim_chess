VENV=.manimchess
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: all venv deps sysdeps clean manim-render run

all: sysdeps venv deps

# Create virtual environment using uv
venv:
	uv venv $(VENV)

# Install Python dependencies
deps: venv
	uv pip install python-chess manim numpy networkx networkx

# Install system dependencies required by Manim
sysdeps:
	@echo "Installing system dependencies for Manim..."
	# Linux (apt)
	if command -v apt-get >/dev/null; then \
		sudo apt-get update && sudo apt-get install -y \
			ffmpeg texlive texlive-latex-extra texlive-fonts-extra \
			sox libcairo2-dev libpango1.0-dev; \
	# MacOS (brew)
	elif command -v brew >/dev/null; then \
		brew install ffmpeg mactex sox cairo pango; \
	else \
		echo "No supported package manager found (apt/brew). Install ffmpeg manually."; \
	fi

# Remove virtual environment and build artifacts
clean:
	rm -rf $(VENV)
	rm -rf media/
	rm -rf __pycache__/