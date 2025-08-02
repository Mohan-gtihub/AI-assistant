#!/usr/bin/env python3
import os
import sys

# Load environment variables from .env file
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Import and run the application
from magic_wand import main

if __name__ == "__main__":
    main()
