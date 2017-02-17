#!/usr/bin/python

from subprocess import Popen, PIPE
import ast

#Get info from disc as string
process = Popen(["lsdvd","/dev/sr0","-x","-Oy"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

#Parse dictionary from string
dvdinfo = ast.literal_eval(output[8:])
print(dvdinfo['longest_track'])
