#1
import os
os.mkdir("simple_dir")

#2
import os
os.makedirs("a/b/c", exist_ok=True)

#3
import os
a = os.listdir(".")
print(a)

#4
import os
for r, d, f in os.walk("."):
    print(r, f)

#5
from pathlib import Path
p = Path("new_folder")
p.mkdir(exist_ok=True)