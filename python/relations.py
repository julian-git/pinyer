from local_config import tolerances, text_splitter, numeric_splitter

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
                          'shoulder_height' + text_splitter + 'shoulder_height'), \
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
            rel['pos_type_list'] = pt + numeric_splitter + pt
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
                rel['pos_type_list'] = 'p' + numeric_splitter + 'p'
                relations.append(rel) # quesito

                rel1 = rel.copy()
                rel1['pos_list'] = \
                    str(position_in_ring[i,j,m]['xml_id']) + '_' + \
                    str(position_in_ring[i+1,j,m+1]['xml_id'])
                rel1['pos_type_list'] = 'p' + numeric_splitter + 'p'
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
                rel['pos_list'] += numeric_splitter + str(position_in_ring[i,j,m]['xml_id'])
                rel['field_names'] += text_splitter + 'shoulder_width'
                rel['pos_type_list'] += numeric_splitter + 'p'
                rel['coeff_list'] += numeric_splitter + '1'
            relations.append(rel)
    return relations

def baix_crosses_relations(bd, position_in_baix_group, position_in_portacrosses, relations):
    rel0 = dict([('pos_list', None), \
                     ('coeff_list', '1_-1'), \
                     ('relation_type', 'one_sided'), \
                     ('field_names', 'shoulder_height' + text_splitter + 'axle_height'), \
                     ('sense', 'le'), \
                     ('rhs', tolerances['delta_height_c_b']), \
                     ('pos_type_list', 'b_c')])

    for i in range(bd['number']):
        rel = rel0.copy()
        rel['pos_list'] = \
            str(position_in_baix_group[i, 'baix']['xml_id']) + \
            numeric_splitter + \
            str(position_in_baix_group[i, 'crossa1']['xml_id']) 
        relations.append(rel)

        rel = rel0.copy()
        rel['pos_list'] = \
            str(position_in_baix_group[i, 'baix']['xml_id']) + \
            numeric_splitter + \
            str(position_in_baix_group[i, 'crossa2']['xml_id']) 
        relations.append(rel)
    return relations


def baixos_relations(bd, position_in_baix_group, position_in_portacrosses, relations):
    relations = baix_crosses_relations(bd, position_in_baix_group, position_in_portacrosses, relations)
    return relations

def relations_xml(relations, coo_of):
    relations_xml = ''
    for rel in relations:
        relations_xml += '<relation'
        for prop, val in rel.iteritems():
            relations_xml += ' ' + prop + '="' + str(val) + '"'
        relations_xml += '/>\n'
    return relations_xml
