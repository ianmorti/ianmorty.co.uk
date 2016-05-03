Title: Workflow and pythonista
Author: Ian Mortimer
Date: 2015-05-29
Tags: workflow, python, iOS
Category: Productivity

Playing with [workflow](http://my.workflow.is) and
[pythonista](http://omz-software.com/pythonista/) I've got a nice way
to take a photo on my phone, store it on Dropbox and then get a link
to the file to use in a blog post like this.

The workflow starts by selecting a photo, uploading it to Dropbox then
grabbing the URL.

![Workflow part 1](https://dl.dropboxusercontent.com/s/0lqenwh1kdrz87q/IMG_1846.png?dl=0)

Once this is done, it gets passed to pythonista for a little munging
to get the proper link for embedding as follows:

![Workflow pythonista ](https://dl.dropboxusercontent.com/s/txq7udtz747iqsi/IMG_1847.png?dl=0)

And the associated script that does a regex replace on the string that
is passed in

![Pythonista workflow](https://dl.dropboxusercontent.com/s/b5yuysg4hp898cp/IMG_1845.png?dl=0)

With that in place in can now snap away and create links in my plain
text notes or blog posts right from my iPhone like this

![Blog post](https://dl.dropboxusercontent.com/s/7rf7suzghfjigtx/IMG_1848.png?dl=0)
