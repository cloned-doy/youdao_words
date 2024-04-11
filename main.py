#!/usr/bin/python
#



def extract_example_words(html_content):
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

def main():
    if len(sys.argv) < 2:
        print("usage: pdict.py <word>")
    else:
        word = ' '.join(sys.argv[1:])
        url = "http://dict.youdao.com/search?q={}".format(urllib.parse.quote(word))
        try:
            html_content = urllib.request.urlopen(url).read().decode('utf-8')
            # print(html_content)
            example_words = extract_example_words(html_content)
            if example_words:
                print("Example words for '{}':".format(word))
                print(example_words)
                # for example_word in example_words:
                    
                #     print(example_word)
            else:
                print("No example words found for '{}'".format(word))
        except Exception as e:
            print("An error occurred:", e)
if __name__ == "__main__":
    main()

"她工作比他努力。\nShe works harder than he does.\n你得更加努力。\nYou must try harder.\n她特别努力。\nShe tried extra hard."

    
