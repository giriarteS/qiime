#!/usr/bin/env python
# File created on 04 Jan 2010.

__author__ = "Kyle Bittinger"
__copyright__ = "Copyright 2010, The QIIME Project"
__credits__ = ["Kyle Bittinger"]
__license__ = "GPL"
__version__ = "0.92-dev"
__maintainer__ = "Kyle Bittinger"
__email__ = "kylebittinger@gmail.com"
__status__ = "Prototype"

from optparse import make_option
import os
from qiime.util import (
    load_qiime_config, get_qiime_project_dir, parse_command_line_parameters,
    )
from qiime.workflow import (
    run_process_sra_submission, print_commands, call_commands_serially,
    print_to_stdout, no_status_updates
    )

sra_template_dir = os.path.join(
    get_qiime_project_dir(), 'qiime', 'support_files', 'sra_xml_templates')

script_info={}
script_info['brief_description']="""A workflow script for creating a second-stage SRA submission."""
script_info['script_description']="""\
The steps performed by this script are:
1. Get fasta and qual from sff files.
2. Produce valid mapping file for library demultiplexing.
3. Demultiplex libraries.
4. Reduce sequence complexity by picking OTUs with cd-hit.
5. Pick a representative sequence for each OTU.
6. Blast the representative set sequences against 95% OTUs in greengenes to eliminate non-16S sequences.
7. Make per-library files of \"good\" ids to pass to sfffile.
8. Use sfffile to make per-library sff files.
9. Use sfffile to quality-trim the barcodes, primers and linkers.
10. Move files around and make archive.
11. Finally, make the XML files for a second-stage submission."""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Example:""","""""","""process_sra_submission.py -s sff_dir -e experiment.txt -r greengenes_unaligned.fasta -u submission.txt"""))
script_info['output_description']="""Produces all the files necessary to make an SRA submission, including an archive of per-library SFF files, and XML files for the experiment, runs, and submission."""
script_info['required_options'] = [
    make_option('-u', '--input_submission_fp',
        help='the tab-delimited text file with info about the submission [REQUIRED]'),
    make_option('-s', '--sff_dir', 
        help='directory containing sff files [REQUIRED]'),
    make_option('-e', '--input_experiment_fp',
        help='the tab-delimited text file with info about the experiment [REQUIRED]'),
    make_option('-r', '--reference_set_fp',
        help='path to reference set of 16S sequences [REQUIRED]'),
    ]
script_info['optional_options'] = [
    make_option('--experiment_attribute_fp',
        help='three-column, tab-delimited file of experiment attributes [default: %default]'),
    make_option('--experiment_link_fp',
        help='three-column, tab-delimited file of experiment links [default: %default]'),
    make_option('-w', '--print_only', action='store_true', default=False,
        help='Print the commands but don\'t call them [default: %default]'),
    make_option('--remove_unassigned',
        help='comma-separated list of run prefixes for which to remove unassigned sequences [default: %default]'),
    ]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    qiime_config = load_qiime_config()

    if opts.print_only:
        command_handler = print_commands
    else:
        command_handler = call_commands_serially

    if opts.verbose:
        status_update_callback = print_to_stdout
    else:
        status_update_callback = no_status_updates

    opts.remove_unassigned = opts.remove_unassigned or ''
    remove_unassigned = opts.remove_unassigned.split(',')

    run_process_sra_submission(
        opts.input_experiment_fp,
        opts.input_submission_fp,
        opts.sff_dir,
        opts.reference_set_fp,
        qiime_config,
        command_handler,
        status_update_callback,
        remove_unassigned=opts.remove_unassigned,
        experiment_link_fp=opts.experiment_link_fp,
        experiment_attribute_fp=opts.experiment_attribute_fp,
        )

if __name__ == "__main__":
    main()
