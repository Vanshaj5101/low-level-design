class Author:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Book:
    def __init__(self, title, author : Author):
        self.title = title
        self.author = author

    def print_info(self):
        print(f'Title : {self.title}')
        print(f'Author : {self.author.name} ({self.author.email})')

author = Author("Paulo Coelho", "paulo@gmail.com")
book = Book('The Alchemist', author)
book.print_info()
