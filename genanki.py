import requests
import urllib.request
from bs4 import BeautifulSoup

# Connect to Anki using AnkiConnect API
anki_url = "http://localhost:8765"
deck_name = "NEWHSK"
    
def search_sentences(word):
    url = "http://dict.youdao.com/search?q={}".format(urllib.parse.quote(word))
    try:
        html_content = urllib.request.urlopen(url).read().decode('utf-8')
        
        soup = BeautifulSoup(html_content, 'html.parser')
        example_words = ''
        example_container = soup.find('div', {'id': 'bilingual'})
        if example_container:
            for li_tag in example_container.find_all('li'):
                for p_tag in li_tag.find_all('p'):
                    exts = p_tag.text.strip()
                    if exts[0] != "《":
                        example_words += (exts+"\n")
            return example_words

        else:
            print("No example words found for '{}'".format(word))
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def update_cards_with_examples(deck_name):
    # Retrieve all cards in the deck
    cards_response = requests.post(f"{anki_url}/findCards", json={"action": "findCards", "version": 6, "params": {"query": f"deck:'{deck_name}'"}})
    if cards_response.status_code != 200:
        print(f"Failed to retrieve cards from Anki. Status code: {cards_response.status_code}")
        return
    
    cards_json = cards_response.json()
    if not cards_json:
        print("No cards found in the specified deck.")
        return
    
    for card_id in cards_json:
        # Get the card's content
        print(card_id)
        card_info_response = requests.get(f"{anki_url}/notesInfo", json={"notes": [card_id]})
        if card_info_response.status_code != 200:
            print(f"Failed to retrieve card info from Anki. Status code: {card_info_response.status_code}")
            continue
        
        card_info_json = card_info_response.json()
        if not card_info_json:
            print(f"No card info found for card ID: {card_id}")
            continue

        print(card_info_response)
        
        card_content = card_info_json[0]
        if "fields" not in card_content:
            print(f"No 'fields' key found in card content: {card_content}")
            continue
        
        mandarin_word = card_content["fields"].get("Simplified")
        if not mandarin_word:
            print(f"No 'Simplified' field found in card content: {card_content}")
            continue
        
        if mandarin_word == "我们":
            # Get example sentence for the word
            example_sentence = search_sentences(mandarin_word)
            if example_sentence:
                # Add example sentence to the card's "Examples" field
                card_content["fields"]["Examples"] = example_sentence
                # Update the card in Anki
                update_response = requests.post(f"{anki_url}/updateNoteFields", json={"note": card_content})
                if update_response.status_code != 200:
                    print(f"Failed to update card in Anki. Status code: {update_response.status_code}")
                else:
                    print(f"Updated card with example sentence for '{mandarin_word}'")

update_cards_with_examples(deck_name)
