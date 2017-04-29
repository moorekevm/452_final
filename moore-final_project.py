# Kevin Moore — LIS 452, 2CR

import re
import os

print("This program attempts to parse Project Gutenberg ebooks, splitting text into discrete chunks and performing basic analytics.")

print("\nHere are the following texts you can test using this program:")

book_list = ["frankenstein", "heart of darkness", "metamorphosis", "pride and prejudice", "a tale of two cities"]
for i in book_list:
    print("\t", i.title())

sentinel = False
book_check = ""

# Let the user pick one of the available texts to parse
while not sentinel:
    book_check = input("\nWhich text would you like to test? ")
    if book_check.lower() in book_list:
        sentinel = True
    else:
        print("I'm sorry. That doesn't appear to be one of the available books. Please try again")

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
# The newlines above and below help by identifying clearly demarcated headings
split_text = re.split("\n[A-Za-z]{4,}\s[0-9]{1,2}\n\n", full_text)

# If that split didn't work, try it again using Roman numerals instead of numbers
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
    if section != 0 and len(section_text) > 100:
        chapter_counter += 1
        chapter_file_name = book_check + "_chapter_" + str(chapter_counter) + ".txt"
        write_file = open(directory + "/" + chapter_file_name, "w")
        section_text = section_text.strip()
        print(section_text, file=write_file)
        write_file.close()

print("\nFinished writing chapters to individual files.")

file_text.close()
