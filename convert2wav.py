# convert2wav.py
# author: Sam Hobson
# 2018.07.18
# Batch convert a folder of audio files into monaural 16kHz wav files for
# speech processing tasks.


import os
import os.path
import subprocess
from datetime import datetime as dt

"""
if an output folder is not given
	output folder = input folder

for each infile in the given input folder
	out_name = use infile-name to create outfile-name
	run ffmpeg -i infile-name ... outfile-name
""" 
AUDIO_EXTS = {
	".wav", 
	".mp3",
	".ogg",
	".flac",
	".m4a",
	".wma",
	".aiff"
}

def main(in_path, out_path, force=False):
	# Make sure out path and in path arent the same
	if in_path == out_path:
		print("output path must be different from input path")
		return 1 

	# If outpath doesn't exist, create
	if not os.path.exists(out_path):
		os.mkdir(out_path)

	# Path to a logfile for writing
	now = dt.now().strftime("%Y-%m-%d_%Hh%Mm%S")
	log_f_path = os.path.join(out_path, f"log_{now}")

	# recursively walk through the in_path
	for root, dirs, files in os.walk(in_path):
		for f_name in files:
			# Split filename and extension
			nom, ext = os.path.splitext(f_name)

			# If file isn't a media file, skip
			if ext.lower() not in AUDIO_EXTS:
				continue

			# Create full input file path
			in_f_path = os.path.join(root, f_name)
			print(in_f_path)

			# Get relative dirpath
			rel_f_path = root[len(in_path)+1:]

			# Use relative dirpath to create full output file path
			# Note: m16k = monaural 16kHz
			out_f_path = os.path.join(out_path, rel_f_path, nom+ext)

			# If output file exists...
			if os.path.exists(out_f_path):
				ow = True
				# If force isn't set, confirm overwrite
				if not bool(force):
					ans = input(
						f"Output file {out_f_path} exists."+\
						"Overwrite? (y/n) [y]: "
					)
					ow = ans == '' or ans == 'y'

				# If overwrite is denied, skip file. Otherwise, erase it.
				if not ow:
					continue
				else:
					os.remove(out_f_path)

			# ffmpeg command to convert the file to Mono 16kHz wav file
			cmd = [
				'ffmpeg', 
				'-i', in_f_path, 
				'-acodec', 'pcm_s16le', 
				'-ac', '1',
				'-ar', '16000',
				out_f_path
			]

			# open a logfile for writing
			with open(log_f_path, 'a') as log_obj:
				# do some logging
				log_obj.write(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
				log_obj.write(f'\nRunning command: {" ".join(cmd)}\n')

				log_obj.flush()

				# Run the process
				p = subprocess.run(cmd, stdout=log_obj, stderr=log_obj)

				# log some newlines
				log_obj.write('\n\n')



if __name__ == '__main__':
	import sys
	if len(sys.argv) != 3:
		print("Usage: convert2wav.py in_path out_path")
		sys.exit(1)

	if main(*sys.argv[1:]):
		sys.exit(1)