# Podman
We can't use Docker on the DSI Cluster since Docker requires root access and we don't have root permissions when using the Cluster.

[Podman](https://podman.io/) is an open source Docker alternative. Podman commands follow the same syntax as Docker commands. All of your favorites like `docker build`, `docker run`, etc. work in Podman — just change the syntax to `podman build`, `podman run`, etc.

One challenge you may encounter while trying to use images on the cluster is disk space limitations while building the image. Even if your image is not very large, lots of temporary files are stored while building an image. 

You can probably change the storage location of the temporary files during the build process using `export TMPDIR="my/new/tmp"` from the default `/var/tmp`. The `/net/projects` folder allows for much more file storage, so it may make sense to create a temporary directory in that folder associated with your project in order to build an image. (Note: I (Todd) have not been able to make this work yet due to permissions issues while building the image.)

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


### Additional Notes
- Be aware of potential conflicts with processor architecture and Docker containers. If your image is built for ARM and you are using an AMD machine, you may run into problems.
- You will probably get a bunch of plugin warnings when using Podman on the cluster: `WARN[0000] Error validating CNI config file`. You can avoid these warnings by renaming your `~/.config/cni/net.d/87-podman.conflist` file to something like `/.config/cni/net.d/87-podman.conflist.old`. The CNI (Container Network Interface) plugins are only necessary if you want your container to be able to communicate with other containers or the outside world.

Last updated: October 2023