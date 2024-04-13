import urllib.request
from bs4 import BeautifulSoup
import json, time, random, re
    
def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):

    '''function to comunicate with ankiconnect. derived from ankiconnect docs itself'''

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

    ''' params wrapper to update the note fields '''

    params = {
            "note": {
                "id": note_id,
                "fields": {
                    "Examples": examples
                }
            }
        }
    invoke('updateNote', **params)

def youdao_sentences(word):

    '''retrieve mandarin examples from youdao.com website'''

    youdao_url = "http://dict.youdao.com/search?q={}".format(urllib.parse.quote(word))
    try:
        time.sleep(random.uniform(1, 2))  # timer limiter
        html_content = urllib.request.urlopen(youdao_url).read().decode('utf-8')
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
    
def dict_cn_sentences(word):
    
    '''retrieve mandarin examples from dict.cn website'''
    
    cdict_cn_link = "http://dict.cn/{}".format(urllib.parse.quote(word))
    try:
        time.sleep(random.uniform(1, 2))  # timer limiter
        html_content = urllib.request.urlopen(cdict_cn_link).read().decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        example_words = "<ul>\n"  # Start with an unordered list
        example_container = soup.find('div', {'class': 'layout sort'}) 
        if example_container:
            for li_tag in example_container.find_all('li'):
                exts = li_tag.text.strip().replace('\t', ' ')  # Replace tabs with spaces
                exts = re.sub(r' {2,}', ' ', exts)
                exts = re.split(r'[\n]+', exts)
                for ext in exts:
                    if ext and ext[0] != "《": 
                        example_words += f"<li>{ext}</li>\n"

            example_words += "</ul>\n"  # Close the unordered list
            return example_words
        
        else:
            print("No example words found for '{}'".format(word))
            return None
        
    except Exception as e:
        print("An error occurred:", e)
        return None

def main(deck_name, dict_cn: True):

    '''
    update notes with examples. 
    this func is basically extract all notes from the mentioned Anki dect, 
    check what is the note's word, 
    then search and add the related examples to the notes accordingly.

    Args:
    deck_name   : the deck name on your Anki
    dict_cn     : dict.cn is the examples source. 
                  rather than youdao, dict.cn has more simpler and diverse sentence options, 
                  so dict.cn is set as the default.
    '''

    success = 0
    edited_before = 0
    failed = 0
    unretrieved = 0
        
    cards = invoke('findCards', query='deck:{}'.format(deck_name))
    total_cards = len(cards)
    for index, card_id in enumerate(cards):
        
        try:
            card_info = invoke('notesInfo', notes=[card_id])
            simplified = card_info[0]['fields']['Simplified']['value']
            examples_value = card_info[0]['fields']['Examples']['value']
            
            if not examples_value.strip(): # Check if the examples_value is a non-empty string
                try:     
                    if not dict_cn:
                        example_sentence = youdao_sentences(simplified)
                    else :
                        example_sentence = dict_cn_sentences(simplified) 

                    update_note_fields(note_id=card_id, examples=example_sentence)
                    print(f"{index + 1} of {total_cards}: {simplified} OK") 
                    success += 1
                    
                except:
                        print(f"{index + 1} of {total_cards}: {simplified} + Failed add example")
                        failed += 1
                        pass
                 
            else:
                print(f"{index + 1} of {total_cards}: {simplified} already has example. skipp")
                edited_before += 1
                
        except:
            lol = '{}'.format(card_info)
            print(f"{index + 1} of {total_cards}: {lol} + failed to retrieve card info. ID: {card_id}")
            unretrieved += 1
            pass

    print(f"All done.\n{total_cards} cards\n{success} cards edited\n{failed} failed to add examples\n{unretrieved} card IDs unretrieved")

if __name__ == "__main__":
    
    deck_name = "NEWHSK"
    main(deck_name, dict_cn=True)


    # code test
    # print(dict_cn_sentences("能力"))
    # print(search_sentences("能力"))
