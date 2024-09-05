# Slurm and Computing Clusters

## Using this Document

This document is written specifically to introduce students to the slurm cluster at the DSI at the University of Chicago. It is general enough, however, that many parts should be useful for even experienced slurm users and general remote computing. If a part is unclear or you have additional tips, please open an issue or pull request! 

Please read all portions carefully and only skip if you really know what you are doing. If you come across an issue, check that it isn't addressed in [Troubleshooting](#troubleshooting) before asking. 

## Background

Research institutions often have computing clusters that can be used to perform tasks that are too instensive to be run on a typical laptop. Examples are high RAM operations and operations that are much more efficient on GPUs. A computing cluster is a collection of computers (also referred to as nodes, machines, or servers) that you are 'in the cloud' (you are not physically at one of them when using them). You are able to log into the head node (also called login node) with an internet connection using [ssh](https://en.wikipedia.org/wiki/Secure_Shell). If you have an account you can use `ssh username_here@address_of_machine` to connect. You will then have to authenticate by proving you have access with either something only you know (a password) or something only you have (a private key -- see [public key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) if interested). Once you have successfully authenticated you will see your command prompt change (the text at the bottom left of your terminal that looks something like `username@computer:~/filepath` -- this is [fully customizable](https://www.howtogeek.com/307701/how-to-customize-and-colorize-your-bash-prompt/) if interested) to show the username you logged in with at the hostname of the machine's *login node* (or head node) (for the ai or dsi cluster this will be `fe0n` where n is a digit). From here you will have access to your own directory. The login node should just be used for low computation tasks like file management, writing code, and extremely simple programs. Everyone using the cluster will login to the same set of login nodes so if you try to run a complex program, it will slow it down for everyone (and you'll recieve an email asking you to stop). 

Logging in through the command line makes it so all commands you run in that terminal are executed on the remote machine. But command line editors (like vim and emacs) can have a significan learning curve compared to editors like VS Code. For this reason we will use a VS Code extension that allows you to connect your whole VS Code window to the cluster (and utilize all of VS Code's nice features and extensions). Instructions are located below.

## Table of Contents

- [Slurm and Computing Clusters](#slurm-and-computing-clusters)
  - [Using this Document](#using-this-document)
  - [Background](#background)
  - [Table of Contents](#table-of-contents)
  - [Part I: Prerequisites](#part-i-prerequisites)
  - [Part II: Set up SSH](#part-ii-set-up-ssh)
    - [\[Windows Users Only\] Step 1: Enable OpenSSH](#windows-users-only-step-1-enable-openssh)
    - [Step 2: Create / Manage SSH Keys](#step-2-create--manage-ssh-keys)
    - [Step 3: Save SSH Configuration](#step-3-save-ssh-configuration)
    - [Step 4: Enable Authentication with SSH Keys](#step-4-enable-authentication-with-ssh-keys)
      - [Mac/Linux Instructions for Remote Authentication](#maclinux-instructions-for-remote-authentication)
      - [Windows Instructions for Remote Authentication](#windows-instructions-for-remote-authentication)
  - [Part III: Slurm and cluster basics](#part-iii-slurm-and-cluster-basics)
    - [Step 1: Connecting to the Cluster](#step-1-connecting-to-the-cluster)
    - [Step 2: Using Slurm](#step-2-using-slurm)
  - [Part IV: Clone your repository on the cluster](#part-iv-clone-your-repository-on-the-cluster)
  - [Part V: Set up VS Code](#part-v-set-up-vs-code)
    - [Step 1: Connect to the Login Node with VS Code](#step-1-connect-to-the-login-node-with-vs-code)
    - [Step 2: Connect to a Compute Node with VS Code](#step-2-connect-to-a-compute-node-with-vs-code)
  - [Part VI: Install Conda for Environment Management](#part-vi-install-conda-for-environment-management)
  - [Part VII: Using Submitit for Long Jobs](#part-vii-using-submitit-for-long-jobs)
    - [Step 1: Slurm Review](#step-1-slurm-review)
    - [Step 2: Background](#step-2-background)
    - [Step 3: Preparing Your Code](#step-3-preparing-your-code)
    - [Step 4: Submitit](#step-4-submitit)
  - [Troubleshooting](#troubleshooting)
    - [Common Errors](#common-errors)
    - [Troubleshooting Tests](#troubleshooting-tests)
  - [Appendix](#appendix)
    - [WSL](#wsl)

## Part I: Prerequisites

This guide is specifically tailored to the University of Chicago DSI Cluster, though it should be generally applicable to most slurm clusters. The guide assumes you have:

- A CNET id
- A CS Account. Get [one here](https://account-request.cs.uchicago.edu/account/requests) if you don't have one already.
- (for Part 3 onward) Access to a slurm partition. To request, send an email to techstaff@cs.uchicago.edu asking for access to compute nodes on the DSI cluster and cc your mentor (if relevant)
- A reasonably up to date and functioning computer running on Windows (10/11), Mac (10.13+/High Sierra+), or Linux. 
- An internet connection. You'll need internet to use ssh.
- VS Code
- A GitHub account

## Part II: Set up SSH

It can be annoying / burdensome to type in your passwords constantly to connect to the cluster or push/pull from GitHub. We can switch to authenticating based on *something we have* using ssh keys. 

### [Windows Users Only] Step 1: Enable OpenSSH

If you are using Windows 10 or 11, you can use OpenSSH like Mac and Linux users. If you use WSL2, please see [specific instructions](#wsl). <!-- markdown-link-check-disable -->To ensure it is set up correctly, complete the following (from [this SO answwer](https://stackoverflow.com/a/40720527)):<!-- markdown-link-check-enable -->
1. Open Manage optional features from the start menu and make sure you have Open SSH Client in the list. If not, you should be able to add it.
2. Open Services from the start Menu
3. Scroll down to OpenSSH Authentication Agent > right click > properties
4. Change the Startup type from Disabled to any of the other 3 options. I have mine set to Automatic (Delayed Start)
5. Open cmd and type where ssh to confirm that the top listed path is in System32. Mine is installed at C:\Windows\System32\OpenSSH\ssh.exe. If it's not in the list you may need to close and reopen cmd.
6. You should know be able to access OpenSSH tools from the Windows Command Prompt. Continue to General Instructions. 


### Step 2: Create / Manage SSH Keys

1. In the terminal of your local computer (or if on windows, Command Prompt), use `ssh-keygen`, [instructions here](https://www.ssh.com/academy/ssh/keygen). Recommended: use `ssh-keygen -t ecdsa -b 521` or `ssh-keygen -t ed25519` to generate your key. 
2. If you have multiple keys, give it an identifiable name but keep it in the `.ssh` directory. Otherwise you can click enter to accept the default suggestion. 
3. You can optionally add a password to your ssh key. If you do not it may be vulnerable. Adding a password may seem counterintuitive (isn't our whole goal to avoid passwords?), but you can use [ssh-agent](https://www.ssh.com/academy/ssh/agent) (explained below) and then you will just have to type your password once per session (or once ever). As you type the password in, no text will appear on screen to keep your password length private from shoulder surfers. You will be asked to repeat it. Do not forget your password! Write it down, or ideally store it in a password manager. A `KEYNAME` and `KEYNAME.pub` file will be created by this command. The file with the `.pub` extension is your public key and can be shared safely. The file with no extension is your private key and should never be shared. 
4. (assuming you password protect your private key) Add the *private* key to your ssh agent. `ssh-add PATH_TO_KEY`. `PATH_TO_KEY` will start with `~/.ssh/` on Mac/Linux and `C:\Users\YOUR_USERNAME\.ssh\` on Windows. You'll have to type your password in once and it will be saved for a period of time (terminal session or until your computer next reboots), drastically limiting the amount of times you have to type in your password. 
5. <!-- markdown-link-check-disable -->[Mac Users Only] (optional) To keep the key in your ssh-agent accross sessions, follow [this stack overflow answer](https://stackoverflow.com/questions/18880024/start-ssh-agent-on-login). <!-- markdown-link-check-enable --> 
6. Confirm your key was added. In your terminal/command prompt/powershell, run `ssh-add -l` to list all keys in your ssh agent. Your key should appear here. If this command returns `The agent has no identities.`, step 4 failed. 

### Step 3: Save SSH Configuration

1. Create / modify your SSH Config. Typing in the full ssh command is now something like `ssh -i PATH_TO_KEY USERNAME@fe01.ds.uchicago.edu` which can be a lot to type and a lot to remember. Using ssh config, we can reduce this to just `ssh fe.ds`. In your `.ssh` directory create a `config` file if one does not exist. To open:
    - [Windows] In command prompt: `code C:\Users\USERNAME\.ssh\config` where `USERNAME` is your windows username. 
    - [Mac] In a terminal: `touch ~/.ssh/config` to create the file if it does not exist and `open ~/.ssh/config` to open it.
    - [Linux] In a terminal: `code ~/.ssh/config`
2. You may or may not already have configurations saved. Place this text in the config file, after any other configurations, *except* any block that starts with `Host *` or `Host fe01.ds.uchicago.edu`:
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
Replace `INSERT_YOUR_CNET` with your CNET ID and `INSERT_PATH_TO_PRIVATE_KEY` with the path the key you previously created. This will map `fe.ds` to an ssh command to the listed hostname, with the listed user and private key, and using the listed identity file as your key. `ForwardAgent` set to yes means that any ssh keys added to your local agent will also be added to the remote machines ssh agent (so you can use your local ssh key for GitHub on the cluster, for example). The second block is for connecting directly to compute nodes.

3. Save and close the file.


### Step 4: Enable Authentication with SSH Keys

For a private key to work for authenticating, the service you are authenticating with must have access to your public key. We will set this up for github and the cluster.

1. Print your public key:
    - [Windows] In command prompt: `type C:\Users\USERNAME\.ssh\KEYNAME` where `USERNAME` is your Windows username and `KEYNAME` is the key your created. 
    - [Mac/Linux] In a terminal: `cat ~/.ssh/KEYNAME.pub` where `KEYNAME` is the key you created. 
2. Copy your public key. Highlight and copy *the entire output*. `ctrl+c` may not work in terminal. `ctrl+shift+c` or right click may work. 
3. Add public key to GitHub. To give GitHub access to your public keys, go to [GitHub's ssh keys page](https://github.com/settings/keys). 
4. Click 'New SSH key'. Give it a name relating to the machine it is storeed on, like "windows laptop", or "linux desktop" and paste in the full contents of the public key.
5. Verify your key was added. In terminal / command prompt, try `ssh git@github.com` it should respond with `Hi GITHUB_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.` or something similar. 

#### Mac/Linux Instructions for Remote Authentication
1. If on Mac/Linux, you can use `ssh-copy-id -i ~/.ssh/KEYNAME_HERE.pub fe.ds`, replacing `KEYNAME_HERE` with the name of the public ssh key you would like to use (it should end with .pub). 
2. You will be prompted for `USERNAME@fe01.ds.uchicago.edu`'s password. This will be your CNET password. 
3. To verify success: In your terminal, `ssh fe.ds` should connect you to the cluster without typing any password.

#### Windows Instructions for Remote Authentication
1. Copy your public key. Follow [Step 4: Enable Authentication with SSH Keys](#step-4-enable-authentication-with-ssh-keys) steps 1 and 2 again.  
2. Now connect to the server. Do `ssh fe.ds`. You'll have to type in your UChicago password. Your command prompt is now attached to the login node. The bottom left of your screen should say something like `USERNAME@fe01:~$`. 
3. Ensure there is an `.ssh` directory. Run `mkdir .ssh`. 
4. Add your public key to the list of authorized keys. Run `echo "PUBLIC_KEY_HERE" >> .ssh/authorized_keys`, replacing `PUBLIC_KEY_HERE` with the copied public key and maintaining the quotations. ctrl+v may not paste in your terminal. Try right clicking, ctrl+shift+v, and shift+insert. 
5. Type `exit` to exit the cluster and return to your windows command prompt.
6. To verify success: In your command prompt, `ssh fe.ds` should connect you to the cluster without typing any password.

## Part III: Slurm and cluster basics

You can now successfully and easily connect to the cluster in your terminal! Congratulations, this is not a trivial task. Lets run through some cluster and Slurm basics. 

### Step 1: Connecting to the Cluster

Before starting this, make sure that you are familiar with using a Unix command line. You can find some information [here](./command-line.md).

1. Connect to the cluster using `ssh fe.ds`.
    * If this works you should see a change in your command prompt. If there are any notifications or messages from `ssh` this probably means that you did not connect.
2. Verify that you are in your _home_ directory using the `pwd` command. Running this command should return `/home/USERNAME` where `USERNAME` is your CNET ID.
3. Understand where data should be place:
    * Home directories are limited to 20 GB of storage. 
    * Home directories are only accessible by you, so they should be not be used for any data that needs to be shared with anyone else
    * The directory `/net/projects` shows _shared_ project directories. These are limited access and you need to contact techstaff if you do not have access to a directory required for a project. Unix user groups are used to manage access. This is the primary location where data should be placed.
    * The directory `/net/scratch` and `/net/scratch2` are open areas where anyone can put anything. Note that this is _ephemeral_. Any data put here may be deleted at any time. 
    * All of the `/net` directories are network storage drives and are available on any node in the cluster.
4. Understand the language of the cluster:
    * **Cluster:** A collection of connected computers which are set up in to share resources (compute, hard drive and memory) so they behave as a single system.
    * **Nodes:** A node is a single computer within the cluster.
    * * **Login Nodes:** A node designed to manage logins, no computing jobs should be run on them. In the DSI cluster these nodes begin with `fe`.
    * **Compute Nodes:** A node which was created for high-performance computing. They have powerful GPUs, CPUs and lots of memory. On the DSI cluster there are multiple designations, such as `g, h, i, j, k, l` and `m`. Nodes with matching prefixes have similar hardware.

### Step 2: Using Slurm

When you want to run an intensive job, use a compute node. These are powerful computers with GPUs, powerful CPUs, and/or lots of memory. In order to fairly share them among all users, Slurm manages a queue system. Users submit requests of what resources they need and when they become available, Slurm grants access. 

**Important:** Before using Slurm on the cluster, please read over the documentation [here](./slurm_commands.md).

Additional reference information about UChicago's Slurm set up can be found at the [UChicago CS Slurm How To Page](https://howto.cs.uchicago.edu/slurm?s[]=slurm).

## Part IV: Clone your repository on the cluster

1. Note that if you have a private git repository you will need to [create an ssh key](#part-ii-set-up-ssh) on the cluster and add those keys to github. Since you are connecting from the environment of the cluster to github you will need to establish your cluster account with github.
2. Connect to the login node. `ssh fe.ds`
3. Verify your current working directory by typing `pwd` and checking to make sure it says `\home\CNET ID`. If this is not your current working directory type in `cd ` to return to your home directory.
4. Go to the repository github page, click the dropdown on the green button that says 'Code', select 'SSH' and copy the value.
1. Type in `git clone COPIED_VALUE` to clone the repo to your home directory. Verify that there were no errors printed and that the repo was properly cloned.

## Part V: Set up VS Code

The instructions below provide specific instructions for setting up [VS Code](https://code.visualstudio.com/). Before preceding, please make sure that it is installed.

### Step 1: Connect to the Login Node with VS Code

Traditionally, one would `ssh` in a terminal and be restricted to command-line text editors like Vim. We can use the extension, `Remote - SSH` allows us to act like we are developing on our local machine as normal for the most part and has less of a learning curve. Information on the extension can be found [here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh).

1. Install `Remote - SSH`. Click 'Extensions' on the menu at the left side of VS Code (its icon is four squares with the top right one pulled away). Search for and install `Remote - SSH`. 

2. We want to allow common extensions to be used on the cluster. Open the command palette (ctrl+shift+p / command+shift+p / View -> Command Palette...) and search for `Open User Settings (JSON)`. If it is empty, paste the following:
3. 
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

Otherwise, make sure to add a comma to the end of the current last item and add the following before the `}`:

```
    "remote.SSH.defaultExtensions": [
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-renderers",
        "ms-python.python",
        "ms-python.vscode-pylance"
    ]
```

1. Follow the instructions [here](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) to set up with the following modifications: 
    - In "Connect to a remote host", try `Remote-SSH: Connect to Host...` and you should see `fe.ds` as an option. Select it. Otherwise, you can try typing in `fe.ds`.
    - (If you are asked, though sometimes this will be detected by VS Code) The type of server is Linux.
2. The (usually green) box at the bottom left of your VS Code window should now say `SSH: fe.ds` to signify you are using the SSH extension and connected to the host `fe.ds` as in the image here:

<div align="center">
  <img src="SSHConnection.png" width="600" style="border: 2px solid black;">
</div>

3. Assuming you have correctly [cloned the repo on the cluster](#part-iv-clone-your-repository-on-the-cluster) you can you click `File` then `Open Folder` and select your repository folder. 
4. Close the window. Now if you open a new VS Code window and select from recent, the one called `REPOSITORY_NAME [SSH: fe.ds] will take you right to the login node of the cluster with your previous configuration. 

### Step 2: Connect to a Compute Node with VS Code

1. Open a terminal / command prompt. Connect to the cluster using `ssh fe.ds`.
2. You should now be connected to the cluster in a **login** node, which is fine for small tasks and coding. To get access to a powerful compute node, you must request access through Slurm. Request an interactive session with a command like: `srun -p general --gres=gpu:1 --pty --mem 1000 -t 90:00 /bin/bash`. Once you have been your request has been granted, your command prompt will change to something like `USERNAME@hostname` where hostname is probably like `g004`.
3. Now your terminal is connected to a compute node. (NOTE: If you did this in a terminal in VS code, just that terminal will connect to a compute node. The rest of VS Code functionality will be run on the login node still. To connect VS code features like python debug and notebook editing to the compute node follow along).
4. Back in VS Code, open the command palette (ctrl+shift+p / command+shift+p / View -> Command Palette...), search for `Remote-SSH: Connect to Host...`. Select it and type in as your host `HOSTNAME.ds` replacing the `HOSTNAME` with the hostname from above. 
4. Your VS Code should now be connected to the compute node. To verify the  You'll have to open the repository folder (see below instructions for cloning). But now you can take advantage of the computational power from the node and the nice features of VS Code (using notebooks, python debugging, etc.)


## Part VI: Install Conda for Environment Management

1. Connect to cluster
2. In a terminal on the cluster:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh
```
You can accept the defaults. Make sure you select yes when it asks to run conda init. This will ensure conda is activated by default. re-open and close your terminal.

3. Create a new environment
```bash
conda create --name PROJECT_NAME python=3.11
conda activate PROJECT_NAME
pip install -r requirements.txt
```
Where `PROJECT_NAME` is the name of the project you are working on. Now when you log into ai cluster, just make sure you run `conda activate PROJECT_NAME`.

4. Ensure VS Code uses the correct python environment. When a python file is open and selected, click the Python version number on the bottom right and select the interpreter for PROJECT_NAME. If it is not listed, the path is: `/home/USERNAME/miniconda3/envs/PROJECT_NAME/bin/python` where `USERNAME` is your CNET ID. 

5. Ensure VS Code uses the correct kernel for Jupyter notebooks. First, install `ipykernel` in the `PROJECT_NAME` environment:
```bash
conda install -n PROJECT_NAME ipykernel --update-deps --force-reinstall
```
With a Jupyter notebook open, click the Python version number in the upper right and select the kernel for `PROJECT_NAME`. You may need to refresh the list of available kernels using the icon in the upper right of the menu.

6. You should now be at a point where you can easily connect to the cluster with VS Code, use jupyter notebooks, and attach to compute nodes for more intensive jobs. This is enough for a lot of tasks, but if you become bothered by long running jobs crashing due to internet connection outages or running out of time on the compute node, please continue to using submitit. 

## Part VII: Using Submitit for Long Jobs

### Step 1: Slurm Review

The commands to remember are:
- `sinfo` for information about the cluster
- `squeue` for information about currently running or queued jobs
- `srun` to run a job interactively
- `sbatch` to submit a job to the queue (we'll use submitit for this)
- `scancel` to cancel a job. Use `scancel JOB_NUMBER`

We'll use [submitit](https://github.com/facebookincubator/submitit) to actually submit jobs in python.

When we use slurm, we must be respectful to not overuse nodes. Please:
- To test code, submit it to the `dev` queue or test them with less data in an interactive session
- Don't run computation heavy jobs on the login nodes. Submit them as jobs
- Do not submit many jobs at once
- To run code you are confident works, submit it to the `general` queue


### Step 2: Background

To understand how we use submitit, some background knowledge will be useful:
1. `if __name__ == "__main__":` blocks. The code under these blocks will run when the file is run as a script and not when it is imported as a module. For more information, see [this](https://realpython.com/if-name-main-python/)
2. Command Line Arguments. When you run something as a script, adding command line arguments can allow you to modify arguments without going into your python code. We'll use a package called argparse to convert command line arguments into easily parsable python objects. For more information, see [this tutorial](https://realpython.com/python-command-line-arguments/) and [argparse documentation](https://docs.python.org/3/library/argparse.html)
3. JSON. We'll use the json file format to store configuration. This is basically like a python dictionary. 

### Step 3: Preparing Your Code

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
### Step 4: Submitit

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

## Troubleshooting

There are a lot of steps here and its easy to miss something or discover a gap in the docs. Here are some common errors, and troubleshooting steps you can take. 

### Common Errors

Error:  `srun: error: Unable to allocate resources: Invalid account or account/partition combination specified`
<br>Cause: You do not have permission to use the partition you requested from. 
<br>Solution: Most likely you need to email techstaff@cs.uchicago.edu requesting access to compute nodes. Otherwise check that you are requesting the correct partition (currently there is only `dev` and `general`. The default if unspecified is the `dev` partition).

Error: `CUDA out of memory`
<br>Cause: The GPU you were using ran out of RAM.
<br>Solution: Could be difficult to solve completely, but there are few things that usually work:
 - Easy: Simple refactoring. Use less GPU by reducing batch sizes, for example. 
 - Medium: Try using another GPU with more memory. To see GPU's available, run `sinfo -o %G`. You can look up the models online. You can request a specific GPU with the `--gres=gpu:GPU_NAME:1` flag where `GPU_NAME` is the type of gpu (like `a40`)
 - Hard: Major refactoring of your code to use less memory.

Error: `Killed` or `Out of Memory` on compute node
<br>Cause: Most likely, you ran out of CPU memory
<br>Solution: Request more memory! Use the `--mem` flag on `srun`

Error: `Disk quota exceeded`
<br>Symptom: VS code fails to connect to login node
<br>Cause: Each home directory has a quota of disk storage space (~50 GB) and you are above it.
<br>Solution: You need to move or delete some files. If you are working on a project with a `/net/projects/` directory, move any data files or checkpoints into that directory (and update your code accordingly!). To check you disk usage, run `du -sh ~`

Error: `git@github.com: Permission denied (publickey). fatal: Could not read from remote repository.`
<br>Cause: GitHub can not access a private key that matches the public key stored on GitHub.
<br>Solution: If you are on the cluster, make sure that you are forwarding your ssh agent. `ssh-add -l` should return the appropriate key. If no identities are found, your ssh-agent has no identities or is not being forwarded. If `ssh-add -l` locally also returns no identities, you must run `ssh-add PATH_TO_KEY` as specified in Part II, [Step 2](#step-2-create--manage-ssh-keys). If the correct identity is found locally, make sure your ssh config matches the one in this document. Finally make sure you have added the appropriate public key to your GitHub account.

### Troubleshooting Tests

Whenever an error comes up, think about all the potential points of failure. Then try to isolate each and see if they work on their own. For example if you are trying to connect to a compute node with VS code using the steps in these instructions, potential points of failure are: VS Code `Remote - SSH` extension, VS Code, your internet connection, ssh config file, ssh keys, slurm, the cluster. Below find some methods to check if different components are working correctly.

Test: run `ssh fe.ds` locally
<br>Expected Result: successful connection to login node.

Test: run `ssh -v fe.ds` locally for verbose output (add up to 3 v's for more verbosity). 
<br>Expected Result: Close to the start, you should see something like: 
```
debug1: Reading configuration data /home/USERNAME/.ssh/config
debug1: /home/USERNAME/.ssh/config line 20: Applying options for fe.ds*
debug1: /home/USERNAME/.ssh/config line 26: Skipping Host block because of negated match for fe.ds
```
where `USERNAME` is your username on your computer. Check that the path after `Reading configuration data` is to the config file you expect and that the right Host blocks are being used. Further down you should see something like: 
```
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering public key: /home/USERNAME/.ssh/id_ed25519 ED25519 SHA256:asdkfh298r9283hkdsjfn23rhdf9284 explicit agent
debug1: Server accepts key: /home/USERNAME/.ssh/id_ed25519 ED25519 SHA256:a;sldfkj2oiefjowihoweflkdfjslfkjksld0923 explicit agent
debug1: Authentication succeeded (publickey).
```

Test: run `ssh-add -l` locally
<br>Expected Result: You should see something like `256 SHA256:<a bunch of characters> USERNAME@HOSTNAME (KEY_TYPE)`. If you see `The agent has no identities`, you must `ssh-add PATH_TO_KEY`.

Test: run `ssh-add -l` on a login node
<br>Expected Result: You should see something like `256 SHA256:<a bunch of characters> USERNAME@HOSTNAME (KEY_TYPE)`. If you see `The agent has no identities`, you must `ssh-add PATH_TO_KEY`.

Test: run `ssh git@github.com` locally and on a login node to test GitHub ssh keys
<br>Expected Result: `Hi GITHUB_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.`

Test: request compute node and `ssh COMPUTE_NODE.ds` where `COMPUTE_NODE` is the node name (like `g004`)
<br>Expected Result: connection to the compute node

## Appendix
### WSL

Using WSL2 on Windows is a great way to have access to a linux system on a Windows OS. The convience of 'pretending' to have two separate operating systems on one, however, can lead to complications. One is with SSH keys. The `.ssh` directory used on your normal Windows system and your WSL will be different from each other. This is fine in most cases, but can lead to headaches when using VS Code. If you wish to connect to a remote SSH machine in VS code, it will use your Windows configuration. So even if you only use WSL2 and the VS Code extension (WSL) to code in WSL2, you must follw the [Windows ssh instructions](#windows-specific-instructions). If you wish use the same keys on each system, you can copy them. See [this article](https://devblogs.microsoft.com/commandline/sharing-ssh-keys-between-windows-and-wsl-2/) for more information.
