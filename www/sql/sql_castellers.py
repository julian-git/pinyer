import sys
sys.path.append('../../python')
import json
import db_interaction 

def get_colla(colla_id):
    return json.dumps(db_interaction.get_colla(db_interaction.get_db(), colla_id), separators=(',', ':'))
