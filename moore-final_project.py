# Kevin Moore — LIS 452, 2CR

import re

print("This program attempts to parse Project Gutenberg ebooks, splitting text into discrete chunks and performing basic analytics.")

print("\nHere are the following texts you can test using this program:")

book_list = ["frankenstein", "heart of darkness", "metamorphosis", "pride and prejudice", "a tale of two cities"]
for i in book_list:
    print("\t", i.title())

sentinel = False
book_check = ""

#Let the user pick one of the available texts to parse
while not sentinel:
    book_check = input("\nWhich text would you like to test? ")
    if book_check.lower() in book_list:
        sentinel = True
    else:
        print("I'm sorry. That doesn't appear to be one of the available books. Please try again")

file_name = (book_check.lower()).replace(" ", "_") + ".txt"

file_text = open(file_name, "r")
full_text = file_text.read()

#Eliminate the extraneous Project Gutenberg information located before and after the main text of the book.
full_text = re.split("\*{3}[A-Za-z;\s]*\*{3}", full_text)
max = 0
max_text = ""
for i in full_text:
    if len(i) > max:
        max_text = i
        max = len(i)

full_text = max_text.strip()

#Eliminate the last chunk of extraneous information and prepare to split the text by chapter or section.
full_text = full_text.split("End of the Project Gutenberg EBook")
full_text = full_text[0].strip()

#We're getting closer, but the program isn't capable of identifying and splitting on Roman numerals just yet.
#It does work for splitting Frankenstein and Pride and Prejudice though
split_text = re.split("[A-Z][a-z]{2,}\s[0-9]{1,2}\n", full_text)

print(len(split_text))

for i in split_text:
    print("\n****************NEW SECTION*****************")
    print(i)


file_text.close()
