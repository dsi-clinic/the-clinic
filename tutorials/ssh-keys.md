# Creating SSH and Using SSH Keys

It can be annoying / burdensome to type in your passwords constantly to connect to the cluster or push/pull from GitHub. We can switch to authenticating based on *something we have* using ssh keys.

## [Windows Users Only] Step 1: Enable OpenSSH

If you are using Windows 10 or 11, you can use OpenSSH like Mac and Linux users. If you use WSL2, please see [specific instructions](#wsl). <!-- markdown-link-check-disable -->To ensure it is set up correctly, complete the following (from [this SO answwer](https://stackoverflow.com/a/40720527)):<!-- markdown-link-check-enable -->
1. Open Manage optional features from the start menu and make sure you have Open SSH Client in the list. If not, you should be able to add it.
2. Open Services from the start Menu
3. Scroll down to OpenSSH Authentication Agent > right click > properties
4. Change the Startup type from Disabled to any of the other 3 options. I have mine set to Automatic (Delayed Start)
5. Open cmd and type where ssh to confirm that the top listed path is in System32. Mine is installed at C:\Windows\System32\OpenSSH\ssh.exe. If it's not in the list you may need to close and reopen cmd.
6. You should know be able to access OpenSSH tools from the Windows Command Prompt. Continue to General Instructions. 


## Step 2: Create / Manage SSH Keys

1. In the terminal of your local computer (or if on windows, Command Prompt), use `ssh-keygen`, [instructions here](https://www.ssh.com/academy/ssh/keygen). Recommended: use `ssh-keygen -t ecdsa -b 521` or `ssh-keygen -t ed25519` to generate your key. 
2. If you have multiple keys, give it an identifiable name but keep it in the `.ssh` directory. Otherwise you can click enter to accept the default suggestion. 
3. You can optionally add a password to your ssh key. If you do not it may be vulnerable. Adding a password may seem counterintuitive (isn't our whole goal to avoid passwords?), but you can use [ssh-agent](https://www.ssh.com/academy/ssh/agent) (explained below) and then you will just have to type your password once per session (or once ever). As you type the password in, no text will appear on screen to keep your password length private from shoulder surfers. You will be asked to repeat it. Do not forget your password! Write it down, or ideally store it in a password manager. A `KEYNAME` and `KEYNAME.pub` file will be created by this command. The file with the `.pub` extension is your public key and can be shared safely. The file with no extension is your private key and should never be shared. 
4. (assuming you password protect your private key) Add the *private* key to your ssh agent. `ssh-add PATH_TO_KEY`. `PATH_TO_KEY` will start with `~/.ssh/` on Mac/Linux and `C:\Users\YOUR_USERNAME\.ssh\` on Windows. You'll have to type your password in once and it will be saved for a period of time (terminal session or until your computer next reboots), drastically limiting the amount of times you have to type in your password. 
5. <!-- markdown-link-check-disable -->[Mac Users Only] (optional) To keep the key in your ssh-agent accross sessions, follow [this stack overflow answer](https://stackoverflow.com/questions/18880024/start-ssh-agent-on-login). <!-- markdown-link-check-enable --> 
6. Confirm your key was added. In your terminal/command prompt/powershell, run `ssh-add -l` to list all keys in your ssh agent. Your key should appear here. If this command returns `The agent has no identities.`, step 4 failed. 

## [Windows Users Only] Step 3: Managing Keys in WSL
You can think of WSL as a separate operating system on your computer with its own file system and its own ssh agent. The ssh keys you created in Windows will not, for the most part, be accessible from WSL. 

### Option 1: Copy SSH Keys
This option is recommended if `ls ~/.ssh` returns: (a) nothing, (b) only a config file you made for clinic, or (c) an error that that directory does not exist.

1. Open a terminal in your WSL2 distro (probably Ubuntu)
2. Create an ssh directory (if one does not exist): `mkdir ~/.ssh`
3. Copy ssh keys and config files. 
a. To copy the whole contents of your Windows ssh directory:
```bash
cp "/mnt/c/Users/YOUR_WINDOWS_USERNAME/.ssh/"* ~/.ssh/
```
replacing `YOUR_WINDOWS_USERNAME` with your windows username. (Note: `/mnt/c` is the path to your Windows system from WSL. You should avoid using Windows files in WSL.) Warning: This will overwrite the contents of any files with matching names. Do not perform this command if you have files with matching names in WSL that you need. 
b. To copy files individually from your windows ssh directory:
```bash
cp "/mnt/c/Users/YOUR_WINDOWS_USERNAME/.ssh/PATH_TO_FILE" ~/.ssh/
```
replacing `YOUR_WINDOWS_USERNAME` with your windows username and `PATH_TO_FILE` with the path to the ssh files you wish to copy. You should copy the ssh keys you use for connecting to the cluster and authenticating with github (potentially the same key), and your `config` file. 
4. Make the correct permissions:
```bash
chmod 700 ~/.ssh
chmod 644 ~/.ssh/NAME_OF_KEY.pub
chmod 600 ~/.ssh/NAME_OF_KEY
chmod 600 ~/.ssh/config
```
where `NAME_OF_KEY.pub` is the public key (usually ends with `.pub`) and `NAME_OF_KEY` is the name of your private key. If the key used for github and the cluster are different, repeat this for each. 

### Option 2: Create separate SSH Keys for WSL

If you wish to have a separate set of keys for WSL and Windows, repeat Step 2.


## Configuring SSH Keys for Cluster Access

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
  MACs hmac-sha2-512 # Windows only

Host *.ds !fe.ds
  HostName %h.uchicago.edu
  IdentityFile INSERT_PATH_TO_PRIVATE_KEY
  ForwardAgent yes
  User INSERT_YOUR_CNET
  ProxyJump fe.ds
  MACs hmac-sha2-512 # Windows only
```
Replace `INSERT_YOUR_CNET` with your CNET ID and `INSERT_PATH_TO_PRIVATE_KEY` with the path the key you previously created. **NOTE**: In Linux/WSL/Mac, this should be something like `~/.ssh/KEYNAME` and in Windows this should be something like `/Users/WINDOWS_USERNAME/.ssh/KEYNAME`. This will map `fe.ds` to an ssh command to the listed hostname, with the listed user and private key, and using the listed identity file as your key. `ForwardAgent` set to yes means that any ssh keys added to your local agent will also be added to the remote machines ssh agent (so you can use your local ssh key for GitHub on the cluster, for example). The second block is for connecting directly to compute nodes.

3. Save and close the file.


## Enabling Authentication with SSH Keys

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
1. Copy your public key. Follow [Step 4: Enable Authentication with SSH Keys](#enabling-authentication-with-ssh-keys) steps 1 and 2 again.  
2. Now connect to the server. Do `ssh fe.ds`. You'll have to type in your UChicago password. Your command prompt is now attached to the login node. The bottom left of your screen should say something like `USERNAME@fe01:~$`. 
3. Ensure there is an `.ssh` directory. Run `mkdir .ssh`. 
4. Add your public key to the list of authorized keys. Run `echo "PUBLIC_KEY_HERE" >> .ssh/authorized_keys`, replacing `PUBLIC_KEY_HERE` with the copied public key and maintaining the quotations. ctrl+v may not paste in your terminal. Try right clicking, ctrl+shift+v, and shift+insert. 
5. Type `exit` to exit the cluster and return to your windows command prompt.
6. To verify success: In your command prompt, `ssh fe.ds` should connect you to the cluster without typing any password.


## Note on WSL

If you use WSL, there are several extra steps to note outlined above. An important thing to note is that the Windows ssh agent and WSL ssh agent are _different_. One may work while the other does not. In addition, the config file and ssh agent VS code uses is always the Windows one, even if you are connected to WSL. 

To debug your configuration for connecting VS code to a remote machine over ssh, open VS code command prompt, search for `Remote SSH: Open SSH Configuration File` and confirm it looks like you expect. To debug your connection on wsl, run `ssh -vv fe.ds` and confirm the ssh agent is using the appropriate file. 