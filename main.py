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
                found_words.append(i)  # store ending index
            i += 1
        return found_words


def count_occurrences_with_trie(s, terms):
    trie = Trie()
    for word in terms:
        trie.insert(word)

    counts = {word: 0 for word in terms}
    word_set = set(terms)

    i = 0
    while i < len(s):
        endings = trie.search_from(s, i)
        if endings:
            longest_end = endings[-1]
            word = s[i:longest_end + 1]
            if word in word_set:
                counts[word] += 1
            i = longest_end + 1
        else:
            i += 1

    return counts


if __name__ == "__main__":
    s = "appapplebananacoconutbananaapplecoconutgrape"
    terms = ["apple", "banana", "coconut", "app"]

    result = count_occurrences_with_trie(s, terms)
    print(result)
