from flask import Flask, jsonify, request, render_template
import mysql.connector
from config import DB_CONFIG
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

app = Flask(__name__)

# Create Database
def create_table():
    mydb = mysql.connector.connect(**DB_CONFIG)
    mycursor = mydb.cursor()
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS recommended_books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255),
            description TEXT
        )
    ''')
    mydb.commit()
    mycursor.close()
    mydb.close()

# Add Books
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    description = data.get('description')
    mydb = mysql.connector.connect(**DB_CONFIG)
    mycursor = mydb.cursor()
    sql = "INSERT INTO recommended_books (title, author, description) VALUES (%s, %s, %s)"
    val = (title, author, description)
    mycursor.execute(sql, val)
    mydb.commit()
    book_id = mycursor.lastrowid
    mycursor.close()
    mydb.close()
    logger.info("Succeed to add one book!")
    return jsonify({"id": book_id, "title": title, "author": author, "description": description}), 201

# Get Book Lists
@app.route('/books', methods=['GET'])
def get_books():
    mydb = mysql.connector.connect(**DB_CONFIG)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute('SELECT * FROM recommended_books')
    books = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return jsonify(books)

# Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    create_table()
    logger.info("Start the webapp!")
    app.run(debug=True, host='0.0.0.0', port=8080)
