"""{* app_name *} wsgi handler."""
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from app import app

if __name__ == "__main__":
    app.run()
