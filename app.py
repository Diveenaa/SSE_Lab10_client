from flask import Flask, jsonify, request, render_template
import json
import requests
import os

app = Flask(__name__)

URL = os.getenv("URL")

@app.route('/home')
def home_page():
    response = requests.get(URL)
    if response.status_code == 200:
        books = response.json()
        return render_template("index.html")

@app.route('/')
def request_books():
    response = requests.get(URL)
    if response.status_code == 200:
        books = response.json()
        return books

@app.route('/books')
def filter_books(genre=None, id=None, title=None, year=None,author=None):
    args_list = list[genre, id, title, author, year]
    if all(v is None for v in args_list):
        genre = request.args.get('genre')
        id = request.args.get('min_id')
        title = request.args.get('title')
        year = request.args.get('min_year')
        author = request.args.get('author')

    books = request_books()
    books = books["books"]
    if id:
        resulting_books = [book for book in books if int(id) <= int(book['id'])]
        if len(resulting_books) == 0:
            return "No books found"
        return resulting_books

    if title:
        resulting_books = [book for book in books if title.lower() in book['title'].lower()]
        if len(resulting_books) == 0:
            return "No books found"
        return resulting_books

    if year:
        resulting_books = [book for book in books if int(year) <= int(book['publication_year'])]
        if len(resulting_books) == 0:
            return "No books found"
        return resulting_books

    if author:
        resulting_books = [book for book in books if author.lower() in book['author'].lower()]
        if len(resulting_books) == 0:
            return "No books found"
        return resulting_books

    if genre:
        resulting_books = [book for book in books if genre.lower() in book['genre'].lower()]
        if len(resulting_books) == 0:
            return "No books found"
        return resulting_books
    
    else:
        return request_books()

@app.route('/form_query', methods = ["POST"])
def get_form_input():
    query = request.form.get('searchType')
    text_input = request.form.get('searchInput')
    print(query)
    if query == 'genre':
        return filter_books(genre=text_input)
    if query == 'min_id':
        return filter_books(id=text_input)
    if query == 'min_year':
        return filter_books(year=text_input)
    if query == 'author':
        return filter_books(author=text_input)
    if query == 'title':
        return filter_books(title=text_input)
    else:
        return filter_books()
