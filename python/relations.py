from local_config import tolerances

def ring_relations(rd, position_in_ring, relations):
    # the default values for all relations created in this function
    rel0 = dict([('pos_list', None), \
                     ('relation_type', 1), \
                     ('field_name', 'shoulder_height'), \
                     ('fparam1', tolerances['height']), \
                     ('pos_type', None)])

    # first, the relations between rengles de mans and rengles de vents
    for j in range(2*rd['period']):
        if j%2 == 0:
            pt = 'ma'  # Ma
        else:
            pt = 'vt'  # Vent
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            rel = rel0.copy()
            rel['pos_list'] = \
                str(position_in_ring[i,j,0]['svg_id']) + '_' + \
                str(position_in_ring[i+1,j,0]['svg_id'])
            rel['pos_type'] = pt
            relations.append(rel)

    # next, the relations in the quesitos
    # of these, first the shoulder_height relations between different rings
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            for m in range(1, i+1):
                rel = rel0.copy()
                rel['pos_list'] = \
                    str(position_in_ring[i,j,m]['svg_id']) + '_' + \
                    str(position_in_ring[i+1,j,m]['svg_id'])
                rel['pos_type'] = 'p'
                relations.append(rel) # quesito

                rel1 = rel.copy()
                rel1['pos_list'] = \
                    str(position_in_ring[i,j,m]['svg_id']) + '_' + \
                    str(position_in_ring[i+1,j,m+1]['svg_id'])
                relations.append(rel1) # quesito

    # next, the relations for the shoulder_width
    rel0['relation_type'] = 3
    rel0['field_name'] = 'shoulder_width'
    rel0['fparam1'] = tolerances['width']
    rel0['pos_type'] = 'p'
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
            rel = rel0.copy()
            rel['pos_list'] = str(position_in_ring[i,j,1]['svg_id'])
            for m in range(2, i+1):
                rel['pos_list'] += '_' + str(position_in_ring[i,j,m]['svg_id'])
            relations.append(rel)
    return relations

def baixos_relations(cd, position_in_portacrosses, relations):
    # the default values for all relations created in this function
    rel0 = dict([('pos_list', None), \
                     ('relation_type', 1), \
                     ('field_name', 'shoulder_height'), \
                     ('fparam1', tolerances['height']), \
                     ('pos_type', None)])
    # first, the relations between 
    return relations

def relations_svg(relations, coo_of):
    relations_svg = ''
    for rel in relations:
        pos_list = rel['pos_list'].split('_')
        fpi = int(pos_list[0])
        if len(pos_list) > 1:
            tpi = int(pos_list[1])
        else:
            tpi = fpi
        if rel['relation_type'] == 1:
            relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[tpi][1]) + 'L' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[tpi][1]) + '"/>'
        elif rel['relation_type'] == 3:
            relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[fpi][1])
            for pos in pos_list[1:]:
                relations_svg += 'L' + \
                    str(coo_of[int(pos)][0]) + ',' + \
                    str(coo_of[int(pos)][1])
            relations_svg += '"/>'
                
        else:
            raise RuntimeError('drawing of relation not implemented')
    return relations_svg
