VENV=.manimchess
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: all venv deps sysdeps clean manim-render run

all: uv sysdeps venv deps

# Install uv
uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "uv not found — installing globally..."; \
		wget -qO- https://astral.sh/uv/install.sh | sh; \
	else \
		echo "uv already installed on system."; \
	fi

# Create virtual environment using uv
venv:
	uv venv $(VENV)

# Install Python dependencies
deps: venv
	uv pip install python-chess manim numpy networkx networkx

# Install system dependencies required by Manim
sysdeps:
	@echo "Installing system dependencies for Manim..."
	if command -v apt-get >/dev/null 2>&1; then \
		sudo apt-get update && sudo apt-get install -y \
			ffmpeg texlive texlive-latex-extra texlive-fonts-extra \
			sox libcairo2-dev libpango1.0-dev; \
		wget -qO- https://astral.sh/uv/install.sh | sh; \
	elif command -v brew >/dev/null 2>&1; then \
		brew install ffmpeg sox cairo pango mactex; \
	else \
		echo "No supported package manager found (apt/brew). Install ffmpeg + LaTeX manually."; \
	fi

# Remove virtual environment and build artifacts
clean:
	rm -rf $(VENV)
	rm -rf media/
	rm -rf __pycache__/