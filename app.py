from flask import Flask, jsonify, request

app = Flask(__name__)
data = [{
    'title': '20.000 лье под водой',
    'author': 'Жюль Верн'
}, {
    'title': 'Война и мир',
    'author': 'Лев Толстой'
}]


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:book_id>')
def books(book_id=None):
    if request.method == 'POST':
        data.append({
            'author': request.form['author'],
            'title': request.form['title'],
        })
        return jsonify(success=1)
    else:
        if book_id is not None and 0 <= book_id < len(data):
            return jsonify(data[book_id])
        else:
            return jsonify(data)


app.run()
