"""This program generates random text based on n-grams
calculated from sample text.

Author: Nathan Sprague and Brett Long
Date: 1/20/16
"""

import random
import string

def text_to_list(file_name):
    """ Converts the provided plain-text file to a list of words.  All
    punctuation will be removed, and all words will be converted to
    lower-case.

    Argument:
        file_name - A string containing a file path.
    Returns
        A list containing the words from the file.
    """
    handle = open(file_name, 'r')
    text = handle.read().lower()
    text = text.translate(
        string.maketrans(string.punctuation,
                         " " * len(string.punctuation)))
    return text.split()

def select_random(distribution):
    """
    Select an item from the the probability distribution
    represented by the provided dictionary.

    Example:
    >>> select_random({'a':.9, 'b':.1})
    'a'
    """

    # Make sure that the probability distribution has a sum close to 1.
    assert abs(sum(distribution.values()) - 1.0) < .000001, \
        "Probability distribution does not sum to 1!"

    r = random.random()
    total = 0
    for item in distribution:
        total += distribution[item]
        if r < total:
            return item

    assert False, "Error in select_random!"


def counts_to_probabilities(counts):
    """ Convert a dictionary of counts to probalities.

    Argument:
       counts - a dictionary mapping from items to integers

    Returns:
       A new dictionary where each count has been divided by the sum
       of all entries in counts.

    Example:

    >>> counts_to_probabilities({'a':9, 'b':1})
    {'a': 0.9, 'b': 0.1}

    """
    probabilities = {}
    total = 0
    for item in counts:
        total += counts[item]
    for item in counts:
        probabilities[item] = counts[item] / float(total)
    return probabilities

def calculate_unigrams(word_list):
    """ Calculates the probability distribution over individual words.

    Arguments:
       word_list - a list of strings corresponding to the
                   sequence of words in a document. Words must
                   be all lower-case with no punctuation.
    Returns:
       A dictionary mapping from words to probabilities.

    Example:

    >>> u = calculate_unigrams(['i', 'think', 'therefore', 'i', 'am'])
    >>> print u
    {'i': 0.4, 'am': 0.2, 'think': 0.2, 'therefore': 0.2}

    """
    unigrams = {}
    for word in word_list:
        if word in unigrams:
            unigrams[word] += 1
        else:
            unigrams[word] = 1
    return counts_to_probabilities(unigrams)

def calculate_bigrams(word_list):
    """Calculates, for each word in the list, the probability distribution
    over possible subsequent words.

    This function returns a dictionary that maps from words to
    dictionaries that represent probability distributions over
    subsequent words.

    Arguments:
       word_list - a list of strings corresponding to the
                   sequence of words in a document. Words must
                   be all lower-case with no punctuation.

    Example:

    >>> b = calculate_bigrams(['i', 'think', 'therefore', 'i', 'am',\
                               'i', 'think', 'i', 'think'])
    >>> print b
    {'i':  {'am': 0.25, 'think': 0.75},
     'am': {'i': 1.0},
     'think': {'i': 0.5, 'therefore': 0.5},
     'therefore': {'i': 1.0}}

    Once the bigram dictionary has been obtained it can be used to
    obtain distributions over subsequent words, or the probability of
    individual words:

    >>> print b['i']
    {'am': 0.25, 'think': 0.75}

    >>> print b['i']['think']
    .75

    """
    bigrams = {}
    tmp = {}
    for word in zip(word_list, word_list[1:]):
        if word[0] not in bigrams:
            bigrams[word[0]] = {}
        if word[1] not in bigrams[word[0]]:
            bigrams[word[0]][word[1]] = 1
        else:
            bigrams[word[0]][word[1]] += 1
        tmp[word[0]] = counts_to_probabilities(bigrams[word[0]])
    bigrams = tmp
    return bigrams

def calculate_trigrams(word_list):
    """Calculates, for each adjacent pair of words in the list, the
    probability distribution over possible subsequent words.

    The returned dictionary maps from two-word tuples to dictionaries
    that represent probability distributions over subsequent
    words.

    Example:

    >>> b = calculate_trigrams(['i', 'think', 'therefore', 'i', 'am',\
                                'i', 'think', 'i', 'think'])
    >>> print b
    {('think', 'i'): {'think': 1.0},
    ('i', 'am'): {'i': 1.0},
    ('therefore', 'i'): {'am': 1.0},
    ('think', 'therefore'): {'i': 1.0},
    ('i', 'think'): {'i': 0.5, 'therefore': 0.5},
    ('am', 'i'): {'think': 1.0}}
    """
    trigrams = {}
    tmp = {}
    for word in zip(word_list, word_list[1:], word_list[2:]):
        if (word[0], word[1]) not in trigrams:
            trigrams[(word[0], word[1])] = {}
            trigrams[(word[0], word[1])][word[2]] = 1
        elif word[2] not in trigrams[(word[0], word[1])]:
            trigrams[(word[0], word[1])][word[2]] = 1
        else:
            trigrams[(word[0], word[1])][word[2]] += 1
        tmp[(word[0], word[1])] = counts_to_probabilities(trigrams[(word[0], word[1])])
    trigrams = tmp
    return trigrams
    

def random_unigram_text(unigrams, num_words):
    """Generate a random sequence according to the provided probabilities.

    Arguments:
       unigrams -   Probability distribution over words (as returned by the
                    calculate_unigrams function).
       num_words -  The number of words of random text to generate.

    Returns:
       The random string of words with each subsequent word separated by a
       single space.

    Example:

    >>> u = calculate_unigrams(['i', 'think', 'therefore', 'i', 'am'])
    >>> random_unigram_text(u, 5)
    'think i therefore i i'

    """
    result = ""
    for i in range(num_words):
        next_word = select_random(unigrams)
        result += next_word + " "
    return result.rstrip()

    
def random_bigram_text(first_word, bigrams, num_words):
    """Generate a random sequence of words following the word pair
    probabilities in the provided distribution.

    Arguments:
       first_word -          This word will be the first word in the
                             generated text.
       bigrams -   Probability distribution over word pairs
                             (as returned by the calculate_bigrams function).
       num_words -           The number of words of random text to generate.

    Returns:
       The random string of words with each subsequent word separated by a
       single space.

    Example:
    >>> b = calculate_bigrams(['i', 'think', 'therefore', 'i', 'am',\
                               'i', 'think', 'i', 'think'])
    >>> random_bigram_text('think', b, 5)
    'think i think therefore i am'

    >>> random_bigram_text('think', b, 5)
    'think therefore i think therefore i'

    """
    result = ""
    next_word = select_random(bigrams[first_word])
    result += first_word + " " + next_word + " "
    for i in xrange(num_words-2):
        next_word = select_random(bigrams[next_word])
        result += next_word + " "
    return result.rstrip()

def random_trigram_text(first_word, second_word, bigrams, trigrams, num_words):
    """Generate a random sequence of words according to the provided
    bigram and trigram distributions.

    By default, each new word will be generated using the trigram
    distribution.  The bigram distribution will be used when a
    particular word pair does not have a corresponding trigram.

    Arguments:
       first_word -          The first word in the generated text.
       second_word -         The second word in the generated text.
       bigrams -             bigram probabilities (as returned by the
                             calculate_bigrams function).
       trigrams -            trigram probabilities (as returned by the
                             calculate_bigrams function).
       num_words -           The number of words of random text to generate.

    Returns:
       The random string of words with each subsequent word separated by a
       single space.

    """
    result = ""
    
    result += first_word + " " + second_word + " "
    next_word = select_random(trigrams[(first_word, second_word)])
    
    for i in xrange(num_words-2):
        #Step to the next word
        first_word = second_word
        second_word = next_word
        
        if (first_word, second_word) in trigrams:
            next_word = select_random(trigrams[(first_word, second_word)])
        else:
            next_word = select_random(bigrams[first_word])
        result += next_word + " "
    return result.rstrip()

def unigram_main():
    """ Generate text from Huck Fin unigrams."""
    words = text_to_list('huck.txt')
    unigrams = calculate_unigrams(words)
    print random_unigram_text(unigrams, 100)

def bigram_main():
    """ Generate text from Huck Fin bigrams."""
    words = text_to_list('huck.txt')
    bigrams = calculate_bigrams(words)
    print random_bigram_text('the', bigrams, 100)

def trigram_main():
    """ Generate text from Huck Fin trigrams."""
    words = text_to_list('huck.txt')
    bigrams = calculate_bigrams(words)
    trigrams = calculate_trigrams(words)
    print random_trigram_text('there', 'is', bigrams, trigrams, 100)


if __name__ == "__main__":
    # You can insert testing code here, or switch out the main method
    # to try bigrams or trigrams. 
    #unigram_main()
    #bigram_main()
    #trigram_main()