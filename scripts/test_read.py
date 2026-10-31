import re
import os

with open("frontend/landing.html", "r", encoding="utf-8") as f:
    content = f.read()

print(f"Total characters in landing.html: {len(content)}")
