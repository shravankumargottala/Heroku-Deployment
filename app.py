import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/',methods=['GET','POST'])
def home():   
   laptop_name = ['Asus', 'Lenovo', 'Dell', 'HP']
   ram_size = [4,8]
   processor_type = ['Core i3', 'Core i5 8250U', 'Core i3 7100U',
       'Core i3 8130U', 'Core i3-5005U', 'Core i5 7200U', 'Core i5 6200U',
       'Core i7', 'Core i5 8300H', 'Core i7 8750H', 'Core i5']
   processor_brand = ['Intel']
   os_sys = ['Windows 10 Home', 'DOS', 'Linux', 'Windows 10']
   mem_tech = ['DDR3', 'DDR3L', 'DDR4 SDRAM', 'DDR DRAM', 'GDDR4',
       'DDR SDRAM', 'GDDR5','DDR4']
   return render_template('index.html',laptop_name=laptop_name,ram_size=ram_size,processor_type=processor_type,processor_brand=processor_brand,os_sys=os_sys,mem_tech=mem_tech)

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    lp_nm =""
    Laptop_replace_values = {'Asus':0, 'Lenovo':1, 'Dell':2, 'HP':3}
    processor_type_replace_values = {'Core i3':0, 'Core i5':1, 'Core i5 8250U':2, 'Core i3 7100U':3,
       'Core i3 8130U':4, 'Core i3-5005U':5, 'Core i5 7200U':6, 'Core i5 6200U':7,
       'Core i7':8, 'Core i5 8300H':9, 'Core i7 8750H':10}
    
    processor_brand_replace_values = {'Intel':0}
    
    os_rplace_values = {'Windows 10 Home':0, 'DOS':1, 'Windows 10':2, 'Linux':3}
    
    mem_tech_replace_values = {'DDR4':0, 'DDR3':1, 'DDR3L':2, 'DDR4 SDRAM':3, 'DDR DRAM':4, 'GDDR4':5,
       'DDR SDRAM':6, 'GDDR5':7}   
    
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
       int_features = [Laptop_replace_values[lp_nm],lp_weight,int(ram_size),hd_size,procc_speed,
                       processor_type_replace_values[proc_type],screen_sz,processor_brand_replace_values[proc_brand],
                       os_rplace_values[os_name],mem_tech_replace_values[mem_tech]]
       print(int_features)
       final_features = [np.array(int_features)]
       print(final_features)
       prediction = model.predict(final_features)

       output = round(np.expm1(prediction[0]),2)
	   
	   
       return render_template('result.html', lop_nm='Laptop Brand name : {}'.format(lp_nm),proc_type='Process Type : {}'.format(proc_type),proc_brand='Process Name : {}'.format(proc_brand),os_name='Operating System : {}'.format(os_name),mem_tech='System Memory Technology : {}'.format(mem_tech),screen_sz='Laptop Screen Size : {} Inches'.format(screen_sz),lp_weight='Laptop Weight : {} Kg'.format(lp_weight),hd_size='Hard Disk Size : {} GB'.format(hd_size),procc_speed='Processing Speed : {} GHzs'.format(procc_speed),ram_size='Ram Size : {} GB'.format(ram_size),prediction_text='{} Laptop Price for the above Specifications will be ₹ {}/-'.format(lp_nm,output))
   

if __name__ == "__main__":
    app.run(debug=True)
