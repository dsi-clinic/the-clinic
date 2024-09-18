## Using Submitit for Long Jobs

For some projects we use [submitit](https://github.com/facebookincubator/submitit) to submit jobs in Python. Another option that is sometimes used is directly writing `sbatch` commands. Each method has its positive and negative aspects. This document details using submitit.

When we use slurm, we must be respectful to not overuse nodes. Please:
- To test code, submit it to the `dev` queue or test them with less data in an interactive session
- Don't run computation heavy jobs on the login nodes. Submit them as jobs
- Do not submit many jobs at once
- To run code you are confident works, submit it to the `general` queue

### Background

To understand how we use submitit, some background knowledge will be useful:
1. `if __name__ == "__main__":` blocks. The code under these blocks will run when the file is run as a script and not when it is imported as a module. For more information, see [this](https://realpython.com/if-name-main-python/)
2. Command Line Arguments. When you run something as a script, adding command line arguments can allow you to modify arguments without going into your python code. We'll use a package called argparse to convert command line arguments into easily parsable python objects. For more information, see [this tutorial](https://realpython.com/python-command-line-arguments/) and [argparse documentation](https://docs.python.org/3/library/argparse.html)
3. JSON. We'll use the json file format to store configuration. This is basically like a python dictionary. 

### Preparing Your Code

To make use of submitit, a long script with no functions or a jupyter notebook will not work. You will need to think of how to write your code in a manner that is more abstract by using python functions and classes. Your code should be: ready for change, easy to understand, and safe from bugs. There are plenty of [good resources](https://web.mit.edu/6.031/www/sp22/classes/04-code-review/) on [software design](https://web.mit.edu/6.031/www/sp22/classes/06-specifications/). For the bare minimum to work with submitit:
1. Move the code you wish to run on the compute node into a single function (which will ideally contain well designed and documented helper functions). For example, you'd want to turn something like this:
```python
import pandas as pd

df = pd.read_csv("test.csv")
df = df[df["year"] > 2004]
average = df["amount"].mean()
print(average)
```
into a function that is general (hint: if a descriptive name of your function is very long, you may want to make it more general) and return results instead of printing. Do this:
```python
import pandas as pd

def get_mean_amount_after_year(path_to_csv: str, earliest_year: int):
    """ Return mean value of 'amount' column with year > earliest_year """
    df = pd.read_csv(path_to_csv)
    df = df[df["year"] > earliest_year]
    return df["amount"].mean()
```
### Submitit

Submitit eliminates the need to remember complicated and long configurations and allows us to work only in python. The sample program in `main.py` runs a test version. 

1. Add a `if __name__ == "__main__":` block at the end of your python file. No submitit code should exist in your actual function. This way we can easily pivot between submiting jobs with submitit and local exucution. Call your function here. 
2. Create a JSON file with configuration information. Include a "slurm" key that maps to a dictionary with slurm configuration options that start with `slurm_` rather than the `--` you use on the command line. Include a `submitit` key that maps to true when you want to submit the job and false when you want to run it normally (either locally or for debugging). Finally include any arguments to your python function. For example:
```json
{
    "path_to_csv": "test_file.csv",
    "earliest_year": 1994,
    "submitit": true,
    "slurm": {
        "slurm_partition": "general",
        "slurm_job_name": "sample",
        "slurm_nodes": 1,
        "slurm_time": "60:00",
        "slurm_gres": "gpu:1",
        "slurm_mem_per_cpu": 16000
    }
}
```
3. Add argparse. I like to use `argparse` to submit a path to a query that contains both all slurm configuration and a `submitit` key that maps to a boolean. Your file will look something like this:

```python
from pathlib import Path

# your actual code will have more and longer functions than this sample
def get_mean_amount_after_year(path_to_csv: str, earliest_year: int):
    """ Return mean value of 'amount' column with year > earliest_year """
    df = pd.read_csv(path_to_csv)
    df = df[df["year"] > earliest_year]
    return df["amount"].mean()

if __name__ == "__main__":
    import argparse
    import json

    # set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query", help="path to json file containing query", default=None
    )
    args = parser.parse_args()
    
    # read in query
    if Path(args.query).resolve().exists():
        query_path = Path(args.query).resolve()
    else:
        # throw
        raise ValueError(
            f"Could not locate {args.query} in query directory or as absolute path"
        )
    with open(query_path) as f:
        query = json.load(f)
    # save query parameters to variables. if you want a default, better to put
    # at the outermost call to a function.
    path_to_csv = query.get("path_to_csv")
    default_earliest_year = 2005
    earliest_year = query.get("earliest_year", default_earliest_year)

    output_directory = Path("results").resolve()
    executor = submitit.AutoExecutor(folder=output_directory)
    # here we unpack the query dictionary and pull any slurm commands that 
    # are in 'slurm' key. For more info on the ** syntax, see:
    # https://stackoverflow.com/a/36908. The slurm options here are the same
    # as those you use on the command line but instead of prepending with '--'
    # we prepend with 'slurm_'
    executor.update_parameters(**query.get("slurm", {}))

    # if submitit is true in our query json, we'll use submitit
    if query.get("submitit", False):
        executor.submit(
            get_mean_amount_after_year,
            path_to_csv,
            earliest_year,
        )
    else:
        get_mean_amount_after_year(
            path_to_csv,
            earliest_year,
        )
```
Then with a query like this:
you can run `python path/to/script.py --query path/to/query.json` and get your result. 

4. Make sure you save your results in some way! Otherwise your script might run perfectly but be the results will be completely lost. This sample script will compute the mean but not save it anywhere. Save it to a file or log it.
5. Using submitit. IMPORTANT: you run submitit on a login node to submit to a compute node. You can run your python file from the command line. 
6. Debugging submitit. Before you submit a long, multi hour job, test on a smaller dataset interactively. For this you can attach to a compute node, and run your script but with the `submitit` flag in your query json set to false. To debug, use the VS Code debugger. Add command line arguments to the debugger by following [these instructions](https://code.visualstudio.com/docs/python/debugging#_set-configuration-options)