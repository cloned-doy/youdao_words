# Add example sentences to your Anki cards - powered by AnkiConnect

## Description

This Python script help me add example sentences related to word on my learning cards, so I can learn the words better.

The hero behind this script is [AnkiConnect](https://ankiweb.net/shared/info/2055492159) - Anki addon to expose a remote API for controlling Anki. 

The sentence examples retrieved from [Dict.cn](dict.cn) an online dictionary for looking up word definitions and examples. 

Initially I use [Youdao Dictionary](http://dict.youdao.com/) as the source, thats why this repo name is youdao.

## Prerequisites
- Anki desktop application installed
- AnkiConnect addon installed and configured in your Anki application
- Setup python env if it necessary, and install the requirements.txt.

## Usage
1. Clone this repository to your local machine.
2. Make sure your Anki desktop application is running.
3. Take a look to the main.py script, update your AnkiConnect URL if necessary. (default is `http://127.0.0.1:8765`)
4. Use the provided functions to interact with your Anki collection programmatically.
