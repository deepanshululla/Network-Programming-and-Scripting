from __future__ import print_function
CRLF = "\r\n"
header_dictionary={}
def xtract(header_data):
	header_array=header_data.split(CRLF)
	statusLine=header_array[0]
	statusArray=statusLine.split()
	stat=statusArray[1]
	header_array2=header_array[1:len(header_array)]
	for lines in header_array2:
		hld=lines.split(':')
		# print(hld)
		header_dictionary[hld[0]]=hld[1]
	return header_dictionary
