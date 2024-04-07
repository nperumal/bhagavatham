from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('src/data/bhagavatam.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Update the row with the new values
        cursor.execute('UPDATE translation SET column1 = ?, column2 = ? WHERE id = ?',
                       (request.form['column1'], request.form['column2'], id))
        conn.commit()
        return 'Row updated.'

    else:
        # Get the current values of the row
        cursor.execute('SELECT poem_translation, poemtitle_translation, context_translation, meaning_translation, 	antidote_translation  FROM translation  WHERE id = ?', (id,))
        row = cursor.fetchone()
        return render_template('edit.html', id=id, row=row)

if __name__ == '__main__':
    app.run(debug=True)