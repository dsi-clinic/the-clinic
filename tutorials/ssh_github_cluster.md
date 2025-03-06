# SSH / Connecting to the Computing Cluster

## Background

This document contains instructions for two important pieces of the data science clinic:
  1. How to access `github` via `ssh`
  2. How to access the DSI cluster via `ssh`

Depending on what you are working on you may need to do both or just have access via github. Sections marked [CLUSTER] are only required for using the cluster.

<!-- Research institutions often have computing clusters that can be used to perform tasks that are too intensive to be run on a typical laptop, such as training an LLM or analyzing large amounts of data. A computing cluster is a collection of computers (also referred to as nodes, machines, or servers) that are 'in the cloud' (you are not physically at one of them when using them).  -->

Please read all portions carefully and only skip if you really know what you are doing. If you come across an issue, check that it isn't addressed in [Troubleshooting](troubleshooting.md) before asking. 

If you are looking for instructions on using slurm to submit compute jobs, please refer to [the clinic's SLURM documentation](slurm.md)

If there is a section which is unclear or needs updating, please open an issue or pull request!

## Table of Contents

- [SSH / Connecting to the Computing Cluster](#ssh--connecting-to-the-computing-cluster)
  - [Background](#background)
  - [Table of Contents](#table-of-contents)
  - [Part 0: Do I (already) have access?](#part-0-do-i-already-have-access)
  - [Part 1: SSH Background \& Prerequisites](#part-1-ssh-background--prerequisites)
  - [Part II: Set up SSH](#part-ii-set-up-ssh)
    - [Step 1: Verify/Install ssh-agent](#step-1-verifyinstall-ssh-agent)
      - [\[Windows\] Enable OpenSSH](#windows-enable-openssh)
      - [\[Mac/Linux\] Verify ssh-agent](#maclinux-verify-ssh-agent)
    - [Step 2: Create / Manage SSH Keys](#step-2-create--manage-ssh-keys)
      - [\[Windows Users Only\] Manage SSH Keys with WSL2](#windows-users-only-manage-ssh-keys-with-wsl2)
    - [Step 3: Add your keys to ssh-agent](#step-3-add-your-keys-to-ssh-agent)
    - [Step 4: \[CLUSTER\] Save SSH Configuration](#step-4-cluster-save-ssh-configuration)
    - [Step 5: Enable Authentication with SSH Keys](#step-5-enable-authentication-with-ssh-keys)
      - [Enabling access to github](#enabling-access-to-github)
      - [\[CLUSTER\] Mac/Linux Instructions for Remote Authentication](#cluster-maclinux-instructions-for-remote-authentication)
      - [\[CLUSTER\] Windows Instructions for Remote Authentication](#cluster-windows-instructions-for-remote-authentication)
  - [Verification](#verification)

## Part 0: Do I (already) have access?

Some students may already have access to the cluster and github and may not need to follow the below instructions. To verify both your github and cluster access, type in the following in a _terminal window_:

1. ```ssh -T git@github.com``` which, if set up properly should generate:
  
  ```
  Hi NickRoss! You've successfully authenticated, but GitHub does not provide shell access.
  Connection to github.com closed.
  ```

2. [CLUSTER] ```ssh fe.ds``` which, if set up properly should generate:
   
```~ ssh fe.ds
  ###############################################################################
  #                                                                             #
  #   *****  IMPORTANT NOTICE: DO NOT RUN COMPUTE JOBS ON LOGIN NODE  *****     #
  #                                                                             #
  #  The login node is for connecting, editing, and submitting jobs only!       #
  #                                                                             #
  #  High-intensive compute jobs must be submitted through the SLURM scheduler. #
  #  Use interactive sessions or submit batch jobs as appropriate.              #
  #                                                                             #
  #       Failure to comply may result in job termination without notice.       #
  #                                                                             #
  #                 For help, contact techstaff@cs.uchicago.edu                 #
  #                                                                             #
  ###############################################################################

Last login: Fri Sep 13 15:06:37 2024 from 10.150.1.240
(base) nickross@fe01:~$
```

The above is also how we demonstrate access to the required resources. If you already have access to the resources that are required you do not need to complete this document.

## Part 1: SSH Background & Prerequisites

To be able to connect to the DSI's cluster you will need an internet connection and will log in using a technology called "secured shell protocol" [("SSH")](https://en.wikipedia.org/wiki/Secure_Shell). This document takes you through the steps to set up an account and login via SSH to this system.

SSH is a command line tool which has a steeper learning curve than GUI-based systems such as VS Code. As such the instructions below will also install an extension to the VS Code IDE which allows you to connect your entire VS Code window to the cluster, allowing you to utilize all of VS Code's features and extensions.

We will focus on installing and verifying a number of different pieces of this software that will be installed or used in the manual below. The table below contains a brief glossary of some of the components that will be used.

| Component Name | What it does / why is it important | 
| --- | --- |
| `wsl2` (Windows only) | This is required to be installed on windows machines to access `bash` and a unix terminal | 
| `OpenSSH` | This is a common implementation of the SSH protocol, depending on your operating system
| `ssh-agent` | This is a key manager for `ssh` which runs in the background. In this course there are two things which `ssh-agent` does: (1) it allows you to avoid entering in your `ssh` password every time you login and (2) it allows for forwarding of `ssh` keys, so that if you are logged into the cluster you can continue to use the keys that are on your machine. 
| _Public_ `ssh` key | When you create an `ssh` key there are two files created, one of which is a _public_ key. This is _shareable_ and will usually be a file that ends in `.pub` 
| _Private_ `ssh` key | When you create an `ssh` key the other file that is created is a `private` key. A private key _should never be shared_ as it is the key that allows you to enter other systems 

This guide is specifically tailored to the University of Chicago DSI Cluster, though it should be generally applicable to most Slurm clusters.

_Before continuing, make sure that you have the following completed:_

- A CNET id
- [CLUSTER] A CS Account. If you are getting access through the Data Science Clinic, an account will be created for you. Otherwise you can get [one here](https://account-request.cs.uchicago.edu/account/requests).
- [CLUSTER] Access to a Slurm partition. If you are getting access through the Data Science Clinic, this will be provided for you. Otherwise send an email to techstaff@cs.uchicago.edu asking for access to compute nodes on the DSI cluster.
- A reasonably up to date and functioning computer running on Windows (10/11), Mac (10.13+/High Sierra+), or Linux. 
- An internet connection. You'll need internet to use SSH.
- VS Code Installed
- A GitHub account

[CLUSTER] Notes: You do not need access to a Slurm partition to continue and set up *access* to the cluster, but you will need it to *use* the cluster. 

<div align="center">

| **Do NOT go past this until you have completed the above.** |
|-----------------------------|

</div>

## Part II: Set up SSH

It can be annoying / burdensome to constantly type in your passwords (*something only you know*) to connect to the cluster or push/pull from GitHub. We can switch to authenticating based on *something only you have* using ssh keys and greatly reduce the friction of developing. 

### Step 1: Verify/Install ssh-agent
There are different steps for Windows users and Mac/Linux users. Follow the below steps. 

#### [Windows] Enable OpenSSH

To set up Windows to use ssh like linux complete the following (from [this SO answer](https://stackoverflow.com/a/40720527)):<!-- markdown-link-check-enable -->
1. Open "Manage optional features" or "Optional features" from the start menu and make sure you have Open SSH Client in the list. If not, you should be able to add it.
2. Open Services from the start Menu
3. Scroll down to OpenSSH Authentication Agent > right click > properties.
4. Change the Startup type from Disabled to "Automatic (Delayed Start)"
5. Open cmd and type `where ssh` to confirm that the top listed path is in System32. Mine is installed at `C:\Windows\System32\OpenSSH\ssh.exe`. If it's not in the list you may need to close and reopen cmd.
6. You should now be able to access OpenSSH tools from the Windows Command Prompt. Continue to General Instructions. 

<div align="center">

| **Windows: Do NOT continue until in PowerShell, `Get-Service ssh-agent` returns with a 'Running' Status _after_ rebooting.** |
|-----------------------------|

</div>


#### [Mac/Linux] Verify ssh-agent

1. Mac/Linux: In the terminal, type in `echo $SSH_AUTH_SOCK` 
   - If this returns _nothing_ then you need to install `ssh-agent`
     - You will need to add the command `eval $(ssh-agent)` to your shell configuration (`.zshrc/.bashrc`) file. 

If ssh-agent was not running, please reboot and verify that it loads on start. 

<div align="center">

| **Mac/Linux: Do NOT continue until you have verified that ssh-agent runs _after_ rebooting.** |
|-----------------------------|

</div>

### Step 2: Create / Manage SSH Keys

1. In the terminal (Command Prompt in Windows) of your local computer navigate to the `.ssh` (pronounced "dot-s-s-h") directory: 
    * On Linux/Mac `cd ~/.ssh`
    * On Windows `cd C:\Users\YOUR_USERNAME\.ssh\`
2. Use `ssh-keygen`, [instructions here](https://www.ssh.com/academy/ssh/keygen). Recommended: use `ssh-keygen -t ecdsa -b 521` or `ssh-keygen -t ed25519` to generate your key. 
3. You will be prompted to enter a file name for the key. Give it an identifiable name, such as `dsi_cluster` and verify the file is in the  directory listed above. Otherwise you can click enter to accept the default suggestion. 
4. You can _optionally_ add a password to your SSH key, though it is not required. As you type the password in, no text will appear on screen to keep your password length private from shoulder surfers. You will be asked to repeat it. Do not forget your password! Write it down, or ideally store it in a password manager.
5. After running this there should be two files in the `.ssh` directory. A `KEYNAME` and `KEYNAME.pub` file will be created by this command. The file with the `.pub` extension is your public key and can be shared safely. The file with no extension is your private key and should never be shared. `KEYNAME` will either be the name you specified above or the the encryption type. 
<div align="center">

| **Do not continue until you have verified that both files mentioned above exist in the .ssh directory.** |
|-----------------------------|

</div>

#### [Windows Users Only] Manage SSH Keys with WSL2
If you are using Windows you need to [install WSL ("Windows Subsystem for Linux")](https://learn.microsoft.com/en-us/windows/wsl/install) on your machine. Installing this allows Windows users access to core Unix based functionality. If you are doing local developement on your Windows machine, you should do it in WSL. TODO

To confirm proper installation:
`wsl printf 'Default shell: $0\nUsername: $USER\nHome Directory: $(cd ~ && pwd)'`
This should return:
```
Default shell: /bin/bash
Username: YOUR_WSL_USERNAME
Home Directory: /home/YOUR_WSL_USERNAME
```
Where `YOUR_WSL_USERNAME` is the username you picked when setting up WSL. It <b>should not be `root`</b> If one of these is incorrect, please go to [troubleshooting instructions](./troubleshooting.md#troubleshooting-wsl)

The convenience of 'pretending' to have two separate operating systems on one can lead to complications. One is with SSH keys, which is the core method we use to authenticate to the DSI Cluster.

The .ssh directory used on your normal Windows system and your WSL will be different from each other. This is fine in most cases, but can lead to headaches when using VS Code. If you wish to connect to a remote SSH machine in VS code, it will use your Windows configuration. So even if you only use WSL and the VS Code extension (WSL) to code in WSL2, you must follow the [Windows ssh instructions](#windows-users-only-manage-ssh-keys-with-wsl2). To use the same keys on each system, you can copy them. Following these instructions adapted from [this article](https://devblogs.microsoft.com/commandline/sharing-ssh-keys-between-windows-and-wsl-2/):

1. Open a terminal in WSL.
1. Make sure you have an .ssh folder in WSL: `mkdir -p ~/.ssh`. The `-p` means to ignore if the directory already exists.
1. Copy keys from Windows to WSL with `cp -r /mnt/c/Users/YOUR_USERNAME/.ssh ~/.ssh`
1. SSH keys should have special permissions (on a shared computer you wouldn't want other users to be able to read your private key!). Run `chmod 600 ~/.ssh/KEYNAME` and `chmod 644 ~/.ssh/KEYNAME.pub` for all the `KEYNAME`s you wish to use in WSL. 
1. Run `chmod 700 ~/.ssh`. 

<div align="center">

| **Do not continue until you have verified correct installation of WSL and can find your SSH key in both Windows and WSL** |
|-----------------------------|

</div>

### Step 3: Add your keys to ssh-agent

1. Add your key to the `ssh-agent`. To do this type in `ssh-add PATH_TO_PRIVATE_KEY`. `PATH_TO_PRIVATE_KEY` should be the _full path_ to the private file. You'll have to type your password in once and it will be saved for a period of time (terminal session or until your computer next reboots), drastically limiting the amount of times you have to type in your password. 
<!-- 2. markdown-link-check-disable[Mac Users Only] (optional) To keep the key in your `ssh-agent` across sessions, follow [this stack overflow answer](https://stackoverflow.com/questions/18880024/start-ssh-agent-on-login). markdown-link-check-enable  -->
2. Confirm your key was added. In your terminal/command prompt/powershell, run `ssh-add -l` to list all keys in your ssh agent. Your key should appear here. If this command returns `The agent has no identities.`, step 3 failed. 

<div align="center">

| **Do not continue until you have verified that your key file appears when you run `ssh-add -l`** |
|-----------------------------|

</div>

### Step 4: [CLUSTER] Save SSH Configuration

We have now created an ssh key file that will allow us to login to the cluster. However, to login we will need to provide the path to key file as well as the username each time we want to login (something like `ssh -i PATH_TO_KEY USERNAME@fe01.ds.uchicago.edu`) which is annoying and error-prone. We will use a config file, in our `.ssh` directory to simplify this process. Instead we will be able to login using just `ssh fe.ds` after completing this process.

1. Create / modify your SSH config file. To open:
    - [Windows] In command prompt: `code C:\Users\USERNAME\.ssh\config` where `USERNAME` is your windows username. 
    - [Mac] In a terminal: `touch ~/.ssh/config` to create the file if it does not exist and `open ~/.ssh/config` to open it.
2. You may or may not already have configurations saved. Place the text below in the config file, after any other configurations, *except* any block that starts with `Host *` or `Host fe01.ds.uchicago.edu`. If you have a block that has the host information then you probably already had access to the cluster and will need to redo it based on the new keys you created.  
[Mac/Linux]:
```
Host fe.ds*
  HostName fe01.ds.uchicago.edu
  IdentityFile PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User YOUR_CNET

Host *.ds !fe.ds
  HostName %h.uchicago.edu
  IdentityFile PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User YOUR_CNET
  ProxyJump fe.ds
```
[Windows]
```
Host fe.ds*
  HostName fe01.ds.uchicago.edu
  IdentityFile PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User YOUR_CNET
  MACs hmac-sha2-512

Host *.ds !fe.ds
  HostName %h.uchicago.edu
  IdentityFile PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User YOUR_CNET
  ProxyJump fe.ds
  MACs hmac-sha2-512
```
Replace `YOUR_CNET` with your CNET ID and `PATH_TO_PRIVATE_KEY` with the path the key you previously created. [Windows: `PATH_TO_PRIVATE_KEY` will be `/Users/USERNAME/.ssh/KEYNAME` where `USERNAME` is your windows username and `KEYNAME` is the name of the key you created. Starting with the root directory `/` is not standard for windows and will not typically work in other situations.] This will map `fe.ds` to an ssh command to the listed hostname, with the listed user and private key, and using the listed identity file as your key. `ForwardAgent` set to yes means that any ssh keys added to your local agent will also be added to the remote machines ssh agent (so you can use your local ssh key for GitHub on the cluster, for example). The second block is for connecting directly to compute nodes.

3. Save and close the file.

### Step 5: Enable Authentication with SSH Keys

For a private key to work for authenticating, the service you are authenticating with must have access to your public key. We will set this up for github and the cluster.

#### Enabling access to github

1. Print your public key:
   - [Windows] In command prompt: `type C:\Users\USERNAME\.ssh\KEYNAME.pub` where `USERNAME` is your Windows username and `KEYNAME` is the key your created. 
   - [Mac/Linux] In a terminal: `cat ~/.ssh/KEYNAME.pub` where `KEYNAME` is the key you created. 
2. Copy your public key. Highlight and copy *the entire output*. `ctrl+c` may not work in terminal. `ctrl+shift+c` or right click may work. 
3. Add the public key to GitHub. To give GitHub access to your public keys, go to [GitHub's ssh keys page](https://github.com/settings/keys). 
4. Click 'New SSH key'. Give it a name relating to the machine it is stored on, like "windows laptop", or "linux desktop" and paste in the full contents of the public key.
5. Verify your key was added. In terminal / command prompt, try `ssh -T git@github.com` it should respond with `Hi GITHUB_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.` or something similar. 

<div align="center">

| **Do not continue until you have verified a success message when you run `ssh -T git@github.com`** |
|-----------------------------|

</div>

#### [CLUSTER] Mac/Linux Instructions for Remote Authentication 
1. If on Mac/Linux, you can use `ssh-copy-id -i ~/.ssh/KEYNAME_HERE.pub fe.ds`, replacing `KEYNAME_HERE` with the name of the public ssh key you would like to use (it should end with .pub). 
2. You will be prompted for `USERNAME@fe01.ds.uchicago.edu`'s password. This will be your CNET password. 
3. To verify success: In your terminal, `ssh fe.ds` should connect you to the cluster without typing any password.

#### [CLUSTER] Windows Instructions for Remote Authentication
1. Copy your public key as in step 1 of [enabling access to github](#enabling-access-to-github).
2. Now connect to the server. Do `ssh fe.ds`. You'll have to type in your UChicago password. Your command prompt is now attached to the login node. The bottom left of your screen should say something like `USERNAME@fe01:~$`. 
3. Ensure there is an `.ssh` directory. If there is not, run `mkdir .ssh`. 
4. Add your public key to the list of authorized keys. Run `echo "PUBLIC_KEY_HERE" >> .ssh/authorized_keys`, replacing `PUBLIC_KEY_HERE` with the copied public key and maintaining the quotations. ctrl+v may not paste in your terminal. Try right clicking, ctrl+shift+v, and shift+insert. 
5. Type `exit` to exit the cluster and return to your windows command prompt.
6. To verify success: In your command prompt, `ssh fe.ds` should connect you to the cluster without typing any password.

## Verification 

Reboot your machine. 

**At this point you should have access to both github and, optionally, the cluster. [Verify you access before proceeding](#part-0-do-i-already-have-access).**

To learn more about using the cluster, see the [slurm documentation](./slurm.md)
