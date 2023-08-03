# library.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship('Book', back_populates='category')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='books')

class Library:
    def __init__(self):
        engine = create_engine('sqlite:///database.db')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_book(self, title, author, category_name):
        category = self.session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
            self.session.commit()

        book = Book(title=title, author=author, category=category)
        self.session.add(book)
        self.session.commit()
        print("Book added successfully!")

    def display_books(self):
        books = self.session.query(Book).all()

        if not books:
            print("No books in the library.")
        else:
            print("Available books:")
            for book in books:
                status = "Available" if book.is_available else "Not Available"
                print(f"Title: {book.title}, Author: {book.author}, Category: {book.category.name}, Status: {status}")

    def issue_book(self, title):
        book = self.session.query(Book).filter_by(title=title, is_available=True).first()

        if book:
            book.is_available = False
            self.session.commit()
            print("Book issued successfully!")
        else:
            print("Book not available for issuing.")

    def return_book(self, title):
        book = self.session.query(Book).filter_by(title=title, is_available=False).first()

        if book:
            book.is_available = True
            self.session.commit()
            print("Book returned successfully!")
        else:
            print("Book already returned or not found.")

    def add_category(self, category_name):
        category = Category(name=category_name)
        self.session.add(category)
        self.session.commit()
        print("Category added successfully!")

    def display_categories(self):
        categories = self.session.query(Category).all()

        if not categories:
            print("No categories found.")
        else:
            print("Available categories:")
            for category in categories:
                print(f"Category: {category.name}")

    def __del__(self):
        self.session.close()

if __name__ == "__main__":
    library = Library()
    while True:
        print("\n Samuel's Library Management System")
        print("1. Display Books")
        print("2. Add Book")
        print("3. Return Book")
        print("4. Display Categories")
        print("5. Add Category")
        print("6. Issue Book")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            library.display_books()
        elif choice == '2':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            category_name = input("Enter book category: ")
            library.add_book(title, author, category_name)
        elif choice == '3':
            title = input("Enter the title of the book you are returning: ")
            library.return_book(title)
        elif choice == '4':
            library.display_categories()
        elif choice == '5':
            category_name = input("Enter category name: ")
            library.add_category(category_name)
        elif choice == '6':
            title = input("Enter the title of the book you want to issue: ")
            library.issue_book(title)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
