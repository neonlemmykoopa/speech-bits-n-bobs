import csv
import re
import numpy as np 
from hobson_io import *


def prune_csv(data, headers, keep):
	"""
	description

	In: 
		data -- NxM ndarray of values
		headers -- list of length M with column headers for data
		keep -- a list of headers to keep
	Out:
		new_data -- NxL ndarray with only the columns defined in headers
		new_headers -- list of length L with headers for new_data
	"""
	# Create outputs
	new_data = None
	new_headers = []

	# Get dimensions of data matrix
	N,M = data.shape

	# Go through each column
	for i, header in enumerate(headers):
		# If the column is one to keep...
		if header in keep:
			# get the column, maintaining its shape as a column
			col = data[:,i].reshape(N,1)

			# If new_data is still empty, set it equal to col
			if new_data is None:
				new_data = col 

			# Otherwise append it to new_data on axis 1
			else:
				new_data = np.append(new_data, col, 1)

			# Append header to new list of headers
			new_headers.append(header)

	# Return outputs
	return new_data, new_headers


def main(in_path, keep_path, out_path):
	"""
	Run the main program

	In:
		in_path -- path to input csv file
		keep_path -- path to file containing headers to keep
		out_path -- path to output csv file.
	"""
	# First open the input csv
	csv_hndl = lambda x: np.array([np.array(r) for r in x])
	data, headers = read_csv(in_path, csv_hndl, use_headers=True, delimiter=',')

	# Read headers to keep
	keeps = []

	# Regex for ignoring comments
	cmnt_re = re.compile("^#")

	# Open and read the file
	with open(keep_path) as f_obj:
		for line in f_obj:
			line = line.strip()
			# If line is commented out, ignore
			if cmnt_re.match(line):
				continue
			# Otherwise add to list of keeps
			keeps.append(line)

	# Prune the csv
	new_data, new_headers = prune_csv(data,headers,keeps)

	# Write to output csv file
	write_csv(
		out_path, 
		new_data, 
		new_headers, 
		delimiter=',', 
		quotechar='"',
		quoting=csv.QUOTE_MINIMAL
	)


if __name__ == '__main__':
	import sys
	if len(sys.argv) != 4:
		print("Usage: in_path keep_path out_path")
		sys.exit(1)

	main(*sys.argv[1:])