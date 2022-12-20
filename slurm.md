## Slurm and Computing Clusters

Research institutions often have computing clusters that can be used to perform tasks that are too instensive to be on a typical laptop. Examples are high RAM operations and operations that are much more efficient on GPUs. A computing cluster is a collection of powerful computers or 'nodes' that can be utilized by many people. Users can access the cluster by logging in over [ssh](https://en.wikipedia.org/wiki/Secure_Shell). In the cluster they will have their own private directory for file storage. There are two main types of nodes to be aware of: 
 - login nodes: 

A computing cluster is a collection of computers (also referred to as nodes, machines, or servers) that you are 'in the cloud' (you are not physically at one of them when using them). You are able to log into the head node (also called login node) with an internet connection using [ssh](https://en.wikipedia.org/wiki/Secure_Shell). If you have an account you can use `ssh username_here@address_of_machine` to connect. You will then have to authenticate by proving you have access with either something only you know (a password) or something only you have (a private key -- see [public key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) if interested). Once you have successfully authenticated you will see your command prompt change (the text at the bottom left of your terminal that looks something like `username@computer:~/filepath` -- this is [fully customizable](https://www.howtogeek.com/307701/how-to-customize-and-colorize-your-bash-prompt/) if interested) to show the username you logged in with at the hostname of the machine's login node (for ai cluster this will be `fe0n` where n is a digit). From here you will have access to your own directory. The login node should just be used for low computation tasks like file management, writing code, and extremely simple programs. Everyone using the cluster will login to the same set of login nodes so if you try to run a complex program, it will slow it down for everyone. 

Logging in through the command line makes it so all commands you run in that terminal are executed on the remote machine. But command line editors (like vim and emacs) can have a significan learning curve compared to editors like VS Code. For this reason we will use a VS Code extension that allows you to connect your whole VS Code window to the cluster (and utilize all of VS Code's nice features and extensions). Instructions are located below.

To run complicated, compute or memory intensive programs, you must use a compute node. Compute nodes are valuable so their access is managed by Slurm. Queues / Partitions exist that each have different resources available. Users can request to use resources from a particular partition and slurm will put your request in line until it is available (often right away). There are two ways to request resources: batch jobs and interactive jobs. Batch jobs should be used for long running and well tested programs. For these you specify what commands should be run and submit it to the partition. Whenever it gets scheduled it will run even if you log out or turn off your computer. For batch jobs we will use a tool called submitit. Interactive jobs are useful for exploration and debugging. For these you can use the `srun` command. The general format is `srun -p PARTITION_NAME --gres=gpu:1 --pty --mem RAM_IN_MEGABYTES -t TIME /bin/bash` and a good starting version is: `srun -p cdac-contrib --gres=gpu:1 --pty --mem 1000 -t 90:00 /bin/bash`. We will use special instructions below to connect VS Code to the compute node and not just the login node. 

### Getting access

Get a [CS Account](https://account-request.cs.uchicago.edu/account/requests) if you don't have one already. Next steps are obsolete. 

### SSH Keys

It can be annoying / burdensome to type in your passwords constantly to connect to the cluster or push/pull from GitHub. We can switch to authorized based on *something we have* using ssh keys. 

1. In the terminal of your local computer (or WSL if on windows), use `ssh-keygen`, [instructions here](https://www.ssh.com/academy/ssh/keygen). Recommended: use `ssh-keygen -t ecdsa -b 521` or `ssh-keygen -t ed25519` to generate your key. If you have multiple, give it an identifiable name. Otherwise you can click enter to accept the default suggestion. You can optionally add a password to your ssh key. If you do not it may be vulnerable. Adding a password may seem counterintuitive (isn't our whole goal to avoid passwords?), but you can use [ssh-agent](https://www.ssh.com/academy/ssh/agent) and then you will just have to type your password once per session.

2. Add your key to your `authorized_keys` in the cluster: locally, `ssh-copy-id -i ~/.ssh/KEYNAME_HERE USERNAME@fe.ai.cs.uchicago.edu`

3. Now, `ssh -i ~/.ssh/KEYNAME_HERE USERNAME@fe.ai.cs.uchicago.edu` should connect without having to type your uchicago password, just your key's passphrase, if any. 

4. SSH keys are useful for github too. You can add them both locally and on the cluster following these instructions:

    1. Open a terminal
    2. Create SSH keys. This will allow you to use them to interact with the remote repository without logging in.
    - use `ssh-keygen` as before or reuse the same key
    - To use the default filename, hit enter
    - hit enter to use no password, or type a password
    3. Upload keys to github
    - Go to [github to upload you ssh keys](https://github.com/settings/keys)
    - back in your terminal `cat ~/.ssh/KEYNAME.pub` (or if you used a different path place it here). Copy the output
    - Click 'New SSH key'. Give it a name like `ai cluster` if on the ai cluster or `laptop` and paste in the full output to the `cat` command

### SSH Config

It can be annoying / tiring to continually remember addresses. We can use a file called `~/.ssh/config` to give aliases to these addresses and switch to using private-public key encryption instead of using passwords. 

Add the following to your `~/.ssh/config` replacing username with your username:
```
Host fe.ai*
   HostName fe.ai.cs.uchicago.edu
   User username
   IdentityFile ~/.ssh/CHANGE_TO_YOUR_KEY

Host *.ai !fe.ai
   HostName %h.cs.uchicago.edu
   User username
   IdentityFile ~/.ssh/CHANGE_TO_YOUR_KEY
   ProxyJump fe.ai
```

If you are using WSL, please note: VS Code struggles accessing your WSL config. You may have to place this at the end of your `/mnt/c/Users/WINDOWS_USERNAME/.ssh/config` and copy your keys there / generate new ones. 

### VS Code

`Remote - SSH` is a VS Code extension that allows you to open a connection to a remote machine in VS Code. Traditionally, one would `ssh` in a terminal and be restriced to command-line text editors like Vim. `Remote - SSH` allows us to act like we are developing on our local machine as normal for the most part and has less of a learning curve.

1. Install `Remote - SSH`. Click 'Extensions' on the menu at the left side of VS Code (its icon is four squares with the top right one pulled away). Search for and install `Remote - SSH`

2. Follow the instructions [here](https://code.visualstudio.com/docs/remote/ssh) to set up with the following modifications:

- In "Connect to a remote host", try `Remote-SSH: Connect to Host...` and you should see `fe.ai` as an option. Select it.
- The type of server is Linux.

3. Now your VS code window is connected to the login node. If you'd like to connect to a compute node for an interactive session:
    1. In a terminal, `ssh fe.ai`
    2. Request an interactive session with something like: `srun -p cdac-contrib --gres=gpu:1 --pty --mem 1000 -t 90:00 /bin/bash`. Once you have been your request has been granted, your command prompt will change to `USERNAME@a00n` where `n` is a digit. 
    3. Back in VS Code, open the command palette (cntr+shift+p / command+shift+p / View -> Command Palette...), search for `Remote-SSH: Connect to Host...`. Select it and type in as your host `a00n.ai` replacing the n with the digit from step 3.2. 
    4. Your VS Code should now be connected to the compute node. You'll have to open the repository folder (see below instructions for cloning). But now you can take advantage of the computational power from the node and the nice features of VS Code (using notebooks, python debugging, etc.)

### Clone Repository

Go to the repository github page, click the dropdown on the green button that says 'Code', select 'SSH' and copy the value. `git clone COPIED_VALUE` will clone the repo. 

### Conda installation

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

### Using Slurm

We'll use slurm to submit jobs. [Here is uchicago's documentation on slurm](https://howto.cs.uchicago.edu/slurm?s[]=slurm).

The commands to remember are:

`cs-squeue`, `squeue`


We'll use [submitit](https://github.com/facebookincubator/submitit) to actually submit jobs in python.

When we use slurm, we must be respectful to not overuse nodes. Please:
- To test code, submit it to the `dev` queue.
- Don't run computation heavy jobs on the compute nodes. Submit them as jobs
- Do not submit many jobs at once
- To run code you are confident works, submit it to the `cdac-contrib` queue
