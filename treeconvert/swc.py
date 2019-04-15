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

import collections
from dataclasses import dataclass
from enum import IntEnum


class StructureIdentifier(IntEnum):
    """Standardized identifiers for SWC (www.neuromorpho.org) -

    """
    UNDEFINED = 0
    SOMA = 1
    AXON = 2
    BASAL_DENDRITE = 3
    APICAL_DENDRITE = 4
    CUSTOM = 5

    @classmethod
    def _missing_(cls, value):
        return StructureIdentifier.CUSTOM

    def __str__(self):
        return str(self.value)


@dataclass
class Edge:
    """http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html

    """
    sample_number: int
    structure_identifier: StructureIdentifier
    x_position: float
    y_position: float
    z_position: float
    radius: float
    parent_sample: int

    def __str__(self):
        return ' '.join(str(x) for x in vars(self).values())

    @classmethod
    def from_nml_entry(cls, node: dict, parent_id: int):
        try:
            structure_identifier = StructureIdentifier(node['comment'])
        except KeyError:
            structure_identifier = StructureIdentifier(0)
        return Edge(node['id'], structure_identifier,
                    node['x'], node['y'], node['z'], node['radius'], parent_id)


class SwcData(collections.abc.MutableSequence):
    def __init__(self, *args):
        self.nodes = []
        self.extend(list(args))

    def insert(self, index: int, item: Edge) -> None:
        if not isinstance(item, Edge):
            raise TypeError(f'Item must be of type {Edge}!')
        self.nodes.append(item)

    def __getitem__(self, i: int) -> Edge:
        return self.nodes[i]

    def __setitem__(self, i: int, o: Edge) -> None:
        self.insert(i, o)

    def __delitem__(self, i: int) -> None:
        del self.nodes[i]

    def __len__(self) -> int:
        return len(self.nodes)

    def __str__(self):
        # This returns a complete SWC file by combining all of its Edges
        return '\n'.join(str(edge) for edge in self)
