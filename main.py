import urllib.request
from bs4 import BeautifulSoup
import json, time, random

def search_sentences(word):
    url = "http://dict.youdao.com/search?q={}".format(urllib.parse.quote(word))
    try:
        time.sleep(random.uniform(1, 2))  # Adjust the delay as needed
        html_content = urllib.request.urlopen(url).read().decode('utf-8')
        
        soup = BeautifulSoup(html_content, 'html.parser')
        example_words = "<ul>\n"  # Start with an unordered list
        example_container = soup.find('div', {'id': 'bilingual'})
        if example_container:
            for li_tag in example_container.find_all('li'):
                for p_tag in li_tag.find_all('p'):
                    exts = p_tag.text.strip()
                    if exts[0] != "《":
                        # Format each example sentence as a list item
                        example_words += f"<li>{exts}</li>\n"

            example_words += "</ul>\n"  # Close the unordered list
            return example_words
        else:
            print("No example words found for '{}'".format(word))
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
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

def update_cards_with_examples(deck_name):
        
    cards = invoke('findCards', query='deck:{}'.format(deck_name))
    total_cards = len(cards)
    for index, card_id in enumerate(cards):
        # card_id = cards[0]
        try:
            card_info = invoke('notesInfo', notes=[card_id])
            simplified = card_info[0]['fields']['Simplified']['value']
            examples_value = card_info[0]['fields']['Examples']['value']
            # Check if the examples_value is a non-empty string
            if not examples_value.strip():
                try:     
                    example_sentence = search_sentences(simplified)
                    update_note_fields(note_id=card_id, examples=example_sentence)
                    print(f"{index + 1} of {total_cards}: {simplified} OK") 
                    
                except:
                        print(f"{index + 1} of {total_cards}: {simplified} + Failed add example, or already has examples")
                        pass
                
            else:
                print(f"{index + 1} of {total_cards}: {simplified} already has example. skipp")
                
        except:
            lol = '{}'.format(card_info)
            print(f"{index + 1} of {total_cards}: {lol} + failed to retrieve card info. ID: {card_id}")
            pass

if __name__ == "__main__":
    
    # Connect to Anki using AnkiConnect API
    # anki_url = "http://localhost:8765"
    deck_name = "NEWHSK"

    update_cards_with_examples(deck_name)
