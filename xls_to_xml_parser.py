# -------------------------------------------------------------------------------------------
# xls_to_xml_parser.py
# XLS to XLM file parser 
# -------------------------------------------------------------------------------------------
# author: routarddev              
# -------------------------------------------------------------------------------------------

from lxml import etree
import xlrd
import datetime
import os
import sys
import codecs


# Creation of subnodes in case a cell has multiple values separated by commas
def create_nodes(container_node, node_list_name, tag_name, cell_value):
	if not container_node.find(node_list_name):
		node = etree.SubElement(container_node, str(node_list_name))

	values = cell_value.split(',')
	for value in values:
		etree.SubElement(node, "%s" % tag_name).text = value.strip()


# Main program execution
def main():

	if (len(sys.argv)>1) and ('-h' in sys.argv or '--help' in sys.argv):
		print "\nusage: python xls_to_xml_parser.py file.xls file.xml"
		print "Options and arguments:" 
		print "file.xls\t: input Excel file from where to read the data"
		print "file.xml\t: output XML file\n"
		exit()

	elif (len(sys.argv) == 3):
		xls_filename = sys.argv[1]
		xlm_filename = sys.argv[2]
		if not (xls_filename.lower().endswith('.xls') and xlm_filename.lower().endswith('.xml')):
			print "\n File extension should be XLS for the first file and XML for the second."
			exit()
		else:
			if not os.path.isfile(xls_filename):
				print "\n Error: XLS file does not exist."
				exit()

	else:
		print "\n Incorrect number of arguments. Type: xls_to_xml_parser.py -h"
		exit()


	# Prepare basic structure of the XML document
	root = etree.Element("ingestion", name="%s" % 'XLS to XML parser', dateCreated=datetime.datetime.now().isoformat())
	dataList = etree.SubElement(root, "data")

	# Open XLS file and prepare to read
	workbook = xlrd.open_workbook(xls_filename, on_demand=True)
	# Hypothesis: all required data is on the first sheet
	sheet = workbook.sheet_by_index(0)

	# Reading and parsing XLS file
	# Iterate through rows
	for row_idx in range(1, sheet.nrows):
	    # Create new data node
	    data_row = etree.SubElement(dataList, "row", id='%s' % row_idx)
	    
	    # Iterate through columns
	    for col_idx in range(0, sheet.ncols):
	    	col_name = codecs.encode(sheet.cell(0, col_idx).value, 'utf-8').replace(" ", "_").lower()
	    	cell_value = sheet.cell(row_idx, col_idx).value

	    	# Hypothesis: multiples values will come separated by commas
	    	if ',' in cell_value:
	    		create_nodes(data_row, col_name+'s', col_name, cell_value)
	    	else:
	    		etree.SubElement( data_row, "%s" % col_name ).text = cell_value


	# Finally, pretifiy XML object and load it to a file
	obj_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
	outputFile = open(xlm_filename, 'w')
	outputFile.write(obj_xml)
	outputFile.close()



# Call to main program when the user runs the script
if __name__ == '__main__':
	main()
