## File Systems

A core component of most operating systems is the file system. The file system determines the structure that data is stored and the methods used to access data. The most common type of data is a `file`. These can be many things, like PDFs, Jupyter Notebooks, music, images, code, etc. Files are stored in a directory structure. You can think of the file system as storing files in a [tree structure](https://en.wikipedia.org/wiki/Tree_(data_structure)). Each file is a leaf and each directory is a branch node. 

## Paths

A file path is the address of a file. It is the human readable directions for how to find a given file. The full path for a given file starts out with the `root` directory of your computer. On Linux and Mac OS, the root directory is notated as `/`. It's a bit more complicated on Windows, but you can think of the root as (usually) `C:\`. When reading a full (or absolute) path, each directory or file is separated by a `/` (or a `\` on Windows). So `/home/username/core-facility-docs/filepaths.md` tells me exactly where the file is located on my computer. The root directory has a child directory `home` which has a child directory `username` which has a child directory `core-facility-docs` which contains the `filepaths.md` file. 

In your terminal, you can see the contents of a directory withe the `ls` command (or `dir` on Windows). You can see the path to your current directory with the `pwd` (print working directory) command. 

### Absolute vs Relative Paths

If your current working directory is `/home/username/core-facility-docs`, you can specify the path to `/home/username/core-facility-docs/filepaths.md` as just `filepaths.md`. That is the relative path. It is relative to the current working directory. Any path that doesn't start with `/` (signifying the root directory) or `~` (signifying `/home/<username>` where `<username>` is your username) will be interpreted as a relative path. Conversely, any path that starts with `/` or `~` will be treated as an absolute path.


## Paths in Python

When you run a python file, the working directory is determined by *where* you ran the file. For example: If your working directory is `/home/username/core-facility-docs` and you run `python scripts/run.py`, the working directory is `/home/username/core-facility-docs`, *not* `/home/username/core-facility-docs/scripts` which is where the script is located. This is a common piece of confusion. If you write a relative path in a python file, it will be relative to different locations depending on how you run the script. This is not good and leads to lots of bugs!

The best fix is often to change to using absolute paths in your python scripts. This, however, makes your scripts dependent on your username and what directory you saved the python script in. This is also not good and leads to lots of bugs!