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

def filter_books(books=None, genre=None, id=None, title=None, year=None,author=None):
    if books == None:
        books = request_books()["books"]
   
    resulting_books = books

    if id:
        resulting_books = [book for book in resulting_books if int(id) <= int(book['id'])]

    if title:
        resulting_books = [book for book in resulting_books if title.lower() in book['title'].lower()]

    if year:
        resulting_books = [book for book in resulting_books if int(year) <= int(book['publication_year'])]

    if author:
        resulting_books = [book for book in resulting_books if author.lower() in book['author'].lower()]

    if genre:
        resulting_books = [book for book in resulting_books if genre.lower() in book['genre'].lower()]

    return resulting_books

@app.route('/books')
def filter_books_route(genre=None, id=None, title=None, year=None,author=None):
    queries = [genre, id, title, year, author]
    if all(query is None for query in queries):
        genre = request.args.get('genre')
        id = request.args.get('min_id')
        title = request.args.get('title')
        year = request.args.get('min_year')
        author = request.args.get('author')

    resulting_books = filter_books(genre=genre, id=id, title=title, year=year, author=author)

    if len(resulting_books) == 0:
        return "No books found"
    
    return resulting_books

@app.route('/form_query', methods = ["POST"])
def get_form_input():
    query = request.form.get('searchType')
    text_input = request.form.get('searchInput')
    if query == 'genre':
        return filter_books_route(genre=text_input)
    if query == 'min_id':
        return filter_books_route(id=text_input)
    if query == 'min_year':
        return filter_books_route(year=text_input)
    if query == 'author':
        return filter_books_route(author=text_input)
    if query == 'title':
        return filter_books_route(title=text_input)
    else:
        return filter_books_route()