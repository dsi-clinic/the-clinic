# Troubleshooting Common Errors

If you are having an error or issue come up, please search for it here before consulting a mentor or TA. This document contains sections for troubleshooting multiple tools because it can sometimes be hard to diagnose which tool is causing an error. 

This document has sections for different tools used in the DSI clinic. Each one has subsections for common errors (for when there is a specific failure and often a specific error message), tips and guides (for when there is something is annoying or seems to be failing but without any error message), and troubleshooting (for when the reason for failure is unclear after looking through the other sections). 

## Table of Contents

- [Cluster](#cluster)
    - [Common Errors](#common-errors)
    - [Tips and Guides](#guides-and-tips)
    - [Troubleshooting](#troubleshooting-cluster)
- [WSL](#wsl)
    - [Tips and Guides](#guides-and-tips-1)
    - [Troubleshooting](#troubleshooting-wsl)





## Cluster

### Common Errors

#### Error:  `srun: error: Unable to allocate resources: Invalid account or account/partition combination specified`
Cause: You do not have permission to use the partition you requested from. 
<br>Solution: Most likely you need to email techstaff@cs.uchicago.edu requesting access to compute nodes. Otherwise check that you are requesting the correct partition (currently there is only `dev` and `general`. The default if unspecified is the `dev` partition).

#### Error: `CUDA out of memory`
Cause: The GPU you were using ran out of RAM.
<br>Solution: Could be difficult to solve completely, but there are few things that usually work:
 - Easy: Simple refactoring. Use less GPU by reducing batch sizes, for example. 
 - Medium: Try using another GPU with more memory. To see GPU's available, run `sinfo -o %G`. You can look up the models online. You can request a specific GPU with the `--gres=gpu:GPU_NAME:1` flag where `GPU_NAME` is the type of gpu (like `a40`)
 - Hard: Major refactoring of your code to use less memory.

#### Error: `Killed` or `Out of Memory` on compute node
Cause: Most likely, you ran out of CPU memory
<br>Solution: Request more memory! Use the `--mem` flag on `srun`

#### Error: `Disk quota exceeded`
Symptom: VS code fails to connect to login node
<br>Cause: Each home directory has a quota of disk storage space (~50 GB) and you are above it.
<br>Solution: You need to move or delete some files. If you are working on a project with a `/net/projects/` directory, move any data files or checkpoints into that directory (and update your code accordingly!). To check you disk usage, run `du -sh ~`

#### Error: `git@github.com: Permission denied (publickey). fatal: Could not read from remote repository.`
Cause: GitHub can not access a private key that matches the public key stored on GitHub.
<br>Solution: If you are on the cluster, make sure that you are forwarding your ssh agent. `ssh-add -l` should return the appropriate key. If no identities are found, your ssh-agent has no identities or is not being forwarded. If `ssh-add -l` locally also returns no identities, you must run `ssh-add PATH_TO_KEY` as specified in the [ssh github cluster doc](./ssh_github_cluster.md). If the correct identity is found locally, make sure your ssh config matches the one in this document. Finally make sure you have added the appropriate public key to your GitHub account.

#### Error: `Could not open a connection to your authentication agent.`
<br>Solution: Run "eval `ssh-agent -s`"

### Guides and Tips
#### Installing Large Conda Environments on the DSI Cluster

The DSI Cluster limits each user to 50GB of space in their home directory. This is enough space for most purposes, but sometimes installing large Conda environments (especially for machine learning projects) takes up more space than this during the installation process - even if the final environment is only a few gigabytes.

In order to work around this, you can change the `TMPDIR` environment variable to use the `/net/scratch` directory for temporary files created while building the environment.

To temporarily change `TMPDIR`, run the following command:
```
export TMPDIR=/net/scratch/<your_username>/tmp
```

If you want to set `TMPDIR` permanently, you can add the above command to your `.bashrc` file in your home directory. (You can add it anywhere in the file).

To check that `TMPDIR` was set correctly, run the following command:
```
echo $TMPDIR
```

You should see the path to the temporary directory that you specified.

### Troubleshooting Cluster

Whenever an error comes up, think about all the potential points of failure. Then try to isolate each and see if they work on their own. For example if you are trying to connect to a compute node with VS code using the steps in these instructions, potential points of failure are: VS Code `Remote - SSH` extension, VS Code, your internet connection, ssh config file, ssh keys, slurm, the cluster. Below find some methods to check if different components are working correctly.

Test: run `ssh fe.ds` locally through the command line:
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

Test: run `ssh -T git@github.com` locally and on a login node to test GitHub ssh keys
<br>Expected Result: `Hi GITHUB_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.`

Test: request compute node and `ssh COMPUTE_NODE.ds` where `COMPUTE_NODE` is the node name (like `g004`)
<br>Expected Result: connection to the compute node


## WSL

### Guides and Tips

#### Create a New User for WSL
If for some reason your WSL instance has no user accounts (this should not happen but sometimes does):
1. In powershell launch wsl as root: `wsl -u root`
1. `adduser USERNAME` where `USERNAME` is the username you would like to use (and should replace `USERNAME` in all following steps). You can skip adding a password by typing enter. If you add a password, note that the cursor will not move as you type, but it is still working.
1. `usermod -aG sudo USERNAME`
1. `exit` to get back to powershell. 
1. Follow instructions to [update default user](#update-default-user-for-wsl)

#### Update Default User for WSL

If you have WSL Build > 18980 (check by running `(gcm wsl).Version` in PowerShell), you can update your default user by:
1. Open your WSL distrubution in Terminal.
1. Confirm the user you wish to set as default exists. Run `cat /etc/passwd | grep "USERNAME"` where `USERNAME` is the username you expect to use. A line should return like ```USERNAME:x:1000:1000:,,,:/home/USERNAME:/bin/bash```. If it does not, you need to [create a new user](#create-a-new-user-for-wsl).
1. Add your username to be the default in your WSL config. Run ```printf "[user]\ndefault = USERNAME\n" | sudo tee -a /etc/wsl.conf``` replacing `USERNAME` with your username.
1. Go to Powershell. Restart WSL by running `wsl --shutdown`
1. Re-open your WSL distrubution in Terminal. You should now see your username.(something like `USERNAME@something:~$`)



### Troubleshooting WSL

#### 1 - Do you have WSL2 installed?
In powershell, `wsl -l -v` should return:
```
  NAME              STATE           VERSION
* Ubuntu            Running         2
```
If `Ubuntu` is not in the list and `VERSION` is not 2, an installation mistake has likely been made. 
<br />If successful, continue. Otherwise: Install WSL2.

#### 2 - Do you have Terminal installed?
Press the start button and search 'Terminal'. Press open
<br />If successful, continue. Otherwise: Install Terminal

#### 3 - Can you enter an interactive shell for your WSL2 Ubuntu instance?
Test: Open Windows Terminal. Click the dropdown on the right of your tabs at the top of the screen. Select `Ubuntu` to open a new Ubuntu shell. 
<br />If successful, continue. Otherwise: If `Ubuntu` does not appear, click settings in the dropdown. On the left menu under 'Profiles', Ubuntu should appear. Click on it and deselect 'Hide profile from dropdown'

#### 4 - Does your Ubuntu instance have a user?
Open Ubuntu in WSL in Terminal. Does the prompt start with your username? The prompt should look something like:
```
(some_conda_name) USERNAME@hostname:/path/to/cwd$
```
or
```
USERNAME@hostname:/path/to/cwd$
```
The important part for now is that `USERNAME` is a `USERNAME` you have created for WSL. It should _not_ be root. 
<br />If successful, continue. Otherwise: If the username is root, we have to check if you created a user. Type `ls /home`.
If your username appears, that means you have created a user and just need to [update the default user for WSL](#update-default-user-for-wsl). If no username appears, then you need to [create a user](#create-a-new-user-for-wsl) 