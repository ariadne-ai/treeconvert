# This file is part of treeconvert.
#
# Copyright (C) 2019 ariadne-service gmbh
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# ariadne-service gmbh ariadne.ai
# Sebastian Spaar sebastian.spaar@ariadne.ai

from argparse import ArgumentParser
from pathlib import Path
from os.path import isfile
from sys import exit, stderr

from treeconvert.conversion import FileFormats, nml_to_swc, nml_to_dict

parser = ArgumentParser(
    description='Convert annotation files between various formats.',
    epilog='If the output format is SWC, and if there are multiple trees in '
           'the input file, treeconvert will create a file for each tree, '
           'and append the filename with its index.'
)
parser.add_argument('--from', type=FileFormats.argparse, dest='from_format',
                    help='input format', required=True,
                    choices=(FileFormats.NML, FileFormats.PYKNOSSOS_NML))
parser.add_argument('--to', type=FileFormats.argparse, dest='to_format',
                    help='output format', required=True,
                    choices=(FileFormats.SWC,))
parser.add_argument('--force', action='store_true',
                    help='overwrite existing output files.')
parser.add_argument('input_file', type=str,
                    help='Input file. Output file will be created '
                         'automatically with extension `.[--to]\'.')

args = parser.parse_args()

input_file = Path(args.input_file)
with input_file.open() as f:
    content = f.read()

nml = nml_to_dict(content, args.from_format == FileFormats.PYKNOSSOS_NML)

for i, thing in enumerate(nml['things']):
    swc = nml_to_swc(nml['things'][i])

    if len(nml['things']) == 1:
        output_file = f'{input_file.stem}.swc'
    else:
        # Append index to filename
        output_file = f'{input_file.stem}.swc.{i + 1}'

    if args.force is False and isfile(output_file):
        print(f'There is already a file called {output_file}! '
              f'Use `--force\' to overwrite it.', file=stderr)
        exit(-1)

    with open(output_file, 'w') as f:
        f.write(str(swc))
        f.write('\n')  # so that file ends with empty line
