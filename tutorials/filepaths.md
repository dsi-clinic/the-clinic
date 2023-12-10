## File Systems

A core component of operating systems is the file system. The file system determines the structure that data is stored and the methods used to access data. The most common type of data is a `file`. These can be many things, like PDFs, Jupyter Notebooks, music, images, code, etc. Files are stored in a directory structure. You can think of the file system as storing files in a [tree structure](https://en.wikipedia.org/wiki/Tree_(data_structure)). Each file is a leaf and each directory is a branch node. 

## Paths

A file path is the address of a file. It is the human readable directions for how to find a given file. The full path for a given file starts out with the `root` directory of your computer. On Linux and Mac OS, the root directory is notated as `/`. It's a bit more complicated on Windows, but you can think of the root as (usually) `C:\`. When reading a full (or absolute) path, each directory or file is separated by a `/` (or a `\` on Windows). So `/home/username/core-facility-docs/filepaths.md` tells me exactly where the file is located on my computer. The root directory has a child directory `home` which has a child directory `username` which has a child directory `core-facility-docs` which contains the `filepaths.md` file. 

In your terminal, you can see the contents of a directory withe the `ls` command (or `dir` on Windows). You can see the path to your current directory with the `pwd` (print working directory) command. 

### Absolute vs Relative Paths

If your current working directory is `/home/username/core-facility-docs`, you can specify the path to `/home/username/core-facility-docs/filepaths.md` as just `filepaths.md`. That is the relative path. It is relative to the current working directory. Any path that doesn't start with `/` (signifying the root directory) or `~` (signifying `/home/<username>` where `<username>` is your username) will be interpreted as a relative path. Conversely, any path that starts with `/` or `~` will be treated as an absolute path.


## Paths in Python

When you run a python file, the working directory is determined by *where* you ran the file.

Imagine your directory structure is as follows:
```
/ (root directory)
├──  etc
├──  lib
├──  home
|   ├──  <username>
|       ├──  my-python-project 
|       ├──  2023-fall-clinic-project
|           ├── README.md
|           ├── .gitignore
|           ├── Dockerfile
|           ├── notebooks/
|           │   ├── README.md
|           │   └── ...
|           ├── utils/
|           │   ├── README.md
|           │   ├── __init__.py
|           │   └── pipeline.py
|           ├── data/
|           │   ├── README.md 
|           │   └── results.csv 
|           ├──  ... 
├──  ...
```
And `/home/<username>/2023-fall-clinic-project/utils/pipeline.py` contains the following:
```python
import pandas as pd

results_df = pd.read_csv("../data/results.csv")
```
Now if you run 

```bash
<username>@Desktop:~/2023-fall-clinic-project/utils$ pwd
/home/<username>/2023-fall-clinic-project/utils
<username>@Desktop:~/2023-fall-clinic-project/utils$ python pipeline.py
```
The script will successfully run and find the `results.csv` file because the current working directory is `/home/<username>/2023-fall-clinic-project/utils`, so `..` takes you to `/home/<username>/2023-fall-clinic-project/`, and then `data/results.csv` resolves the path to `/home/<username>/2023-fall-clinic-project/data/results.csv` which exists.

However, if you ran:
```bash
<username>@Desktop:~/2023-fall-clinic-project$ pwd
/home/<username>/2023-fall-clinic-project
<username>@Desktop:~/2023-fall-clinic-project$ python utils/pipeline.py
```
The script will fail. Because the current working directory is `/home/<username>/2023-fall-clinic-project/`, `..` will translate to `/home/<username>`, so `../data/results.csv` will translate to `/home/<username>/data/results.csv` which doesn't exist (or if it does exist is probably not what you expected!)

Remember one of our main goals if for code to reproducible. Constraints like from which directory you can run a script are burdensome and simply won't work for many use cases.

A potential fix is to change to using absolute paths in your python scripts. This, however, makes your scripts dependent on your username and what directory you saved the python script in. This is also not good and leads to lots of bugs and makes it difficult to reproduce your code. 

To get around these two issues, you can make your paths relative to something that will stay the same regardless of who is running the program and how they are running it. Python's `pathlib` package allows you to access the path to the current file. For example: 
```python
import pandas as pd
from pathlib import Path

# here resolves to the path of the current python file
here = Path(__file__).resolve()
# repo_root will be the absolute path to the root of the repository,
# no matter where the repository is. 
# For pathlib Path objects, `.parent` gets the parent directory and `/`
# can be used like `/` in unix style paths.
repo_root = here.parent.parent
results_df = pd.read_csv(repo_root / "data" / "results.csv")

```
This script will work regardless of where it is called from, whose computer it is on,
and where the repository was installed. 