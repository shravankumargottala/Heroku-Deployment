import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/',methods=['GET','POST'])
def home():   
   laptop_name = ['HP', 'Lenovo', 'Dell', 'Asus']
   ram_size = [4,6,8,12,16]
   processor_type = ['Core i3 7100U', 'Core i5 7200U', 'Core i3', 'Core i5 8250U',
       'Core i5', 'Core i3 8130U', 'Core i5 6200U', 'Core i3-5005U',
       'Core i7', 'Core i5 8300H']
   processor_brand = ['Intel']
   os_sys = ['Windows 10, Home', 'DOS', 'Windows 10',
       'Windows 10 Home High End', 'Linux']
   mem_tech = ['DDR4', 'DDR3', 'DDR4, Optane', 'DDR3L']
   return render_template('index.html',laptop_name=laptop_name,ram_size=ram_size,processor_type=processor_type,processor_brand=processor_brand,os_sys=os_sys,mem_tech=mem_tech)

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    lp_nm =""
    Laptop_replace_values = {'HP':0, 'Lenovo':1, 'Dell':2, 'Asus':3}
    processor_type_replace_values = {'Core i3':0, 'Core i3-5005U':1,'Core i3 7100U':2, 
                                     'Core i3 8130U':3,'Core i5':4, 'Core i5 6200U':5,'Core i5 7200U':6,
                                     'Core i5 8250U':7,'Core i5 8300H':8,'Core i7':9}
    
    processor_brand_replace_values = {'Intel':0}
    
    os_rplace_values = {'Windows 10':0, 'Windows 10, Home':1, 
           'Windows 10, Home High End':2, 'DOS':3,'Linux':4}
    
    mem_tech_replace_values = {'DDR3':0,'DDR3L':1,'DDR4':2, 'DDR4, Optane':3}   
    
    if request.method == 'POST':
       lp_nm = request.form['laptop_name']
       proc_type = request.form['processor_type']
       proc_brand = request.form['processor_brand']
       os_name = request.form['oper_sys']
       mem_tech = request.form['memory_tech']
       screen_sz = request.form['scr_size']
       lp_weight = request.form['lp_weight']
       hd_size = request.form['hd_size']
       procc_speed = request.form['procc_speed']
       ram_size = request.form['ram_size']
       print("laptop name is ",lp_nm,Laptop_replace_values[lp_nm],screen_sz)
       int_features = [Laptop_replace_values[lp_nm],lp_weight,ram_size,hd_size,procc_speed,
                       processor_type_replace_values[proc_type],screen_sz,processor_brand_replace_values[proc_brand],
                       os_rplace_values[os_name],mem_tech_replace_values[mem_tech]]
       print(int_features)
       final_features = [np.array(int_features)]
       print(final_features)
       prediction = model.predict(final_features)

       output = round(prediction[0], 2)

       return render_template('result.html', prediction_text='Laptop Price should be INR {}'.format(output))
   

if __name__ == "__main__":
    app.run(debug=True)