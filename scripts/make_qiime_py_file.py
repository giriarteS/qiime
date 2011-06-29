#!/usr/bin/env python
# make_qiime_py_file.py

"""
This is a script which will add headers and footers to new python files
and make them executable. 
"""

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME Project" 
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.3.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from qiime.util import parse_command_line_parameters, get_options_lookup
from qiime.util import make_option
from sys import exit
from os import popen
from os.path import exists
from time import strftime
from optparse import OptionParser

options_lookup = get_options_lookup()

script_info={}
script_info['brief_description']="""Create python file""" 
script_info['script_description']="""This is a script which will add headers and footers to new python files
and make them executable.""" 
script_info['script_usage']=[] 
script_info['script_usage'].append(("""Example usage:""","""Create a new script:""","""%prog -s -a "Greg Caporaso" -e gregcaporaso@gmail.com -o my_script.py""")) 
script_info['script_usage'].append(("""""","""Create a new test file:""","""%prog -t -a "Greg Caporaso" -e gregcaporaso@gmail.com -o my_test.py""")) 
script_info['script_usage'].append(("""""","""Create a basic file (e.g., for library code):""","""%prog -a "Greg Caporaso" -e gregcaporaso@gmail.com -o my_lib.py""")) 
script_info['output_description']="""The results of this script is either a python script, test, or library file, depending on the input parameters."""
script_info['required_options']=[\
options_lookup['output_fp']
] 

script_info['optional_options']=[\
make_option('-s','--script',action='store_true',\
help="Pass if creating a script to include option parsing"+\
" framework [default:%default].", default=False),
make_option('-t','--test',action='store_true',\
help="Pass if creating a unit test file to include relevant"+\
" information [default:%default].",default=False),
make_option('-a','--author_name',
help="The script author's (probably you) name to be included"+\
" the header variables. This will typically need to be enclosed "+\
" in quotes to handle spaces. [default:%default]",default='AUTHOR_NAME'),
make_option('-e','--author_email',
help="The script author's (probably you) e-mail address to be included"+\
" the header variables. [default:%default]",default='AUTHOR_EMAIL'),
make_option('-c','--copyright',
help="The copyright information to be included in"+\
" the header variables. [default:%default]",default='Copyright 2011, The QIIME project')
] 

script_info['version'] = __version__


script_block = """
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\\
 # Example required option
 #make_option('-i','--input_dir',type="existing_filepath",help='the input directory'),\\
]
script_info['optional_options'] = [\\
 # Example optional option
 #make_option('-o','--output_dir',type="new_dirpath",help='the output directory [default: %default]'),\\
]
script_info['version'] = __version__"""

header_block =\
"""#!/usr/bin/env python
# File created on %s
from __future__ import division

__author__ = "AUTHOR_NAME"
__copyright__ = "COPYRIGHT"
__credits__ = ["AUTHOR_NAME"]
__license__ = "GPL"
__version__ = "1.3.0-dev"
__maintainer__ = "AUTHOR_NAME"
__email__ = "AUTHOR_EMAIL"
__status__ = "Development"
 
""" % strftime('%d %b %Y')

if __name__ == "__main__":
    
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    
    if opts.test and opts.script:
        option_parser.error('-s and -t cannot both be passed: file must be a'+\
        'test or a script, or neither one.')
    
    script = opts.script
    test = opts.test
    output_fp = opts.output_fp

    # Check to see if the file which was requested to be created
    # already exists -- if it does, print a message and exit
    if exists(output_fp):
        print '\n'.join(["The file name you requested already exists.",\
            " Delete extant file and rerun script if it should be overwritten.",\
            " Otherwise change the file name (-o).",\
            "Creating no files and exiting..."])
        exit(1) 

    # Create the header data
    header_block = header_block.replace('AUTHOR_NAME',opts.author_name)
    header_block = header_block.replace('AUTHOR_EMAIL',opts.author_email)
    header_block = header_block.replace('COPYRIGHT',opts.copyright)
    lines = [header_block]

    if test:
        lines.append('from cogent.util.unit_test import TestCase, main')
        # Run unittest.main() if test file
        lines += ['','','','if __name__ == "__main__":','    main()']
    elif script:
        lines.append(script_block)
        lines += ['','','','def main():',\
         '    option_parser, opts, args =\\',\
         '       parse_command_line_parameters(**script_info)',\
         '','',\
         'if __name__ == "__main__":',\
         '    main()']
    else:
        # Running the file does nothing by default if not a test file
        pass

    # Open the new file for writing and write it.
    f = open(output_fp,'w')
    f.write('\n'.join(lines))
    f.close()
    
    if test or script:
        # Change the permissions on the new file to make it executable
        chmod_string = ' '.join(['chmod 755',output_fp])
        popen(chmod_string)
        
