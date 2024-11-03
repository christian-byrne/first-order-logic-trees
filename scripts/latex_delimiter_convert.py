import re
import os
from rich import print

# We convert from the latex syntax which uses "\( " and "\) " to the markdown inline math syntax which uses "$" and "$".
# Likewise, for multiline math, we convert from "\[ " and "\] " to "$$". 
FROM_TO = [
  (r"\\\( ", r"$"),
  (r" \\\)", r"$"),
  (r"\\\[\s*", "$$"),
  (r"\\\]\s*", "$$"),
]

input_filepath = input("Enter the path to the input file: ")

candidates = [
  # As given at cmdline
  input_filepath,
  # As given relative to the current working directory
  os.path.join(os.getcwd(), input_filepath),
  # As given relative to the script's directory
  os.path.join(os.path.dirname(os.path.abspath(__file__)), input_filepath),
  # As given relative to the script's parent directory
  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), input_filepath),
  # As given relative to the script's grandparent directory
  os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), input_filepath),
  # As given relative to the user home directory
  os.path.join(os.path.expanduser("~"), input_filepath),
]

resolved_path = None
for candidate in candidates:
  if os.path.exists(candidate):
    resolved_path = candidate
    print(f"Resolved path to input file: {resolved_path}")
    break

if resolved_path is None:
  print(f"Could not find the input file at any of the following locations: {candidates}")
  exit(1)

overwrite = input("Do you want to overwrite the input file? (y/n): ").lower().strip() == "y"


if overwrite:
  output_path = resolved_path
else:
  from pathlib import Path
  output_path = Path(resolved_path).with_name(f"{Path(resolved_path).stem}_converted{Path(resolved_path).suffix}")

with open(resolved_path, "r") as f:
  content = f.read()

for from_, to in FROM_TO:
  content = re.sub(from_, to, content)

with open(output_path, "w") as f:
  f.write(content)

print(f"Converted content written to {output_path}")

# Create a temp PDF file with pandoc to check the conversion

os.system(f"pandoc {output_path} -o {output_path.with_suffix('.pdf')}")

os.system(f"xdg-open {output_path.with_suffix('.pdf')}")

keep = input("Do you want to keep the preview PDF file? (y/n): ").lower().strip() == "y"

if not keep:
  os.remove(output_path.with_suffix('.pdf'))

print("Done!")
