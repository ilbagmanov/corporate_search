import prepare_inverted_index
import prepare_tokens_and_lemmas
import search_inverted_index

if __name__ == '__main__':
    # prepare_tokens_and_lemmas.start()
    # prepare_inverted_index.start()
    # search_inverted_index.test()
    s = '123 we we  we'
    x = s[0:s.find(' ')]
    y = s[s.find(' '):]
    print(x)
    print(y)
