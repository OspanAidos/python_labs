#1
import shutil
shutil.copy("src.txt", "dst.txt")

#2
import shutil
shutil.copy2("src.txt", "dst_meta.txt")

#3
import os
if os.path.exists("old.txt"):
    os.remove("old.txt")

#4
import shutil
shutil.move("a.txt", "b.txt")

#5
from pathlib import Path
Path("temp.txt").unlink(missing_ok=True)