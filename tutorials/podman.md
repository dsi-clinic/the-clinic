# Podman (Docker on the cluster)
We can't use Docker on the DSI Cluster since Docker requires root permissions which are not given on the cluster.

However, there exists a drop-in replacement, called [Podman](https://podman.io/) which is an open source Docker alternative. Podman commands follow the exact same syntax as Docker commands. All of your favorites like `docker build`, `docker run`, etc. work in Podman — just change the syntax to `podman build`, `podman run`, etc. Podman was built to be a drop-in replacement, meaning that all syntax should be exactly the same.

### Current status

Currently all `podman` commands run on the login node without any issue.

On compute nodes, Slurm sets an env variable `XDG_RUNTIME_DIR` that changes `podman`'s operation (specifically there is an issue about a specific directory `/run/user/xxxx` being created on login). The work around is to remove this environment variable by running `unset XDG_RUN_TIME_DIR` which will remove the variable from the environment and allow for operation. There is a plan to fix this issue, but as of 9/2024, the issue was still present. 

### Other Notes

#### Size Issues

One challenge you may encounter while trying to use images on the cluster is disk space limitations while building the image. Even if your image is not very large, lots of temporary files are stored while building an image. 

You can probably change the storage location of the temporary files during the build process using `export TMPDIR="my/new/tmp"` from the default `/var/tmp`. The `/net/projects` folder allows for much more file storage, so it may make sense to create a temporary directory in that folder associated with your project in order to build an image. However, this is an experimental solution and has not been tested.

Another method around this is to build the image locally (not on the cluster) and then just pull the image onto the cluster via dockerhub or another artifact repo. `podman` is able to pull images from dockerhub as outlined in the section below.

### Uploading a Local Docker Image to the Cluster

You can also upload a Docker image to the cluster and run the image using Podman.

If you have an image built locally that you would like to put on the cluster, you can use Docker hub to do this.

1.  Log in to Docker hub locally:
`docker login --username=<username> --password=<password>`
2. Tag your image locally:
`docker tag <local-image>:<tag> <username>/<repo-name>:<tag>`
This step can be a big confusing. An image can have multiple tags — what we are doing here is specifying the local image that we want to add a tag to, then tagging it with the remote repo name and the tag we want applied on the remote repo. This is required for the process of uploading the image to work correctly.
3. Push the image:
`docker push <username>/<repo-name>:<tag>`
Since we have tagged the image, we can now run the `docker push` command, which will connect with Docker hub, find our repo, and upload the image with the appropriate tag.
4. Log in to Docker hub on the remote server using Podman:
`podman login docker.io --username <username> --password <password>`
5. Download the image on the remote server using Podman:
`podman pull <username>/<repo-name>:<tag>`
6. Run your image using whatever command you want:
`podman run ...`

### Processor Architecture Conflicts

Be aware of potential conflicts with processor architecture and Docker containers. If your image is built for ARM and you are using an AMD machine, you may run into problems. If you are building and pulling images from different systems (such as building the image on an ARM based Mac system) and then pulling it onto the cluster you may run into platform incompatibility. 

Luckily there are relatively straightforward methods to build containers for different architectures, as detailed [here](https://docs.docker.com/build/building/multi-platform/).

### Validation of CNI config file

You may get a bunch of plugin warnings when using Podman on the cluster: `WARN[0000] Error validating CNI config file`. You can avoid these warnings by renaming your `~/.config/cni/net.d/87-podman.conflist` file to something like `/.config/cni/net.d/87-podman.conflist.old`. The CNI (Container Network Interface) plugins are only necessary if you want your container to be able to communicate with other containers or the outside world.

Last updated: September 2024