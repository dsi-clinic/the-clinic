Many students prefer to run notebooks on the DSI cluster using VS Code, but there are many times that you might prefer to access a notebook outside of an IDE. This is a guide on how to run a Jupyter notebook on the DSI cluster and access it through a browser on your local machine.

### Starting a Jupyter Server
1. Log in to the DSI cluster
1. Activate an environment that has ```jupyter``` installed. ```pip install jupyter``` if you need to install.
2. Run a Jupyter server:
```bash 
jupyter notebook --no-browser --port=8888
```
Notice the URLs that come up. We’ll use these soon.
3. Now, open a new terminal on your local machine to setup an SSH tunnel:
```bash
ssh -L 8888:localhost:8888 <cnetid>@fe01.ds.uchicago.edu
```
Note: if you are in a compute node (e.g. g002), instead you need to forward it twice:
```bash
ssh -t -t <cnetid>@fe01.ds.uchicago.edu -L 8888:localhost:8888 ssh g002 -L 8888:localhost:8888
```
1. Open up the URL from the first terminal (consisting of ```localhost:8888``` and a really long token). This should pull up the Jupyter interface in your browser, without having to manually input the token.
http://localhost:8888/?token=...

You should now be accessing a Jupyter notebook on your local browser that is running on the cluster.
