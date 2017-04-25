# Kevin Moore — LIS 452, 2CR


print("This program attempts to parse Project Gutenberg ebooks, splitting text into discrete chunks and performing basic analytics.")

print("\nHere are the following texts you can test using this program:")
print("\tFrankenstein")
print("\tHeart of Darkness")
print("\tJane Eyre")
print("\tPride and Prejudice")
print("\tTale of Two Cities")

sentinel = False
book_list = ["frankenstein", "heart of darkness", "jane eyre", "pride and prejudice", "tale of two cities"]

while not sentinel:
    book_check = input("Which text would you like to test? ")
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

