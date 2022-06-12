
from flask import Flask,render_template
from matplotlib.style import context
import pandas as pd
import numpy as np
import pickle
pt = pickle.load(open('pickle/pt.pkl','rb'))
books = pickle.load(open('pickle/books.pkl','rb'))
recoms_df = pickle.load(open('pickle/recoms.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_csv('csv/av_books.csv')
    return render_template('index.html',column_names = df.columns.values,row_data = list(df.values.tolist()),zip=zip)

@app.route('/top')
def top():
    df = pd.read_csv('csv/top_ten.csv')
    return render_template('top.html',column_names = df.columns.values,row_data = list(df.values.tolist()),zip=zip)

@app.route('/detail/<id>')
def detail(id):
    df = pd.read_csv('csv/av_books.csv')
    id = int(id)
    
    book = df.loc[df['Index'] == id].values[0]
    data = []
    movie_name = book[1]
    index = np.where(pt.index==movie_name)[0][0]
    movies_ind = sorted(list(enumerate(recoms_df[index])),key=lambda x: x[1],reverse=True)[1:6]
    for i in movies_ind:
        
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)
        data.append(item)
        
    # print(data) 
    return render_template('recommend.html',book=book,data=data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)