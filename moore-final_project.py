# Kevin Moore — LIS 452, 2CR
# Final Project

import re
import os

print("This program attempts to parse Project Gutenberg ebooks, splitting text into discrete chunks and performing basic analytics.")

print("\nHere are the following texts you can test using this program:")

book_list = ["frankenstein", "heart of darkness", "metamorphosis", "pride and prejudice", "a tale of two cities"]
for i in book_list:
    print("\t", i.title())

sentinel = False
book_check = ""

# Let the user pick one of the available texts to parse.
while not sentinel:
    book_check = input("\nWhich text would you like to test? ")
    if book_check.lower() in book_list:
        sentinel = True
    else:
        print("I'm sorry. That doesn't appear to be one of the available books. Please try again.")

book_check = (book_check.lower()).replace(" ", "_")
file_name = book_check + ".txt"

file_text = open(file_name, "r")
full_text = file_text.read()

# Eliminate the extraneous Project Gutenberg information located before and after the main text of the book.
full_text = re.split("\*{3}[A-Za-z;\s]*\*{3}", full_text)
max = 0
max_text = ""
for i in full_text:
    if len(i) > max:
        max_text = i
        max = len(i)

full_text = max_text.strip()

# Eliminate the last chunk of extraneous information and prepare to split the text by chapter or section.
full_text = full_text.split("End of the Project Gutenberg EBook")
full_text = full_text[0].strip()

# Search for common chapter heading patterns like "Chapter 1" or "Section 32"
# The newlines above and below help by identifying clearly demarcated headings.
split_text = re.split("\n[A-Za-z]{4,}\s[0-9]{1,2}\n\n", full_text)

# If that split didn't work, try it again using Roman numerals instead of numbers.
if len(split_text) == 1:
    split_text = "".join(split_text)
    split_text = re.split("(\n[A-Za-z]*\s[IVX]{1,5}\.?\s?[A-Za-z\s]*\n\n)", split_text)

chapter_counter = 0

# This chunk creates a new directory to store all the chapter text files I'll be writing
# The "Try: Except:" structure came from this Stack Overflow question:
    # http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
file_path = book_check + "/chapter_text.txt"
directory = os.path.dirname(file_path)

try:
    os.stat(directory)
except:
    os.mkdir(directory)

for section, section_text in enumerate(split_text):
    # This conditional statement eliminates the title page (index position 0) and removes likely tables of contents
    # by checking the length — long text following a chapter heading probably means a full chapter instead of table of
    # contents information.
    if section != 0 and len(section_text.split()) > 50:
        chapter_counter += 1
        chapter_file_name = book_check + "_chapter_" + str(chapter_counter) + ".txt"
        write_file = open(directory + "/" + chapter_file_name, "w")
        section_text = section_text.strip()
        print(section_text, file=write_file)
        write_file.close()

print("\n\nFinished writing chapters to individual files.")

file_text.close()

# Now that we've finished parsing and writing the chapter content, let's do some basic text analysis.

chapter_lengths = []
total_words = 0
total_sections = 0
word_use = {}

# I looked at http://www.ranks.nl/stopwords to find a list of good stopwords worth excluding when calculating the
# most-used words in each chapter. I compiled those words into a Python list on my own.
stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
punctuation = ['"', '.', ',', '?', '!', ';', ':']

# This portion of the program iterates through the isolated chapters and calculates the word count for each one.
# It adds the word count to a list, maintaining order in a way that Python dictionaries don't.
for section in split_text:
    if section != 0 and len(section.split()) > 50:
        chapter_lengths.append(len(section.split()))
        # Now we go word by word and count how many times they repeat
        for word in section.split():
            for letter in word:
                # These conditionals eliminate a very specific quotation mark along with any other stray punctuation
                if ord(letter) == 8220:
                    word = word.replace(letter, "")
                if letter in punctuation:
                    word = word.replace(letter, "")
            # Now we add the word to the dictionary if it's not already entered and it isn't one of the stopwords
            if word.lower() not in word_use and word.lower() not in stopwords:
                word_use[word.lower()] = 1
            # If the word is already in the dictionary, then we increase its word count value by 1
            if word.lower() in word_use:
                word_use[word.lower()] += 1
        total_words += len(section.split())
        total_sections += 1

print("\n\nThe average chapter length is", round(total_words/total_sections), "words.")
current_chapter = 1

for chapter in chapter_lengths:
    print("Chapter " + str(current_chapter) + " is " + str(chapter) + " words long.")
    current_chapter += 1

most_used_words = []
print("\n\nHere are the five most used words in", book_check.title().replace("_", " ") + ":")

for i in range(5):
    max = 0
    max_word = ""
    # Iterate through the dictionary to find the most repeated word, delete it from the dictionary, and repeat 5 total times
    for word in word_use:
        if word_use[word] > max:
            max = word_use[word]
            max_word = word
    most_used_words.append("'" + max_word + "' is used " + str(max) + " times.")
    del word_use[max_word]

for word in most_used_words:
    print(word)
