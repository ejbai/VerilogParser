# Version 2: Print the name of each module separately, and what from the keywords are in it

# Known (at least, predicted) cases that won't be accounted for:
#   When keywords follow a */ in the same line: they will not be counted
#   In 'if looking_for_in_out', searching to see if input or output is in the line does not account for them being part of a comment...


import re       # for regular expressions
import sys      # for getting command line arguments (the file we are reading)

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "filename")
    sys.exit()


try:
    file = open(sys.argv[1], 'r')       # open our specified (Verilog, assumedly) file
except IOError:
    sys.exit()
lines = file.readlines()                # read the lines from the Verilog program into a list, where each element is a line as a string
file.close()                            # close the Verilog file we opened


parts = ['module', 'input', 'output', 'reg', 'wire']       # create our list of parts we want to search for; this can be updated
parts_dict = dict(zip(parts, [0 for part in parts]))                # initialize the dictionary with zeros as the counts of all the parts


in_comment_block = False
lines_in_comment_block = 0                              # assumes there is nothing to the right of the */ that ends the comment block
lines_individually_commented = 0                        # lines which are wholly commented with a //
lines_with_eol_comment_outside_comment_block = 0        # lines which have a // at some point that is not the beginning
lines_with_individual_or_eol_in_comment_block = 0


in_module = False
inputs = []
outputs = []
looking_for_in_out = False  


def clean_in_out_lists(list):
    whole = ''.join(letter for letter in list)                  # the list returned from group matching in re search was a list of single characters
    elements = [e.strip() for e in re.split(',|;', whole) if e]       # split the string by commas to create a list, then strip each item in the list
    for e in elements:
        if not e:
            elements.remove(e)                                  # get rid of empty strings
    return elements

def print_in_out(inputs, outputs):
    print('  Inputs ({}):'.format(len(clean_in_out_lists(inputs))))
    for i in clean_in_out_lists(inputs):
        print('    ', i, sep='')
    print('  Outputs ({}):'.format(len(clean_in_out_lists(outputs))))
    for o in clean_in_out_lists(outputs):
        print('    ', o, sep='')

def check_if_in_module(in_module):
    if in_module:                           # this checks to see if we're already in a module, in case the previous module did not have had an 'endmodule'
        print_in_out(inputs, outputs)       # print the inputs and outputs from the previous module before we start looking at this module
    return True



##################################################################################

# Search through each line

for line in lines:

# Look for comments
    if re.search('\s/\*', line):            # look for /* at the beginning of the text in the line
        in_comment_block = True             # we are now in a comment block
        lines_in_comment_block += 1
        continue

    if in_comment_block:                                            # if currently in a comment block
        lines_in_comment_block += 1
        if re.search('\s\*/', line):                                # end of the comment block
            in_comment_block = False                                # out of the comment block for next time
        elif re.search('.*//', line):                               # if any // while we're in the comment block
            lines_with_individual_or_eol_in_comment_block += 1
        continue

    if re.search('^//|\A\s*//', line):                          # if any // starts the line or preceded only by whitespace
        lines_individually_commented += 1
    elif re.search('.*//', line):                               # if any // preceded by anything (non-whitespace and whitespace characters)
        lines_with_eol_comment_outside_comment_block += 1


    # Look for key words ("parts")
    for part in parts:
        regex = r'\b' + re.escape(part) + r'\b'             # the keyword
        if re.search(regex, line):                          # if the keyword exists at all
            parts_dict[part] += 1                           # increase the count of the keyword
        regex2 = r'.*//.*\b' + re.escape(part) + r'\b'      # the keyword with // somewhere before it
        if re.search(regex2, line):                         # if the keyword exists within a comment
            parts_dict[part] -= 1                           # decrease the count of the keyword



    # Search based on test1.v module definition format
    if re.search(r'\bmodule\b.*input.*output', line):                           # if we're currently on the first line of the module and the inputs and outputs are defined there
        in_module = check_if_in_module(in_module)
        print("\n\nModule:", re.search('module (\w+)', line).group(1))
        if re.search('input', line):
            inputs = re.search('\(input(.*)output(.*)\)', line).group(1)        # put each character in the inputs section in a list
            outputs = re.search('\(input(.*)output(.*)\)', line).group(2)       # put each character in the outputs section in a list

    # Search based on test2.v | test3.v module definition format                # test2.v format: if we're currently on the first line of the module and the variable names are there but not specified as input or output
                                                                                # test3.v format: if we're currently on the first line of the module and there is only an open parenthesis (no variable names)
    elif re.search(r'\bmodule\b', line):
        in_module = check_if_in_module(in_module)
        print("\nModule:", re.search('module (\w+)', line).group(1))
        looking_for_in_out = True

    elif re.search('endmodule', line):                                          # end of a module
        looking_for_in_out = False
        in_module = False
        print_in_out(inputs, outputs)

    
    if looking_for_in_out:                                                      # if we are looking for inputs or outputs (since they were not part of the module definition)
        if re.search('input', line):
            inputs.append(re.search('input\s*(.*)', line).group(1))
        elif re.search('output', line):
            outputs.append(re.search('output\s*(.*)', line).group(1))

# Print the inputs and outputs if we have gotten to the end of the file and there was only one module but it had no 'endmodule'
check_if_in_module(in_module)
