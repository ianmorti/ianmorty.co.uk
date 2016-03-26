Title: Adding python requests documentation to dash
Author: Ian Mortimer
Date: 2015-04-01
Tags: python
Category: Development

Recently, I've been using [dash](https://kapeli.com/dash) quite a lot but I was missing some docsets, one of the most frequently used was [requests](http://docs.python-requests.org/en/latest/) so I decided to add it locally.

In order to add this into dash, you need to create a docset.

First, clone the requests git repo:

	git clone git@github.com:kennethreitz/requests.git
	
Then `cd` into the `requests/docs` directory.  Now we're going to build the docs so you want to make sure you have sphinx installed which, on a mac, is a simple:

	brew install sphinx

Now we can `make` the documentation.  I chose to build the `html` documentation with the following command:

	make html
	
This generates a `_build/html` directory which you can now point [doc2dash](https://pypi.python.org/pypi/doc2dash) at to do the conversion as follows:

	doc2dash -a -n requests _build/html
	
The `-a` option simply adds the documention automatically into dash once finished and the `-n` option gives it a name otherwise you end up with a docset called `html` which will clash with the existing `html` docset !

That's it.  Other docsets can be generated following [these instructions](https://kapeli.com/docsets) on the dash website.


