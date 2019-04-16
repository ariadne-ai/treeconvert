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


import declxml

parameters = declxml.dictionary('parameters', [
    declxml.dictionary('experiment', [
        declxml.string('.', attribute='name')
    ], required=False),
    declxml.dictionary('lastsavedin', [
        declxml.string('.', attribute='version')
    ], required=False),
    declxml.dictionary('createdin', [
        declxml.string('.', attribute='version')
    ], required=False),
    declxml.dictionary('guiMode', [
        declxml.string('.', attribute='mode')
    ], required=False),
    declxml.dictionary('dataset', [
        declxml.string('.', attribute='path'),
        declxml.integer('.', attribute='overlay')
    ], required=False),
    declxml.string('nodes_0_based', required=False, default=False)
], required=False)

node_processor = declxml.dictionary('node', [
    declxml.integer('.', attribute='id'),
    declxml.floating_point('.', attribute='radius', required=False, default=1.0),
    declxml.integer('.', attribute='x', required=False),
    declxml.integer('.', attribute='y', required=False),
    declxml.integer('.', attribute='z', required=False),
    declxml.integer('.', attribute='inVp', required=False),
    declxml.integer('.', attribute='inMag', required=False),
    declxml.integer('.', attribute='time', required=False),
    declxml.string('.', attribute='comment', required=False)
], required=False)

pyknossos_node_processor = declxml.dictionary('node', [
    declxml.integer('.', attribute='id'),
    declxml.floating_point('.', attribute='radius', required=False, default=1.0),
    declxml.floating_point('.', attribute='x', required=False),
    declxml.floating_point('.', attribute='y', required=False),
    declxml.floating_point('.', attribute='z', required=False),
    declxml.integer('.', attribute='inVp', required=False),
    declxml.integer('.', attribute='inMag', required=False),
    declxml.integer('.', attribute='time', required=False),
    declxml.string('.', attribute='comment', required=False)
], required=False)

nodes_processor = declxml.array(node_processor, nested='nodes')

pyknossos_nodes_processor = declxml.array(pyknossos_node_processor, nested='nodes')

edge_processor = declxml.dictionary('edge', [
    declxml.integer('.', attribute='source'),
    declxml.integer('.', attribute='target')
], required=False)

edges_processor = declxml.array(edge_processor, nested='edges')

thing_processor = declxml.dictionary('thing', [
    declxml.integer('.', attribute='id'),
    declxml.floating_point('.', attribute='color.r', required=False),
    declxml.floating_point('.', attribute='color.g', required=False),
    declxml.floating_point('.', attribute='color.b', required=False),
    declxml.integer('.', attribute='neuron_id', required=False, omit_empty=True, default=100),
    declxml.integer('.', attribute='skeleton_id', required=False, omit_empty=True, default=99),
    nodes_processor,
    edges_processor
])

pyknossos_thing_processor = declxml.dictionary('thing', [
    declxml.floating_point('.', attribute='id'),
    declxml.floating_point('.', attribute='color.r', required=False),
    declxml.floating_point('.', attribute='color.g', required=False),
    declxml.floating_point('.', attribute='color.b', required=False),
    declxml.integer('.', attribute='neuron_id', required=False, omit_empty=True),
    declxml.integer('.', attribute='skeleton_id', required=False, omit_empty=True),
    pyknossos_nodes_processor,
    edges_processor
])

comment_processor = declxml.dictionary('comment', [
    declxml.integer('.', attribute='node'),
    declxml.string('.', attribute='content')
], required=False)

comments_processor = declxml.array(comment_processor, nested='comments')

branchpoint_processor = declxml.dictionary('branchpoint', [
    declxml.integer('.', attribute='id')
], required=False)

branchpoints_processor = declxml.array(branchpoint_processor, nested='branchpoints')

things_processor = declxml.dictionary('things', [
    parameters,
    declxml.array(thing_processor, alias='things'),
    comments_processor,
    branchpoints_processor
])

pyknossos_things_processor = declxml.dictionary('things', [
    parameters,
    declxml.array(pyknossos_thing_processor, alias='things'),
    comments_processor,
    branchpoints_processor
])
