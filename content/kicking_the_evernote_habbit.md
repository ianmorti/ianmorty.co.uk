Title: kicking the evernote habbit
Author: Ian Mortimer
Date: 2015-01-21
Tags: evernote, plain text, workflow 
Category: Productivity

I toyed with Evernote many years ago and never really got into it
partly because I was using a [Slackware](http://www.slackware.org) box
and support for that platform was, well, rubbish and also because I
didn't really put much into it in terms of both data and effort.  Two
years ago however, as part of my mobile package I was given a free
Evernote pro subscription so I decided to give it another bash.

This time around I went all in.  I'd already amassed a fairly large
collection of text notes and I easily imported them all into Evernote.
From there I used it daily as my _everything bucket_.  It all went
in - notes from meetings, photos of mind maps on whiteboards,
receipts, PDFs of user manuals, and more.

For a while I was pretty happy with the ease of capturing my stuff and
getting it into one trusted system that would sync across all my
devices but something wasn't quite right.

For me, the problem came with lack of real structure in the notes.
Now, I could add formatting to the notes in the form of text sizes,
colours and emphasis (like **bold** and _italics_) but this all felt a
bit superficial and lacked any substance.  What I really wanted was a
way to define sections and sub sections.  Other problems started to
crop up when I pushed the editor beyond simple text like using tables
and code snippets.  Tables are not easily created and we're just plain
difficult to edit and the thing that got me with code snippets was the
seemingly impossible feat of keeping the same font across platforms
when viewing them!  For example, when setting a fixed width font on my
mac for a snippet, it would appear in Times New Roman (a variable
width font) on my iPhone and something else on my iPad - why?

As someone who takes structured notes containing many snippets of
code, these problems just caused too much friction for what should be
the simple task of creating notes to captures ideas quickly and
efficiently.

With this I set about getting my stuff out of Evernote which proved to
be a little more complicated than I'd hoped.

The main problem was the storage format. Evernote uses an XML document
structure that contains the body of the note as HTML text and
attachements as a base64 encoded blob so I knocked up a quick and
dirty Python script to extract the pertinent information from the
exported file (select all your notes you're interested in and export
them as a single .enex file) to try and recover as much of my data as
possible.

The script below makes some assumptions about the structure of my
notes and their content but should be a good starting point for
others.  I also set the file attributes to reflect the creation time
of the note in evernote.

	# -*- coding: utf-8 -*-

	import xml.etree.ElementTree as ET
	import os
	import base64
	from dateutil import parser
	import logging
	import urllib

	logging.basicConfig(filename='everout.log',
						filemode='w',
						level=logging.DEBUG,
						format='%(asctime)s %(levelname)s %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S %p')

	tree = ET.parse("My Notes.enex")
	root = tree.getroot()

	for note in root:
		dirname = None
		title = note[0].text.encode('utf-8').replace('/', '_')
		print "Processing note {}".format(title)
		updated = note[3].text
		created = note[2].text
		source_url = None
		try:
			attrs = note[4].getchildren()
			source = [x for x in note[4].getchildren() if x.tag == "source-url"]
			if source:
				source_url = source[0].text
		except Exception:
			print "no source"
		content_xml = note[1].text.encode('utf-8').replace('&mdash;', '').replace('&nbsp;', '')
		content = ET.fromstring(content_xml)
		logging.log(logging.INFO, "Creating note {}".format(title))
		# FIXME use pypandoc and export to MD
		title = title + ".txt"
		line_count = 0
		current_tag = None
		previous_tag = None
		with open(title, 'w') as f:
			if source_url:
				f.write("Source URL --> [{}]({})".format(source_url.encode('utf-8'),
													  source_url.encode('utf-8')))
			for line in content.iter():
				print("LINE: {!r} TEXT: {!r}".format(line.tag, line.text))
				previous_tag = current_tag
				current_tag = line.tag
				if line_count >= 0:
					# we had a code block, skip the lines
					print("SKIPPING LINE: {}".format(line_count))
					line_count = line_count - 1
					continue

				if line.tag == "div":
					if line.get('style', False):
						if line.get('style', '').startswith("-en-codeblock: true"):
							print "GOT CODEBLOCK"
							try:
								codeblock = line.getchildren()[0].getchildren()
								line_count = len(codeblock) + 2
								for line in codeblock:
									if line.text:
										f.write("    {}\n".format(line.text.encode('utf-8')))
								continue
							except IndexError:
								logging.error("Couldn't index into codeblock")
								continue

					if line.text:
						f.write(line.text.encode('utf-8'))
					continue

				if line.tag == "br":
					f.write("\n\n")
					continue

				if line.tag == "en-media":
					if line.get('type', '').startswith('image'):
						# use reference style link and add links at end
						link_hash = line.get('hash')
						f.write("\nIMG:{}\n".format(link_hash))
						print "ADDING IMAGE TAG for {}".format(link_hash)
						continue

				if line.tag == "a":
					href = line.get('href', '')
					if line.text:
						f.write("[{}]({})".format(line.text.encode('utf-8'),
												  href.encode('utf-8')))
						if line.tail:
							# not sure if we need to recursively apply formatting here
							f.write("{}".format(line.tail.encode('utf-8')))
						continue

				if line.tag == "b" and line.text:
					f.write("**{}**".format(line.text.encode('utf-8')))
					continue

				if line.tag == "code" and line.text:
					f.write("`{}`".format(line.text.encode('utf-8')))
					if line.tail:
						# not sure if we need to recursively apply formatting here
						f.write("{}".format(line.tail.encode('utf-8')))
					continue

				# want to look at previous tag, if ol or ul
				if line.tag == "li":
					if line.text:
						f.write(" - {}\n".format(line.text.encode('utf-8')))
					continue

				if line.tag == "span":
					print "LAST_TAG WAS {}".format(previous_tag)
					if "Source" in line.get('style', []) or "Courier" in line.get('style', []):
						if line.text:
							print "LINE (FIXED) : {}".format(line.text.encode('utf-8'))
							# f.write("    {}\n".format(line.text.encode('utf-8')))
							f.write("`{}`".format(line.text.encode('utf-8')))
							if line.tail:
								# not sure if we need to recursively apply formatting here
								f.write("{}".format(line.tail.encode('utf-8')))
							if previous_tag == "div" or previous_tag == "span":
								f.write('\n')
							continue
					if "-evernote-highlight:true" in line.get('style', []):
						if line.text:
							print "LINE HIGHLIGHT: {}".format(line.text.encode('utf-8'))
							f.write("_{}_".format(line.text.encode('utf-8')))
							if line.tail:
								# not sure if we need to recursively apply formatting here
								f.write("{}".format(line.tail.encode('utf-8')))
							if previous_tag == "div" or previous_tag == "span":
								f.write('\n')
							continue
					else:
						if line.text:
							print("STYLE WAS {} for {}".format(line.get('style'),
															   line.text.encode('utf-8')))
							f.write("{}".format(line.text.encode('utf-8')))
							continue

		if note.find('./resource') is not None:
			logging.log(logging.INFO, "Note '{}' has an attachment".format(title))
			resources = note.findall('./resource')
			logging.log(logging.INFO, "found {} resources".format(len(resources)))
			image_links = {}
			for resource in resources:
				logging.log(logging.INFO, "looking at resource")
				# Grab the object ID and append it to the file for the reference links
				resource_xml = resource.find('./recognition')
				if resource_xml is not None:
					res_tree = ET.fromstring(resource_xml.text.encode('utf-8'))
					object_id = res_tree.get('objID')
					logging.info("Found object ID: {}".format(object_id))
					binary = resource.find('./data')
					if binary.text is not None:
						filename_resource = resource.find('./resource-attributes/file-name')
						if filename_resource is None:
							logging.log(logging.WARN, "no filename found, using object_id")
							filename = object_id
							# continue
						else:
							filename = filename_resource.text.encode('utf-8')
						dirname = title + " attachments"
						if not os.path.exists(dirname):
							os.mkdir(dirname)
						resource_path = dirname + os.sep + filename
						logging.log(logging.INFO, "Creating resource file {}".format(resource_path))
						with open(resource_path, 'w') as r:
							r.write(base64.decodestring(binary.text))
						# append the reference link to the text file
						logging.info("Adding link {} to link list".format(resource_path))
						image_links[object_id] = resource_path

			if image_links:
				lines = []
				logging.info("replacing image links in file now")
				with open(title) as infile:
					for line in infile:
						for objid, target in image_links.iteritems():
							if line.startswith('IMG:'):
								# need the right format and base href
								# See http://brettterpstra.com/2012/09/27/quick-tip-images-in-nvalt/
								target_path = urllib.quote(target)
								target_link = "![{}]({})\n".format(target, target_path)
								new_line = line.replace('IMG:{}'.format(objid), target_link)
								if line != new_line:
									print "Replaced {} with {}".format(line, new_line)
									logging.info("replaced {} with {}".format(objid,
																			  target_link,
																			  line))
								line = new_line
						lines.append(line)

				logging.info("writing back file")
				with open(title, 'w') as outfile:
					for line in lines:
						outfile.write(line)

		atime = mtime = int(parser.parse(updated).strftime('%s'))
		modif = (atime, mtime)
		logging.log(logging.INFO, "setting modification date to {}".format(mtime))
		os.utime(title, modif)
		if dirname is not None:
			os.utime(dirname, modif)
			os.utime(title, modif)
		print "Note '{}' created on {}".format(title, created)

This script wasn't perfect but it extracted most of what I needed into a directory full of text files and attachments. 

In my next post I'll go through how I now store and use my notes in their plaintext format. 
