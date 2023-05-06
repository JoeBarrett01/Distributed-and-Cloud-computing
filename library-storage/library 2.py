# The following imports are required

import Pyro5.api
from Pyro5.api import expose, serve
import datetime
from datetime import date, timedelta

@expose
class Library:
    """
    A class used to represent a data storage system using a remote object paradigm

    Attributes
    ----------
    users : dict
        a formatted dictionary to keep track of users entering the library.
    authors : dict
        a formatted dictionary to keep track of authors inside the library.
    books : dict
        a formatted dictionary to keep track of books currently inside the library.
    loans : dict
        a formatted dictionary to keep track of which books are no longer in the library
        and have been removed by a specific user. 

    """
    def __init__(self):
        self.users = {}
        self.authors = {}
        self.books = {}
        self.loans = {}


    # task 1
    def add_user(self, user_name, user_number):
        """
        Adds user to Library

        Parameters
        ----------
        user_name: str
            representation of person's name in computer system.
        user_number: int
            unique user identification number. 
        """
        self.users[user_number] = user_name

    # task 2
    def return_users(self):
        """
        Formats and returns users who have been added to the library.
        """
        user_table = [["User ID", "User Name"]]
        for user_id, user_name in self.users.items():
            user_table.append([user_id, user_name])
        # Get the maximum width of each column
        col_widths = [max(len(str(row[i])) for row in user_table) for i in range(len(user_table[0]))]
        # Format the table
        formatted_table = ["  ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(user_table[0]))).rstrip() for row in user_table]
        # Add the underline
        formatted_table.insert(1, "-" * sum(col_widths) + "--")
        return "\n".join(formatted_table)

    # task 3
    def add_author(self, author_name, genre):
        """
        Adds Author to the library.

        Parameters
        ----------
        author_name: str
            name of author.
        genre: str
            genre of book that author wrote. 
        """
        self.authors[author_name] = genre

    # task 4
    def return_authors(self):
        """
        Formats author data and returns information in form of table.
        """
        author_table = [["Author", "Genre"]]
        for author, genre in self.authors.items():
            author_table.append([author, genre])
        # Get the maximum width of each column
        col_widths = [max(len(str(row[i])) for row in author_table) for i in range(len(author_table[0]))]
        # Format the table
        formatted_table = ["  ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(author_table[0]))).rstrip() for row in author_table]
        # Add the underline
        formatted_table.insert(1, "-" * sum(col_widths) + "--")
        return "\n".join(formatted_table)

    # task 5
    def add_book_copy(self, author_name, book_title):
        """
        Enables the library to accept a copy of a book. 

        Parameters
        ----------
        author_name: str
            name of author
        book_title: str
            title of book
        """
        key = (author_name, book_title)
        if key in self.books:
            self.books[key] += 1
            print(f"Added book copy: {author_name} - {book_title}")
        else:
            self.books[key] = 1
        
    # task 6
    def return_books_not_loan(self):
        """
        Formats and returns all information regarding a book not on loan. 
        """
        header = ("Author", "Book Title")
        data = [(author, book) for (author, book), count in self.books.items() if count > 0]
        
        # Get the width of the longest value in each column
        col_widths = [max(len(str(row[i])) for row in [header] + data) for i in range(len(header))]
        
        # Build the formatted output string
        output = ["".join("{:<{}}".format(header[i], col_widths[i]+2) for i in range(len(header)))]
        output.append("".join("-" * (w+2) for w in col_widths))
        for row in data:
            output.append("".join("{:<{}}".format(str(row[i]), col_widths[i]+2) for i in range(len(row))))
        
        return "\n".join(output)

    # task 7
    def loan_book(self, user_name, book_title, year, month, day):
        """
        Loans a copy of a specified book to a specified user on a specified date.

        Parameters
        ----------
        user_name: str
            name of user obtained from users.
        book_title: str
            name of book obtained from books.
        year: int
            4 digit date information.
        month: int
            2 digit date information.
        day: int
            2 digit date information.

        Return
        ------
        1 if the book in question was successfully loaned. 
        0 otherwise.
        """
        index = None
        for title, count in self.books.items():
            author, title_str = title
            if title_str == book_title and count > 0:
                index = title
                break
        if index is not None:
            self.books[index] -= 1
            loan = {"user": user_name, "date": (year, month, day)}
            if index in self.loans:
                self.loans[index].append(loan)
            else:
                self.loans[index] = [loan]
            return 1
        else:
            return 0

    # task 8
    def return_books_loan(self):
        """
        Returns all associated pieces of information relating to the set of book copies 
        currently on loan
        """
        loans = []
        for key, value in self.loans.items():
            for loan in value:
                loan_info = {
                    "Author Name": key[0],
                    "Book Title": key[1],
                    "User Name": loan["user"],
                    "Loan Date": loan["date"]
                }
                loans.append(loan_info)
        if not loans:
            return "No books on loan."
        else:
            # Create table header
            header = ["{:<15}".format(title) for title in loans[0].keys()]
            header_str = "|".join(header)
            header_underline = "|".join(["{:<15}".format("-" * len(title)) for title in loans[0].keys()])
            # Create table body
            rows = []
            
            for loan in loans:
                row = ["{:<15}".format(str(value)) for value in loan.values()]
                row_str = "|".join(row)
                rows.append(row_str)
            # Combine header and rows and return as string
            return f"{header_str}\n{header_underline}\n" + "\n".join(rows)

    # task 9
    def end_book_loan(self, user_name, book_title, year, month, day):
        """ 
        The user has now ended the book loan

        Parameters
        ----------
        user_name: str
            name of user 
        book_title: str
            name of book  
        year: int
            date info
        month: int
            date info
        day: int
            date info

        Return
        ------
         a loaned copy of a specified book by a specified user on a specified date;
        """
        for title, loans in self.loans.items():
            for loan in loans:
                if loan['user'] == user_name and title == book_title and loan['date'] == str(datetime.date(year, month, day)):
                    self.books[title] += 1
                    loans.remove(loan)
                    return 1
        return 0

    # task 10
    def delete_book(self, book_title):
            """
            Deletes books not on loan

            Parameters
            ----------
            book_title: str
                Title of book
            """
            # Iterate over all copies of the book
            for book in self.books:
                if book[0] == book_title:
                    # Check if the copy is currently on loan
                    is_on_loan = False
                    for loan in self.loans:
                        if loan.book == book and loan.return_date is None:
                            is_on_loan = True
                            break
                    if not is_on_loan:
                        # Delete the copy from the system
                        self.books.remove(book)

    # task 11
    def delete_user(self, user_id):
        """
        Deletes a user if they have never loaned a book

        Parameter
        ---------
        user_id: int
            identification number of user

        Return
        ------
            1 if user is delted. 
            0 Otherwise. 
        """
        if user_id in self.users:
            self.users.pop(user_id)
            return 1
        else:
            return 0

    # task 12
    def user_loans_date(self, user_name, start_year, start_month, start_day, end_year, end_month, end_day):
        """
        Return all book titles a user previously has loaned where the corresponding loan and
        return dates both lie between a specified start and end date inclusive
        
        Parameters
        ----------
        user_name: str
            name of user in system
        start_year: int
            4 digit year of starting loan.
        start_month: int
            month given by 1-12
        start_day: int
            day in month, represented by integer. 
        end_year: int
            4 digit year of ending loan. 
        end_month: int
            month given by 1-12
        end_day: int
            day of end loan given by integer. 
        
        """
        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)

        titles = []

        for key, loans in self.loans.items():
            author, title = key
            for loan in loans:
                loan_date = datetime.date(*loan['date'])
                return_date = datetime.datetime.strptime(loan.get('return_date', datetime.date.today().strftime('%Y-%m-%d')), '%Y-%m-%d').date()

                if loan['user'] == user_name and start_date <= loan_date <= end_date and start_date <= return_date <= end_date:
                    titles.append(title)

        if titles:
            formatted_titles = "\n- ".join(titles)
            return f"Books loaned by {user_name} between {start_date} and {end_date}:\n- {formatted_titles}"
        else:
            return f"No books loaned by {user_name} between {start_date} and {end_date}."


daemon = Pyro5.api.Daemon()
library_object = Library()

Pyro5.api.serve({library_object: "example.library"}, daemon=daemon, use_ns=True)