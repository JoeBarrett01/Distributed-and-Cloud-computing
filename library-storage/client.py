import Pyro5.api

ns = Pyro5.api.locate_ns()
uri = ns.lookup("example.library")
rental_object = Pyro5.api.Proxy(uri)



rental_object.add_user("Conor Reilly", 123456)
print(rental_object.return_users())
rental_object.add_author("James Joyce", "fiction")
print(rental_object.return_authors())
rental_object.add_book_copy("James Joyce", "Ulysses")
print(rental_object.return_books_not_loan())
rental_object.loan_book("Conor Reilly", "Ulysses", 2019, 1, 3)
print(rental_object.return_books_loan())
rental_object.end_book_loan("Conor Reilly", "Ulysses", 2019, 2, 4)
rental_object.delete_book("Ulysses")
rental_object.delete_user("Conor Reilly")
print(rental_object.user_loans_date("Conor Reilly", 2010, 1, 1, 2029, 2, 1))