# Kevin Moore — LIS 452, 2CR

print("This program attempts to parse Project Gutenberg ebooks, splitting text into discrete chunks and performing basic analytics.")

print("\nHere are the following texts you can test using this program:")

book_list = ["frankenstein", "heart of darkness", "jane eyre", "pride and prejudice", "a tale of two cities"]
for i in book_list:
    print("\t", i.title())

sentinel = False

while not sentinel:
    book_check = input("\nWhich text would you like to test? ")
    if book_check.lower() in book_list:
        sentinel = True
    else:
        print("I'm sorry. That doesn't appear to be one of the available books. Please try again")

file_name = (book_check.lower()).replace(" ", "_") + ".txt"

file_text = open(file_name, "r")
full_text = file_text.read()

full_text = full_text.split("End of the Project Gutenberg EBook")

if len(full_text) == 1:
    full_text = str(full_text)
    full_text = full_text.split("***END OF THE PROJECT GUTENBERG EBOOK")

full_text = full_text[0]

full_text = full_text.split("*** START OF THIS PROJECT GUTENBERG EBOOK " + book_check.upper() + " ***")

if len(full_text) == 1:
    full_text = str(full_text)
    full_text = full_text.split("***START OF THE PROJECT GUTENBERG EBOOK " + book_check.upper() + "***")

full_text = full_text[1]
print(len(full_text))

file_text.close()
