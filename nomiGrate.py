#!/usr/bin/python

import os
import datetime as dt
import sys
from shutil import copyfile
from time import sleep

now       = dt.datetime.now()
searchDir = raw_input("In which directory do I begin my search: ")
ago       = input("How many days back am I looking: ")
shellAgo  = now-dt.timedelta(days=ago)
exclude   = set([".git",".svn"])
hits      = {}
fileExts  = {}
fileCount = 0
images    = []

def writeOut(results):
	""" Grind through the results dictionary.
	In: Dictionary with file hits
	Out: A read-for-print string with one entry per line
	"""
	out = ""
	for key in sorted(results):
		out += results[key] + ":" + str(key) + str("\n")

	return out


def copyFiles(results,dest):
	""" Copy files from original location to sequestered directory for further examination
	In: Dictionary with file hits
	Out: Finished notification after either a successful series of file copies or an error
	"""
	if not os.path.exists(dest) or not os.path.isdir(dest):
		os.mkdir(dest)

	for key in sorted(results):
		print "Moving " + key + " to " + dest + "/" + os.path.basename(key)
		try:
			copyfile(key, dest+"/"+os.path.basename(key))
		except StandardError as errStr:
			print "[Error] Couldn't copy " + str(key) + ": " + str(errStr)

	return "...finished"


for root,dirs,files, in os.walk(searchDir):
	dirs[:] = [d for d in dirs if d not in exclude]
	for fname in files:
		fileCount += 1
		sys.stdout.write("Searching for files modified since " + str(shellAgo) + " [" + str(fileCount) + "]\r")
		sys.stdout.flush()
		if root.endswith("/"):
			fullPath, ext = os.path.splitext(root + fname)
		else:
			fullPath, ext = os.path.splitext(root + "/" + fname)
		st = os.stat(fullPath + ext)

		mtime = dt.datetime.fromtimestamp(st.st_mtime)
		if mtime > shellAgo:
			hits[fullPath + ext] = mtime.strftime('%Y-%m-%d %H:%M')
			if ext in fileExts:
				fileExts[ext] += 1
			else:
				fileExts[ext] = 1
			if ext in (".jpg",".png",".bmp",".gif"):
				images.append(fullPath + ext)

print "Searching for files modified since " + str(shellAgo.strftime('%Y-%m-%d'))

if len(hits) != 0:
	stamp = now.strftime('%Y%m%d-%H%M%S-')
	report = stamp + "nomiGrate-Report.txt"
	directory = stamp + "nominatedForMigration"

	print "Found " + str(len(hits)) + " modified files in the last " + str(ago) + " day(s)."

	if len(fileExts) != 0:
		print "File extensions found:"
		for ext, count in fileExts.iteritems():
			print "- " + ext + " [" + str(count) + "]"

	print "Actions:"
	print "[1] Nothing, return to command line."
	print "[2] Collect copies of hits in ./" + directory + "/"
	print "[3] Write these results to ./" + report
	print "[4] Write these results to the screen"

	action = int(raw_input("What should I do with them [1]: ") or 1)

	if action == 2:
		print "Copying to ./" + directory + "/..."
		print copyFiles(hits,directory)

	elif action == 3:
		print "Writing to " + report
		filename = "./" + report
		target = open(filename, 'w')
		output = writeOut(hits)
		target.write(output)
		target.close()
		print "...done."

	elif action == 4:
		print writeOut(hits)

	else:
		print "Goodbye"

else:
	print "No files modified in the last " + str(ago) + " day(s)."
