#!/usr/bin/env python

# Script: checkpatch_to_xml.py
# Author: Maloy Ghosh <mghosh@cdot.in>
#
# Purpose:
import re
import fileinput
import pprint
from xml.sax.saxutils import quoteattr, escape



CHECKPATCH_BLOCK_START_PATTERN = "^(WARNING|ERROR|CHECK):([A-Z0-9_]+):"
SUMMARY_PATTERN = "total: ([0-9]+) errors, ([0-9]+) warnings, ([0-9]+) lines checked"

def is_summary_line(line):
    summary_grp = re.search(SUMMARY_PATTERN, line)
    if (summary_grp):
        return True, summary_grp
    else:
        return False, None
def escape_strings(string):
    return quoteattr(escape(string));


def dump_xml(checkpatch_op_dict):
    op = ""
    test_number = len(checkpatch_op_dict.keys())

    op += '<testsuite name="CHECKPATCH" tests="%d">\n' % (test_number)
    for key in checkpatch_op_dict.keys():
        test_class_name = "CHECKPATCH." + key.split(":")[0]
        test_name = key.split(":")[1]
        failure_type = test_name;
        failure = escape_strings(checkpatch_op_dict[key]["short"]).strip('\"');
        system_error = escape_strings(checkpatch_op_dict[key]["long"].replace("\n\n","\n")).strip('\"')

        op += ' <testcase classname="%s" name="%s">\n' % (test_class_name, test_name)
        op += '  <failure type="%s">%s</failure>\n' % (failure_type, failure)
        op += '  <system-err>\n%s\n\n  </system-err>\n' % (system_error)
        op += ' </testcase>\n'

    op += '</testsuite>'
    print op

def main():
    checkpatch_op_dict = {}
    failure_class = ""
    failure_short_des = ""
    failure_log_des = ""
    start = True

    warnings = 0
    errors = 0
    prev_block_class = ""
    prev_block = ""
    curr_block = ""
    curr_block_class = ""


    for line in fileinput.input():
        # Check if we have reached summary line
        rsp, summary_grp = is_summary_line(line)
        if (rsp):
            break;



        line_grp = re.search(CHECKPATCH_BLOCK_START_PATTERN, line)
        if (line_grp):
            curr_block_class = line_grp.group(0)[:-1]
            curr_block = ""
            if curr_block_class not in checkpatch_op_dict.keys():
                # Initialise
                checkpatch_op_dict[curr_block_class] = {}
                checkpatch_op_dict[curr_block_class]["short"] = curr_block_class.split(":")[1]
                checkpatch_op_dict[curr_block_class]["long"] = line.replace(curr_block_class + ":", "").strip() + "\n"


            prev_block_class = curr_block_class;
        else:
            checkpatch_op_dict[prev_block_class]["long"] += line + "\n"


        #print "======================================================="
        #print " Line: " + line
        #print "#######################################################"
        #print "prev_block_class: " + prev_block_class
        #print "prev_block: " +  prev_block
        #print "#######################################################"
        #print "curr_block_class: " + curr_block_class
        #print "curr_block: "  + curr_block
        #print "======================================================="
        #pprint.pprint(checkpatch_op_dict)
        #print "======================================================="

    #pprint.pprint(checkpatch_op_dict)
    dump_xml(checkpatch_op_dict)

if __name__ == "__main__":
    main()
