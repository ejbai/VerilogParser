# Version 1: Print the counts of each keyword not part of a comment, and some other information about comments

# Known (at least, predicted) cases that won't be accounted for:
#   When keywords follow a */ in the same line: they will not be counted


import re   # for regular expressions

file = open('test1.v', 'r')     # open our Verilog file
lines = file.readlines()        # read the lines from the Verilog program into a list, where each element is a line as a string
file.close()                    # close the Verilog file we opened


parts = ['module', 'input', 'output', 'inout', 'reg', 'wire']       # create our list of parts we want to search for; this can be updated
parts_dict = dict(zip(parts, [0 for part in parts]))                # initialize the dictionary with zeros as the counts of all the parts

in_comment_block = False
lines_in_comment_block = 0                              # assumes there is nothing to the right of the */ that ends the comment block
lines_individually_commented = 0                        # lines which are wholly commented with a //
lines_with_eol_comment_outside_comment_block = 0        # lines which have a // at some point that is not the beginning
lines_with_individual_or_eol_in_comment_block = 0


for line in lines:

# Look for comments
    if re.search('\s/\*', line):        # look for /* at the beginning of the text in the line
        in_comment_block = True         # we are now in a comment block
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
#        print("Line individually commented:",line)
    elif re.search('.*//', line):                               # if any // preceded by anything (non-whitespace and whitespace characters)
        lines_with_eol_comment_outside_comment_block += 1
#        print("Line with EOL comment:",line)


# Look for key words ("parts")
    for part in parts:
        regex = r'\b' + re.escape(part) + r'\b'             # the keyword
        if re.search(regex, line):                          # if the keyword exists at all
            parts_dict[part] += 1                           # increase the count of the keyword
        regex2 = r'.*//.*\b' + re.escape(part) + r'\b'      # the keyword with // somewhere before it
        if re.search(regex2, line):                         # if the keyword exists within a comment
            parts_dict[part] -= 1                           # decrease the count of the keyword


for part, count in parts_dict.items():
    print("(Non-commented) Instances of {}: {}".format(part, count))


print("\nNumber of lines in a comment block:", lines_in_comment_block)
print("Number of lines in a comment block with an entire line or EOL comment:", lines_with_individual_or_eol_in_comment_block)
print("Number of individually commented lines (total):", lines_individually_commented)
print("Number of lines not in a comment block with an EOL comment:", lines_with_eol_comment_outside_comment_block)
