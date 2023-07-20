import matplotlib

matplotlib.use('Agg')

import pandas as pd
import numpy as np
from flask import render_template,Flask,request
import matplotlib.pyplot as plt

app = Flask(__name__)
@app.route('/', methods = ['GET' , 'POST'])

def index():
    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        hospital = request.form.get('hospital')
        number = request.form.get('number')

        if blood_type:
            data = pd.read_csv("Database.csv")
            data_entry = {'Bloodtype': [blood_type], 'Hospital': [hospital], 'Contact Number': [number]}
            data_df = pd.DataFrame(data_entry)
            data_df.to_csv("Database.csv", mode='a', header=False, index=False)
            # A+- B+- AB=- , O+,0-
            data = pd.read_csv("Database.csv")
            data_blood_np = np.array(data['Bloodtype'])
            a_pos = 0
            ab_pos = 0
            b_pos = 0
            o_pos = 0
            a_neg = 0
            b_neg = 0
            ab_neg = 0
            o_neg = 0

            for n in range(len(data_blood_np)):
                if data_blood_np[n] == "A+":
                    a_pos += 1
                if data_blood_np[n] == "B+":
                    b_pos += 1
                if data_blood_np[n] == "AB+":
                    ab_pos += 1
                if data_blood_np[n] == "O+":
                    o_pos += 1
                if data_blood_np[n] == "A-":
                    a_neg += 1
                if data_blood_np[n] == "B-":
                    b_neg += 1
                if data_blood_np[n] == "AB-":
                    ab_neg += 1
                if data_blood_np[n] == "O-":
                    o_neg += 1

            y_list = [a_pos, b_pos, ab_pos, o_pos, a_neg, b_neg, ab_neg, o_neg]
            x_list = ["A+", "B+", "AB+", "O+", "A-", "B-", "AB-", "O-"]
            plt.clf()
            plt.bar(x_list, y_list)
            plt.savefig("static/images/plot.png")







    return render_template('index.html')

@app.route('/search' , methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        search_blood = request.form.get('search_blood')
        search_hosp = request.form.get('search_hosp')
        search_num = request.form.get('search_num')
        data = pd.read_csv("Database.csv")


        print("ALL DATA ")
        print(data)
        search_blood_np = np.array(data['Bloodtype'])
        search_hosp_np = np.array(data['Hospital'])
        search_num_np = np.array(data['Contact Number'])
#create an emplty list
        all_results = {}
        j = 0
        for i in range (len(search_blood_np)):
            if (search_blood_np[i] == search_blood):
                j += 1
                print("Found a match !")
                result = { 'Bloodtype' : (search_blood_np[i]), 'Hospital' : search_hosp_np[i] , 'Contact Number ' : search_num_np[i] }
                all_results[j] = result
                print(result)
        return render_template('results.html',result=all_results)




    return render_template('search.html')




if __name__ == '__main__':
    app.run(port=5000)



