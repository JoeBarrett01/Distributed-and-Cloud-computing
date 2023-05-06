import Pyro5.api
from Pyro5.api import expose, serve



class Library:
    def __init__(self):
        self.users = {}
        self.authors = {}
        self.books = {}
        self.books_not_loan = set()
        self.loaned_books = {}
        self.book_copies = {}

    ## Helper Methods    
    def _find_user(self, user_name):
        return self.users.get(user_name)
    
    @expose
    # Task 1
    def add_user(self, user_name, user_number):
        """
        adds a user to library
        """
        if user_name not in self.users:
            self.users[user_name] = user_number
            print(f"User {user_name} added to the system with contact number {user_number}.")
        else:
            print(f"User {user_name} already exists in the system.")

    @expose
    # Task 2
    def return_users(self):
        user_info = []
        for name, contact in self.users.items():
            user_info.append([name, contact])
        headers = ["Name", "Contact Number"]
        max_lengths = [max(len(str(row[i])) for row in user_info) for i in range(len(headers))]
        table = ""
        # Generate header row
        for i, header in enumerate(headers):
            table += f"{header:{max_lengths[i]}}  "
        table += "\n"
        # Generate separator row
        for i, header in enumerate(headers):
            table += f"{'-'*max_lengths[i]}  "
        table += "\n"
        # Generate data rows
        for row in user_info:
            for i, value in enumerate(row):
                table += f"{value:{max_lengths[i]}}  "
            table += "\n"
        return table

    @expose
    # Task 3
    def add_author(self, author_name, author_genre):
        self.authors[author_name] = author_genre
        print(f"Author {author_name} added to the system with genre {author_genre}.")

    @expose
    # Task 4
    def return_authors(self):
        author_info = []
        for name, genre in self.authors.items():
            author_info.append([name, genre])
        headers = ["Name", "Genre"]
        max_lengths = [max(len(str(row[i])) for row in author_info) for i in range(len(headers))]
        table = ""
        # Generate header row
        for i, header in enumerate(headers):
            table += f"{header:{max_lengths[i]}}  "
        table += "\n"
        # Generate separator row
        for i, header in enumerate(headers):
            table += f"{'-'*max_lengths[i]}  "
        table += "\n"
        # Generate data rows
        for row in author_info:
            for i, value in enumerate(row):
                table += f"{value:{max_lengths[i]}}  "
            table += "\n"
        return table
    
    @expose
    # Task 5
    def add_book_copy(self, author_name, book_title):
        book = (author_name, book_title)
        if book in self.books:
            self.books[book] += 1
        else:
            self.books[book] = 1
            self.books_not_loan.add(book)
        print(f"A copy of '{book_title}' by {author_name} has been added to the system.")

    @expose
    # Task 6
    def return_books_not_loan(self):
        book_info = []
        headers = ["Author", "Title"]
        max_lengths = [len(header) for header in headers]
        table = ""
        # Generate header row
        for i, header in enumerate(headers):
            table += f"{header:{max_lengths[i]}}  "
        table += "\n"
        # Generate separator row
        for i, header in enumerate(headers):
            table += f"{'-'*max_lengths[i]}  "
        table += "\n"
        # Generate data rows
        for book in self.books_not_loan:
            author, title = book
            book_info.append([author, title])
        for row in book_info:
            for i, value in enumerate(row):
                table += f"{value:{max_lengths[i]}}  "
            table += "\n"
        return table
    
    @expose
    def loan_book(self, user_name, book_title, year, month, day):
        book = self.books.get(book_title)
        if book is None:
            return 0
        copies = book['copies']
        loaned_books = self.loaned_books.get(book_title, [])
        if copies <= len(loaned_books):
            return 0
        loan_date = datetime.date(year, month, day)
        self.loaned_books.setdefault(book_title, []).append({'user': user_name, 'loan_date': loan_date})
        return 1

    @expose
    def return_books_loan(self):
        books_on_loan = []
        for book_title in self.loaned_books:
            for loan in self.loaned_books[book_title]:
                books_on_loan.append((self.books[book_title]['author'], book_title, loan['user']))
        return books_on_loan

daemon = Pyro5.api.Daemon()
library_object = Library()

Pyro5.api.serve({library_object: "example.library"}, daemon=daemon, use_ns=True)
