# Slurm and Computing Clusters

Research institutions often have computing clusters that can be used to perform tasks that are too instensive to be run on a typical laptop. Examples are high RAM operations and operations that are much more efficient on GPUs. A computing cluster is a collection of computers (also referred to as nodes, machines, or servers) that you are 'in the cloud' (you are not physically at one of them when using them). You are able to log into the head node (also called login node) with an internet connection using [ssh](https://en.wikipedia.org/wiki/Secure_Shell). If you have an account you can use `ssh username_here@address_of_machine` to connect. You will then have to authenticate by proving you have access with either something only you know (a password) or something only you have (a private key -- see [public key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) if interested). Once you have successfully authenticated you will see your command prompt change (the text at the bottom left of your terminal that looks something like `username@computer:~/filepath` -- this is [fully customizable](https://www.howtogeek.com/307701/how-to-customize-and-colorize-your-bash-prompt/) if interested) to show the username you logged in with at the hostname of the machine's *login node* (or head node) (for the ai or dsi cluster this will be `fe0n` where n is a digit). From here you will have access to your own directory. The login node should just be used for low computation tasks like file management, writing code, and extremely simple programs. Everyone using the cluster will login to the same set of login nodes so if you try to run a complex program, it will slow it down for everyone (and you'll recieve an email asking you to stop). 

Logging in through the command line makes it so all commands you run in that terminal are executed on the remote machine. But command line editors (like vim and emacs) can have a significan learning curve compared to editors like VS Code. For this reason we will use a VS Code extension that allows you to connect your whole VS Code window to the cluster (and utilize all of VS Code's nice features and extensions). Instructions are located below.


Get a [CS Account](https://account-request.cs.uchicago.edu/account/requests) if you don't have one already.

## SSH Keys

It can be annoying / burdensome to type in your passwords constantly to connect to the cluster or push/pull from GitHub. We can switch to authunticating based on *something we have* using ssh keys. 

### Windows Specific Instructions

If you are using Windows 10, you can use OpenSSH like Mac and Linux users. If you use WSL2, please see [specific instructions](#wsl). To ensure it is set up correctly, complete the following (from [this SO answwer](https://stackoverflow.com/a/40720527)):
1. Open Manage optional features from the start menu and make sure you have Open SSH Client in the list. If not, you should be able to add it.
2. Open Services from the start Menu
3. Scroll down to OpenSSH Authentication Agent > right click > properties
4. Change the Startup type from Disabled to any of the other 3 options. I have mine set to Automatic (Delayed Start)
5. Open cmd and type where ssh to confirm that the top listed path is in System32. Mine is installed at C:\Windows\System32\OpenSSH\ssh.exe. If it's not in the list you may need to close and reopen cmd.
6. You should know be able to access OpenSSH tools from the Windows Command Prompt. Continue to General Instructions. 

### General Instructions

#### Create / Manage SSH Keys

1. In the terminal of your local computer (or if on windows, Command Prompt), use `ssh-keygen`, [instructions here](https://www.ssh.com/academy/ssh/keygen). Recommended: use `ssh-keygen -t ecdsa -b 521` or `ssh-keygen -t ed25519` to generate your key. If you have multiple, give it an identifiable name. Otherwise you can click enter to accept the default suggestion. You can optionally add a password to your ssh key. If you do not it may be vulnerable. Adding a password may seem counterintuitive (isn't our whole goal to avoid passwords?), but you can use [ssh-agent](https://www.ssh.com/academy/ssh/agent) and then you will just have to type your password once per session.

2. (assuming you password protect your private key) Add the key to your ssh agent. `ssh-add PATH_TO_KEY`. `PATH_TO_KEY` will start with `~/.ssh/` on Mac/Linux and `C:\Users\YOUR_USERNAME\.ssh\` on Windows. You'll have to type your password in once and it will be saved for a period of time (terminal session or until your computer next reboots), drastically limiting the amount of times you have to type in your password. 

#### Use SSH Keys

3. For a remote machine: To use your private key to log in to a remote machine, it must have access to your public key. To do this you will have to add it to the `~/.ssh/authorized_keys` file on the remote machine. If on Mac/Linux, you can use `ssh-copy-id -i ~/.ssh/KEYNAME_HERE USERNAME@fe01.ds.uchicago.edu`. If on Windows, you'll have to copy your public key, `ssh USERNAME@fe01.ds.uchicago.edu`, and paste it into `~/.ssh/authorized_keys` with `echo PUBLIC_KEY_HERE >> .ssh/authorized_keys`.

4. For GitHub. SSH Keys can also be used for GitHub authentication. You can use the same ssh keys, or follow steps 1-2 again with a new ssh key and name. To give GitHub access to your public keys, go to [GitHub's ssh keys page](https://github.com/settings/keys). Click 'New SSH key'. Give it a name relating to the machine it is storeed on, like "windows laptop", or "linux desktop" and paste in the full contents of the public key. You can access the contents by typing `cat PATH_TO_PUBLIC_KEY` or, on Windows `type PATH_TO_PUBLIC_KEY`.

5. Create / modify your SSH Config. Typing in the full ssh command is now something like `ssh -i PATH_TO_KEY USERNAME@fe01.ds.uchicago.edu` which can be a lot to type and a lot to remember. Using ssh config, we can reduce this to just `ssh fe.ds`. In your `.ssh` file create a `config` file or append the following to the existing file: 
```
Host fe.ds*
  HostName fe01.ds.uchicago.edu
  IdentityFile INSERT_PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User INSERT_YOUR_CNET

Host *.ds !fe.ds
  HostName %h.uchicago.edu
  IdentityFile INSERT_PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User INSERT_YOUR_CNET
  ProxyJump fe.ds
```
This will map `fe.ds` to an ssh command to the listed hostname, with the listed user and private key, and using the listed identity file as your key. `ForwardAgent` set to yes means that any ssh keys added to your local agent will also be added to the remote machines ssh agent (so you can use your local ssh key for GitHub on the cluster, for example). The second block is for connecting directly to compute nodes.


## VS Code

`Remote - SSH` is a VS Code extension that allows you to open a connection to a remote machine in VS Code. Traditionally, one would `ssh` in a terminal and be restriced to command-line text editors like Vim. `Remote - SSH` allows us to act like we are developing on our local machine as normal for the most part and has less of a learning curve.

1. Install `Remote - SSH`. Click 'Extensions' on the menu at the left side of VS Code (its icon is four squares with the top right one pulled away). Search for and install `Remote - SSH`

2. Add useful extensions to always be installed in remote connections. Open the command palette (ctrl+shift+p / command+shift+p / View -> Command Palette...) and search for `Open User Settings`. If it is empty, paste:
```
{
    "remote.SSH.defaultExtensions": [
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-renderers",
        "ms-python.python",
        "ms-python.vscode-pylance"
    ]
}
```
otherwise, make sure to add a comma to the end of the current last item and add the following before the `}`:
```
    "remote.SSH.defaultExtensions": [
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-renderers",
        "ms-python.python",
        "ms-python.vscode-pylance"
    ]
```

2. Follow the instructions [here](https://code.visualstudio.com/docs/remote/ssh) to set up with the following modifications:
    - In "Connect to a remote host", try `Remote-SSH: Connect to Host...` and you should see `fe.ds` as an option. Select it. Otherwise, you can try typing in `fe.ds`.
    - The type of server is Linux.

#### Connecting to a compute node in VS Code

3. Now your VS code window is connected to the login node. If you'd like to connect to a compute node for an interactive session:
    1. In a terminal or command prompt `ssh fe.ds`
    2. Request an interactive session with something like: `srun -p general --gres=gpu:1 --pty --mem 1000 -t 90:00 /bin/bash`. Once you have been your request has been granted, your command prompt will change to something like `USERNAME@hostname` where hostname is probably like `g004`.
    3. Back in VS Code, open the command palette (cntr+shift+p / command+shift+p / View -> Command Palette...), search for `Remote-SSH: Connect to Host...`. Select it and type in as your host `hostname.ds` replacing the hostname with the hostname from step 3.2. 
    4. Your VS Code should now be connected to the compute node. You'll have to open the repository folder (see below instructions for cloning). But now you can take advantage of the computational power from the node and the nice features of VS Code (using notebooks, python debugging, etc.)

## Clone Repository

Go to the repository github page, click the dropdown on the green button that says 'Code', select 'SSH' and copy the value. `git clone COPIED_VALUE` will clone the repo. 

## Conda installation

To install conda:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh
```
You can accept the defaults. Make sure you select yes when it asks to run conda init. This will ensure conda is activated by default. re-open and close your terminal.


Create environment
```bash
conda create --name PROJECT_NAME python=3.9
conda activate PROJECT_NAME
pip install -r requirements.txt
```
Now when you log into ai cluster, just make sure you run `conda activate PROJECT_NAME` and select it as your defualt python for vs code. Click the Python version number on the bottom right and select the interpreter for PROJECT_NAME. If it is not listed, the path is: `/home/USERNAME/miniconda3/envs/PROJECT_NAME/bin/python`.

## Using Slurm and Submitit

### Slurm

We'll use slurm to submit jobs. [Here is uchicago's documentation on slurm](https://howto.cs.uchicago.edu/slurm?s[]=slurm).

The commands to remember are:
- `sinfo` for information about the cluster
- `squeue` for information about currently running or queued jobs
- `srun` to run a job interactively
- `sbatch` to submit a job to the queue (we'll use submitit for this)
- `scancel` to cancel a job. Use `scancel JOB_NUMBER`

We'll use [submitit](https://github.com/facebookincubator/submitit) to actually submit jobs in python.

When we use slurm, we must be respectful to not overuse nodes. Please:
- To test code, submit it to the `dev` queue.
- Don't run computation heavy jobs on the compute nodes. Submit them as jobs
- Do not submit many jobs at once
- To run code you are confident works, submit it to the `general` queue

### Submitit

Submitit eliminates the need to remember complicated and long configurations and allows us to work only in python. The sample program in `main.py` runs a test version. 

The main ideas are:
- Any code you wish to execute together should be runnable by calling a python function. Don't do this: 
```python
import pandas as pd

df = pd.read_csv("test.csv")
df = df[df["year"] > 2004]
average = df["amount"].mean()
print(average)
```
Put the code in a function that is general (hint: if a descriptive name of your function is very long, you may want to make it more general) and return results instead of printing. Do this:
```python
import pandas as pd

def get_mean_amount_after_year(path_to_csv: str, earliest_year: int):
    """ Return mean value of 'amount' column with year > earliest_year """
    df = pd.read_csv(path_to_csv)
    df = df[df["year"] > earliest_year]
    return df["amount"].mean()
```
- Put submitit code in a `if __name__ == "__main__":` block so it is executed when you run the file as a script. No submitit code should exist in your actual function. This way we can easily pivot between cluster and local exucution. I like to use `argparse` to submit a path to a query that contains both all slurm configuration and a `cluster` key that maps to a boolean. 
```python
from pathlib import Path

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

    with executor.batch():
        if query.get("cluster", False):
            job = executor.submit(
                get_mean_amount_after_year,
                path_to_csv,
                earliest_year,
            )
        else:
            average = get_mean_amount_after_year(
                path_to_csv,
                earliest_year,
            )
```
Then with a query like this:
```json
{
    "path_to_csv": "test_file.csv",
    "earliest_year": 1994,
    "cluster": true,
    "slurm": {
        "slurm_array_parallelism": 6,
        "slurm_partition": "general",
        "slurm_job_name": "mbio-all",
        "slurm_nodes": 1,
        "slurm_time": "240:00",
        "slurm_gres": "gpu:1",
        "slurm_mem_per_cpu": 16000
    }
}
```
you can run `python path/to/script.py --query path/to/query.json` and get your result. 

Make sure you save your results in some way! Otherwise your script might run perfectly but be the results will be completely lost.

## Appendix
### WSL

Using WSL2 on Windows is a great way to have access to a linux system on a Windows OS. The convience of 'pretending' to have two separate operating systems on one, however, can lead to complications. One is with SSH keys. The `.ssh` directory used on your normal Windows system and your WSL will be different from each other. This is fine in most cases, but can lead to headaches when using VS Code. If you wish to connect to a remote SSH machine in VS code, it will use your Windows configuration. So even if you only use WSL2 and the VS Code extension (WSL) to code in WSL2, you must follw the [Windows ssh instructions](#windows-specific-instructions). If you wish use the same keys on each system, you can copy them. See [this article](https://devblogs.microsoft.com/commandline/sharing-ssh-keys-between-windows-and-wsl-2/) for more information.