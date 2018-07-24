# hobson_io.py
# author: Sam Hobson 
# A library of customizable i/o functions that I reuse frequently.

import csv 

def read_csv(
	f_path, 
	#delimiter=',', 
	csv_handler=lambda x:[list(r) for r in x],
	use_headers=False, 
	hdr_handler=lambda x:list(x),
	**kwargs
):
	"""
	Reads in a csv file and returns it as a specified data structure. By default
	it returns the data as a 2 dimensional array.  

	In: 
		f_path -- the path to the csv file to open  
		csv_handler -- pointer to a function which determines how the csv data 
			is stored. (default=as a 2D list) 
		use_headers -- set to true if the data has headers (default=False)  
		hdr_handler -- pointer to a function which determines how the header  
			data is stored. (default=as a list) 
		**kwargs -- arguments to be passed to the csv reader object

	Out: 
		vals -- the data values in the csv file in the desired formats  
		headers -- if use_headers is true, a list containing the header names
			for each column
	"""
	with open(f_path, newline='') as f_obj:
		# Create a CSV object.
		csv_o = csv.reader(f_obj, **kwargs)

		# Read headers, then values
		headers = hdr_handler(next(csv_o)) if use_headers else None
		vals = csv_handler(csv_o)

	# Return the array and matrix
	return (vals, headers) if use_headers else vals


def write_csv(
	f_path,
	data,
	headers=None,
	**kwargs
):
	"""
	Write the given data matrix to a csv file.  If the file exists, it will be
	overwritten.

	In:
		f_path -- the path to save the csv to
		data -- a 2D list of the data to write
		headers -- column headers for the data (default=None)
		**kwargs -- arguments to be passed to the csv writer object
	"""

	with open(f_path,'w',newline='') as f_obj:
		# Create a new csv writer
		csv_o = csv.writer(f_obj, **kwargs)

		# If there are headers, write those first
		if headers:
			csv_o.writerow(headers)

		# Write each row in the data matrix to the csv
		for row in data:
			csv_o.writerow(row)