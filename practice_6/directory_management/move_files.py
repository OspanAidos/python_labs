#1
import os
os.rename("old_dir", "new_dir")

#2
import shutil
shutil.move("file.txt", "subdir/file.txt")

#3
import os
os.replace("tmp.txt", "final.txt")

#4
import shutil
shutil.copytree("src_dir", "backup_dir")

#5
import os
os.chdir("..")