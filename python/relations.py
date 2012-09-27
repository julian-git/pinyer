from local_config import tolerances, field_name_splitter, pos_splitter

def ring_relations(rd, position_in_ring, relations):
    # the default values for all relations created in this function
    rel0 = dict([('pos_list', None), \
                     ('coeff_list', None), \
                     ('relation_type', 'zero_or_tol'), \
                     ('field_names', \
                          'shoulder_height' + field_name_splitter + 'shoulder_height'), \
                     ('sense', False), \
                     ('rhs', tolerances['height']), \
                     ('pos_list', None), \
                     ('pos_type_list', None)])

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
            rel['pos_type_list'] = pt + pos_splitter + pt
            relations.append(rel)

    rel0['sense'] = True 
    # next, the relations in the quesitos
    # of these, first the shoulder_height relations between different rings
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            for m in range(1, i+1):
                rel = rel0.copy()
                rel['pos_list'] = \
                    str(position_in_ring[i,j,m]['svg_id']) + '_' + \
                    str(position_in_ring[i+1,j,m]['svg_id'])
                rel['pos_type_list'] = 'p' + pos_splitter + 'p'
                relations.append(rel) # quesito

                rel1 = rel.copy()
                rel1['pos_list'] = \
                    str(position_in_ring[i,j,m]['svg_id']) + '_' + \
                    str(position_in_ring[i+1,j,m+1]['svg_id'])
                rel1['pos_type_list'] = 'p' + pos_splitter + 'p'
                relations.append(rel1) # quesito

    # next, the relations for the shoulder_width
    rel0['relation_type'] = 'abs_tol'
    rel0['field_names'] = ''
    rel0['rhs'] = tolerances['width']
    rel0['pos_type_list'] = 'p'
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
            rel = rel0.copy()
            rel['pos_list'] = str(position_in_ring[i,j,1]['svg_id'])
            rel['field_names'] = 'shoulder_width'
            for m in range(2, i+1):
                rel['pos_list'] += pos_splitter + str(position_in_ring[i,j,m]['svg_id'])
                rel['field_names'] += field_name_splitter + 'shoulder_width'
            relations.append(rel)
    return relations

def baixos_relations(bd, position_in_baix_group, position_in_portacrosses, relations):
    # the default values for all relations created in this function
    rel0 = dict([('pos_list', None), \
                     ('coeff_list', '1_-1'), \
                     ('relation_type', 'one_sided'), \
                     ('field_names', 'shoulder_height' + field_name_splitter + 'axle_height'), \
                     ('sense', True), \
                     ('rhs', tolerances['delta_height_c_b']), \
                     ('pos_type_list', 'b_c')])
    # first, the relations between the baix and the crosses
    for i in range(bd['number']):
        rel = rel0.copy()
        rel['pos_list'] = \
            str(position_in_portacrosses[i,1]['svg_id']) + \
            pos_splitter + \
            str(position_in_baix_group[i, 'crossa1']['svg_id']) 
        print rel
        relations.append(rel)

        rel = rel0.copy()
        rel['pos_list'] = \
            str(position_in_portacrosses[i,1]['svg_id']) + \
            pos_splitter + \
            str(position_in_baix_group[i, 'crossa2']['svg_id']) 
        relations.append(rel)
    return relations

def relations_svg(relations, coo_of):
    print coo_of
    relations_svg = ''
    for rel in relations:
        pos_list = rel['pos_list'].split('_')
        fpi = int(pos_list[0])
        if len(pos_list) > 1:
            tpi = int(pos_list[1])
        else:
            tpi = fpi

        if rel['relation_type'] == 'zero_or_tol':
            relations_svg += '<path class="' + rel['pos_type_list'] + '" d="M' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[tpi][1]) + 'L' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[tpi][1]) + '"/>'

        elif rel['relation_type'] == 'abs_tol':
            relations_svg += '<path class="' + rel['pos_type_list'] + '" d="M' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[fpi][1])
            for pos in pos_list[1:]:
                relations_svg += 'L' + \
                    str(coo_of[int(pos)][0]) + ',' + \
                    str(coo_of[int(pos)][1])
            relations_svg += '"/>'
                
        elif rel['relation_type'] == 'one_sided':
            relations_svg += '<path class="' + rel['pos_type_list'] + '" d="M' + \
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
