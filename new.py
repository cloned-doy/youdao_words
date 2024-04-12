import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def update_note_fields(note_id, examples):
    params = {
            "note": {
                "id": note_id,
                "fields": {
                    "Examples": examples
                }
            }
        }
    invoke('updateNote', **params)
    
examples = "你好"


cards = invoke('findCards', query='deck:NEWHSK')
update_note_fields(note_id=result[0], examples=examples)
sample_notes = invoke('notesInfo', notes=[result[0]])
simplified = sample_notes[0]['fields']['Simplified']['value']
