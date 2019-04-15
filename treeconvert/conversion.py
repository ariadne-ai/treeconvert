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

import sys
from collections import defaultdict, deque
from enum import Enum
from itertools import groupby, chain
from operator import itemgetter

import declxml

from treeconvert.nml import things_processor, pyknossos_things_processor
from treeconvert.swc import SwcData, Edge


class FileFormats(Enum):
    NML = 'nml'
    PYKNOSSOS_NML = 'pyknossos_nml'
    SWC = 'swc'

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return FileFormats[s.upper()]
        except KeyError:
            return s


class ParseError(Exception):
    """Raised when NML XML could not be parsed correctly."""


def nml_to_dict(xml_str: str, is_pyknossos=False) -> dict:
    """Converts NML into a Python dict."""
    try:
        _ = declxml.parse_from_string(
            things_processor if not is_pyknossos else pyknossos_things_processor,
            xml_str
        )
        return _
    except declxml.XmlError as error:
        print(error, file=sys.stderr)
        raise ParseError(str(error))


def nml_to_swc(nml: dict) -> SwcData:
    nodes = {node['id']: node for node in nml['nodes']}
    targets = defaultdict(list, {
        target: [edge['source'] for edge in list(edges)]
        for target, edges in groupby(
            sorted(nml['edges'], key=itemgetter('target')),
            itemgetter('target')
        )})
    sources = defaultdict(list, {
        source: [edge['target'] for edge in list(edges)]
        for source, edges in groupby(
            sorted(nml['edges'], key=itemgetter('source')),
            itemgetter('source')
        )})
    neighbors = {node: set(sources[node] + targets[node]) for node in chain(nodes)}

    try:
        first_node = set(nodes.keys() - targets.keys()).pop()
    except KeyError:
        # No root node found, so take random node from nml['nodes'].
        first_node = set(nodes).pop()

    swc = SwcData()
    swc.append(Edge.from_nml_entry(nodes[first_node], -1))

    next_nodes = deque([first_node])
    visited = set()

    while len(next_nodes) > 0:
        node = next_nodes.popleft()
        visited.add(node)

        for neighbor in neighbors[node]:
            if neighbor in visited:
                continue
            next_nodes.append(neighbor)
            swc.append(Edge.from_nml_entry(nodes[neighbor], node))
    return swc
