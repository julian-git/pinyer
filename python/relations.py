from local_config import tolerances, field_name_splitter, pos_splitter

def ring_relations(rd, position_in_ring, relations, has_folre):
    # the default values for all relations created in this function
    if has_folre:
        sense = 'le'
    else:
        sense = 'ge'
    rel0 = dict([('pos_list', None), \
                     ('coeff_list', '1_1'), \
                     ('relation_type', 'zero_or_tol'), \
                     ('field_names', \
                          'shoulder_height' + field_name_splitter + 'shoulder_height'), \
                     ('sense', sense), \
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
                str(position_in_ring[i,j,0]['xml_id']) + '_' + \
                str(position_in_ring[i+1,j,0]['xml_id'])
            rel['pos_type_list'] = pt + pos_splitter + pt
            relations.append(rel)

    rel0['sense'] = 'le'
    # next, the relations in the quesitos
    # of these, first the shoulder_height relations between different rings
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            for m in range(1, i+1):
                rel = rel0.copy()
                rel['pos_list'] = \
                    str(position_in_ring[i,j,m]['xml_id']) + '_' + \
                    str(position_in_ring[i+1,j,m]['xml_id'])
                rel['pos_type_list'] = 'p' + pos_splitter + 'p'
                relations.append(rel) # quesito

                rel1 = rel.copy()
                rel1['pos_list'] = \
                    str(position_in_ring[i,j,m]['xml_id']) + '_' + \
                    str(position_in_ring[i+1,j,m+1]['xml_id'])
                rel1['pos_type_list'] = 'p' + pos_splitter + 'p'
                relations.append(rel1) # quesito

    # next, the relations for the shoulder_width
    rel0['relation_type'] = 'sum_in_interval'
    rel0['field_names'] = ''
    rel0['rhs'] = tolerances['width']
    rel0['pos_type_list'] = 'p'
    rel0['coeff_list'] = '1'
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
            rel = rel0.copy()
            rel['pos_list'] = str(position_in_ring[i,j,1]['xml_id'])
            rel['field_names'] = 'shoulder_width'
            for m in range(2, i+1):
                rel['pos_list'] += pos_splitter + str(position_in_ring[i,j,m]['xml_id'])
                rel['field_names'] += field_name_splitter + 'shoulder_width'
                rel['pos_type_list'] += pos_splitter + 'p'
                rel['coeff_list'] += pos_splitter + '1'
            relations.append(rel)
    return relations

def baixos_relations(bd, position_in_baix_group, position_in_portacrosses, relations):
    # the default values for all relations created in this function
    rel0 = dict([('pos_list', None), \
                     ('coeff_list', '1_-1'), \
                     ('relation_type', 'one_sided'), \
                     ('field_names', 'shoulder_height' + field_name_splitter + 'axle_height'), \
                     ('sense', 'le'), \
                     ('rhs', tolerances['delta_height_c_b']), \
                     ('pos_type_list', 'b_c')])

    # first, the relations between the baix and the crosses
    for i in range(bd['number']):
        rel = rel0.copy()
        rel['pos_list'] = \
            str(position_in_baix_group[i, 'baix']['xml_id']) + \
            pos_splitter + \
            str(position_in_baix_group[i, 'crossa1']['xml_id']) 
        relations.append(rel)

        rel = rel0.copy()
        rel['pos_list'] = \
            str(position_in_baix_group[i, 'baix']['xml_id']) + \
            pos_splitter + \
            str(position_in_baix_group[i, 'crossa2']['xml_id']) 
        relations.append(rel)
    return relations

def relations_xml(relations, coo_of):
    relations_xml = ''
    for rel in relations:
        relations_xml += '<relation'
        for prop, val in rel.iteritems():
            relations_xml += ' ' + prop + '="' + str(val) + '"'
        relations_xml += '/>\n'

        # pos_list = rel['pos_list'].split('_')
        # fpi = int(pos_list[0])
        # if len(pos_list) > 1:
        #     tpi = int(pos_list[1])
        # else:
        #     tpi = fpi

        # if rel['relation_type'] == 'zero_or_tol':
        #     relations_xml += 'M' + \
        #         str(coo_of[fpi][0]) + ',' + \
        #         str(coo_of[tpi][1]) + 'L' + \
        #         str(coo_of[fpi][0]) + ',' + \
        #         str(coo_of[tpi][1]) 

        #     # relations_xml += '<path class="' + rel['pos_type_list'] + '" d="M' + \
        #     #     str(coo_of[fpi][0]) + ',' + \
        #     #     str(coo_of[tpi][1]) + 'L' + \
        #     #     str(coo_of[fpi][0]) + ',' + \
        #     #     str(coo_of[tpi][1]) + '"/>'

        # elif rel['relation_type'] == 'abs_tol':
        #     relations_xml += 'M' + \
        #         str(coo_of[fpi][0]) + ',' + \
        #         str(coo_of[fpi][1])
        #     for pos in pos_list[1:]:
        #         relations_xml += 'L' + \
        #             str(coo_of[int(pos)][0]) + ',' + \
        #             str(coo_of[int(pos)][1])
                
        # elif rel['relation_type'] == 'one_sided':
        #     relations_xml += 'M' + \
        #         str(coo_of[fpi][0]) + ',' + \
        #         str(coo_of[fpi][1])
        #     for pos in pos_list[1:]:
        #         relations_xml += 'L' + \
        #             str(coo_of[int(pos)][0]) + ',' + \
        #             str(coo_of[int(pos)][1])

        # else:
        #     raise RuntimeError('drawing of relation not implemented')

    return relations_xml
