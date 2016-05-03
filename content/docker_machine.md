Title: docker machine
Author: Ian Mortimer
Date: 2015-10-18
Tags: docker
Category: Development

[Docker Machine](https://docs.docker.com/machine/drivers/generic/)
provides a generic driver to allow you to use any generic linux
installation as a docker host for your containers.  When setting this
up, a few things caught me out so I'll put the process here so others
setting this up might not hit the same speed bumps !

Firstly, create your remote host somewhere.  I used Ubuntu 14.04
server for this installation.

I had to make a small tweak to the sudoers file to avoid prompts from
the docker-machine host.  Edit the sudoers file (`sudo visudo`) and
append the following line:

	<username> ALL=(ALL) NOPASSWD: ALL
	
where `username` is the username of your user on this host e.g.

	ian ALL=(ALL) NOPASSWD: ALL
	
Once you've done this and made a note of its IP address and user
credentials, go back to your local machine.

Copy over your ssh key so you can login without a password prompt:

	ssh-copy-id -i ~/.ssh/id_rsa.pub <remote user>@<remote host>

You could also create a different key and copy that over if you like
but this is the simplest for development deployments.

Now go ahead and create your machine

	docker-machine -D create -d generic --generic-ip-address <ip of remote> --generic-ssh-user <user on remote> <machine name>
	
Where <ip of remote> is the IP address of the remote host, <user on
remote> is the user on that host

The `-D` option shows debug output and you should see a bunch of
commands whizzing past indicating stuff is happening (setting
hostnames, updating host files, `apt-get update` running etc)

Once it completes you should now have a remote docker host to play
with so setup your docker-machine env vars for this host:

	eval "$(docker-machine env <machine name>)"
	
	docker ps
	
That's it.  You can now switch between your remote host and other
hosts with ease just by running the `docker-machine env` command for
the host you want.
