

import json
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='frontend')


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search_from(self, text, start_index):
        node = self.root
        found_words = []
        i = start_index
        while i < len(text) and text[i] in node.children:
            node = node.children[text[i]]
            if node.is_end:
                found_words.append(i)
            i += 1
        return found_words


def find_morphemes(s, terms):
    trie = Trie()
    for word in terms:
        trie.insert(word)

    word_set = set(terms)
    found_words = []

    i = 0
    while i < len(s):
        endings = trie.search_from(s, i)
        if endings:
            longest_end = endings[-1]
            word = s[i:longest_end + 1]
            if word in word_set:
                found_words.append(word)
            i = longest_end + 1
        else:
            i += 1

    return found_words

@app.route('/')
def home():
    return render_template('site.html')


@app.route('/process', methods=['POST'])
def process():
    user_input = request.form.get('userInput')  # matches the HTML input name
    print("Received from frontend:", user_input)

    # Load the morpheme data
    with open("info.json", "r") as f:
        word_data = json.load(f)

    terms = list(word_data.keys())
    found_words = find_morphemes(user_input, terms)

    meaning_with_repetition = [word_data[word] for word in found_words]
    seen = set()
    meaning_without_repetition = []

    for word in found_words:
        meaning = word_data[word]
        if meaning not in seen:
            seen.add(meaning)
            meaning_without_repetition.append(meaning)

    # Send all of this to result.html
    return render_template(
        'result.html',
        input_word=user_input,
        meaning_with_repetition=meaning_with_repetition,
    )




if __name__ == "__main__":
    app.run(debug=True)

