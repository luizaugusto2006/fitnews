"""Ponto de entrada WSGI para PythonAnywhere (configure em WSGI configuration file)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app  # noqa: E402

if __name__ == "__main__":
    app.run()
