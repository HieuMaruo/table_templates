from flask import Flask, render_template, jsonify, request
import pandas as pd
from models import Page
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['test_db']
pages = db.page

@app.route("/")
def hello():

    return render_template('index.html')

@app.route('/get_data', methods = ['GET'])
def data():
    df = pd.read_csv('/home/jdoz/Downloads/G-Army Comb - Sheet1.csv')
    x = df['Release'].tolist()
    x = [str(i).encode('utf-8').decode('ascii', 'ignore') for i in x]
    y = df['Total RICE'].tolist()
    return jsonify({'xs':x,'ys':y})

@app.route('/scatter', methods = ['GET'])
def scat():
    df = pd.read_pickle('/home/jdoz/Downloads/ERPs/Combined_Data_RICE_LMH_1020.pkl')
    group = df.groupby('Program')
    dataset = []
    colors = ['rgba(22, 159, 132, 0.59)','rgba(46, 204, 113, 0.63)','rgba(155, 89, 182, 0.62)','rgba(41, 128, 185, 0.57)']
    for i,color in zip(group,colors):
        label = i[0]
        xs = i[1]['Total RICE']
        ys = i[1]['Total Hours']
        data = [{'x':x,'y':int(y)} for x,y in zip(xs, ys)]
        dset = {'label':label, 'backgroundColor':color, 'pointRadius':10, 'data':data}
        dataset.append(dset)


    return jsonify({'dataset':dataset})

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/db')
def database():
    return render_template('page.html')

@app.route('/db/data', methods = ['GET'])
def db_data():
    data = db.page
    output = []
    for page in data.find({"archived":{'$ne': True}}):
        output.append({'url' : page['url'],
                                  'status' : page['status'],
                                  'keyword' : page['keyword'],
                                  'last_updated' : page['last_updated']})

    return jsonify({'data':output})

@app.route('/db/data/update', methods = ['GET','POST'])
def add_data():
    data = request.get_json('page')
    if data['page']:
        for post in data['page']:
            record = Page.objects(keyword = post['keyword']).update_one(
                        set__status = post['status'],
                        set__url = post['url'],
                        upsert = True)
    return render_template('page.html')

@app.route('/db/data/delete', methods = ['POST','PUT'])
def delete_record():
    page = request.get_json('row')['row']
    record = Page.objects(keyword = page['keyword']).update_one(set__archived = True, upsert = True)
    return render_template('page.html')




if __name__ == "__main__":
    app.run()
