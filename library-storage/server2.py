import Pyro5.api
from Pyro5.api import expose, serve
import datetime

@expose
class Library:
    def __init__(self):
        self.users = {}
        self.authors = {}
        self.books = {}
        self.books_loan = {}
        self.loans = {}

    def add_user(self, name, user_number):
        self.users[user_number] = name

    def _format_table(self, rows):
        # Calculate the maximum width of each column
        col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]
        # Construct the format string for each row
        format_str = "  ".join("{{:<{}}}".format(width) for width in col_widths)
        # Construct the separator string for the headers
        sep_str = "  ".join("{{:<{}}}".format("-" * width) for width in col_widths)
        # Construct the output string with headers and rows
        output = ""
        for i, row in enumerate(rows):
            if i == 0:
                output += format_str.format(*row) + "\n"
                output += sep_str.format(*["" for _ in col_widths]) + "\n"
            else:
                output += format_str.format(*row) + "\n"
        return output
    
    def return_users(self):
        rows = [("User ID", "User Name")]
        rows += [(str(user_number), user_name) for user_number, user_name in self.users.items()]
        return self._format_table(rows)


    def add_author(self, author_name, genre):
        self.authors[author_name] = genre

    def return_authors(self):
        rows = [("Author Name", "Genre")]
        rows += [(author_name, genre) for author_name, genre in self.authors.items()]
        return self._format_table(rows)

    def add_book_copy(self, author_name, book_title):
        book_key = (author_name, book_title)
        if book_key not in self.books:
            self.books[book_key] = 0
        self.books[book_key] += 1

    def return_books_not_loan(self):
        rows = [("Author Name", "Book Title")]
        rows += [(author_name, book_title) for (author_name, book_title), count in self.books.items() if count > 0]
        return self._format_table(rows)

    def loan_book(self, user_name, book_title, year, month, day):
        key = (author_name, book_title)
        if key in self.books and self.books[key] > 0:
            self.books[key] -= 1
            return_date = datetime.date(year, month, day) + datetime.timedelta(days=14)
            loan = {"user": user_name, "date": str(return_date)}
            if key in self.loans:
                self.loans[key].append(loan)
            else:
                self.loans[key] = [loan]

    def return_books_loan(self):
        rows = [("Author Name", "Book Title", "User Name", "Return Date")]
        for (author_name, book_title), loans in self.loans.items():
            for loan in loans:
                user_name = loan["user"]
                return_date = loan["date"]
                rows.append((author_name, book_title, user_name, return_date))
        return self._format_table(rows)
    """
    def loan_book(self, user_name, book_title, year, month, day):
        book_key = (self.get_book_author(book_title), book_title)
        if book_key not in self.books or self.books[book_key] == 0:
            return "Book not available for loan"
        self.books[book_key] -= 1
        loan_date = datetime.date(year, month, day)
        loan_info = {"user": user_name, "date": loan_date}
        if book_key not in self.books_loan:
            self.books_loan[book_key] = []
        self.books_loan[book_key].append(loan_info)
    
    def get_book_author(self, book_title):
        for author, book in self.books.keys():
            if book == book_title:
                return author
        return None

    def return_books_loan(self):
        return self.books_loan
    """

daemon = Pyro5.api.Daemon()
library_object = Library()

Pyro5.api.serve({library_object: "example.library"}, daemon=daemon, use_ns=True)