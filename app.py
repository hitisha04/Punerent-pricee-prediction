from flask import Flask,request,render_template,redirect
from flask import request, render_template, url_for
from keras import models
import numpy as np
import pandas  as pd 
import pickle as pk
from PIL import Image
import string
import random
import os
import cgi
import cgitb #found this but isn't used?

form = cgi.FieldStorage()
app=Flask(__name__)
model=pk.load(open('static\model\my_model.pickle' ,'rb'))
encoder=pd.read_pickle("static\model\encoder1.pkl")

@app.route('/',methods=['GET','POST'])

def welcome():
    if request.method=='GET':
        return render_template('index.html',seller_type=seller_type,layout_type=layout_type,property_type=property_type,locality=locality,furnish_type=furnish_type)
    if request.method == "POST":
        sel_type=request.form['seller']
        lay_type=request.form['layout']
        pro_type=request.form['Propert']
        loc_type=request.form['localit']
        fur_type=request.form['furnish']
        bathroom=int(request.form['bathroom'])
        bedroom=int(request.form['bedroom'])
        area=int(request.form['Area'])
        vals=['seller_type', 'bedroom', 'layout_type', 'property_type', 'locality', 'area', 'furnish_type', 'bathroom']
        data=pd.DataFrame([ [sel_type,bedroom,lay_type,pro_type,loc_type,area,fur_type,bathroom]],columns=vals)
        data['layout_type']=data['layout_type'].replace(to_replace=['BHK', 'RK'],value=[2,1])
        data['furnish_type']=data['furnish_type'].replace(to_replace=['Unfurnished', 'Semi-Furnished', 'Furnished'],value=[1,2,3])
        data['property_type']=data['property_type'].replace(to_replace=['Independent Floor', 'Apartment', 'Studio Apartment', 'Villa',
       'Independent House', 'Penthouse'],value=[3,2,1,5,4,6])
        data=encoder.transform(data)
        price=data
        price=model.predict(price)
        price=int(price[0]*1.5)//100
        price=price*100
       

        return render_template('dex.html',sel_type=sel_type,lay_type=lay_type,pro_type=pro_type,loc_type=loc_type,fur_type=fur_type,bathroom=bathroom,bedroom=bedroom,area=area,price=price)
    
   

seller_type=['OWNER', 'AGENT', 'BUILDER']
layout_type=['BHK', 'RK']
property_type=['Independent Floor', 'Apartment', 'Studio Apartment', 'Villa',
       'Independent House', 'Penthouse']
locality=['Mundhwa', 'Wakad', 'Wagholi', 'Kothrud', 'Yerawada', 'Ganj Peth',
       'Pimple Saudagar', 'Hinjewadi', 'Dhanori', 'Nigdi', 'Bopkhel',
       'Viman Nagar', 'Dhayari', 'Pimple Nilakh', 'Chakan', 'Chinchwad',
       'Kharadi', 'Kalyani Nagar', 'Ravet', 'Lohegaon', 'Parvati Darshan',
       'Chikhali', 'Baner', 'Pimple Gurav', 'Bhosari', 'Undri', 'Dighi',
       'Sus', 'Hadapsar', 'Sinhgad Road', 'Tathawade', 'Ambegaon 1',
       'Karve Nagar', 'Bavdhan', 'Warje', 'Kondhwa', 'Manjari', 'Daund',
       'Manjari Budruk', 'Wadegaon', 'New Sangavi', 'Pimpri', 'Alandi',
       'Gahunje', 'Wadgaon Sheri', 'Sopan Baug', 'Katraj', 'Bhawani Peth',
       'Anand Nagar', 'Siddharth nagar', 'Thergaon', 'Talwade',
       'Tingre Nagar', 'Akurdi', 'Sangamvadi', 'Pirangut', 'Kasba Peth',
       'Wanowrie', 'Aundh', 'Balewadi', 'Handewadi', 'New Kalyani Nagar',
       'Punawale', 'Fursungi', 'Budhwar Peth', 'Dhayari Phata',
       'Talegaon Dabhade', 'Ambegaon Budruk', 'Pashan', 'Rahatani',
       'hingne Khurd', 'NIBM Annex Mohammadwadi', 'Ganesh Nagar',
       'Magarpatta', 'Wanwadi', 'Ghorpadi', 'Koregaon Park',
       'Vadgaon Budruk', 'Chandan Nagar', 'Mahalunge', 'Shewalewadi',
       'Vishrantwadi', 'Hinjewadi Phase 1', 'Ambegaon Pathar',
       'Shivaji Nagar', 'Khadki', 'Manjari Khurd', 'Agalambe', 'Nanded',
       'Charholi Budruk', 'Shivane', 'Bhugaon', 'Rasta Peth',
       'Kondhwa Budruk', 'NIBM Annexe', 'Mohammed wadi', 'Sinhagad Fort',
       'Ashok Nagar', 'Perugate', 'Morwadi', 'Sunarwadi', 'Khadakwasla',
       'Old Sangvi', 'Dhankawadi Police Station Road', 'Erandwane',
       'Dhaygude Wada', 'Karegaon', 'Nere', 'Bibwewadi', 'Moshi',
       'Yashwantnagar', 'Fatima Nagar', 'Bhukum', 'Koregaon Bhima',
       'Deccan Gymkhana', 'Sheela Vihar Colony', 'Sasane Nagar',
       'Kalewadi', 'Warje Malwadi', 'Jambhe', 'Shukrawar Peth',
       'Bhegade Aali', 'Vakil Nagar', 'Rambaug Colony', 'Sadashiv Peth',
       'Shaniwar Peth', 'Sanaswadi', 'bavdhan patil nagar', 'Bund Garden',
       'Vikas Nagar', 'Gultekdi', 'Vadgaon', 'Narhe', 'Talegaon',
       'Balaji Nagar', 'Pimpri Chinchwad', 'Mangawadi', 'Dattwadi',
       'Ubale Nagar', 'DP Road', 'Shinde Vasti', 'Nigdi Sector 24',
       'Vishal Nagar', 'Baramati', 'Law College Road', 'Dange Chowk',
       'Keshav Nagar', 'Bopodi', 'Koregaon Park Annexe', 'Satara road',
       'Ghorapdi', 'Akurdi Chowk', 'Dhanakwadi', 'Pradhikaran Nigdi',
       'Yamuna Nagar', 'Shivtirth Nagar', 'Happy Colony', 'Somwar Peth',
       'Ideal Colony', 'Chinchwad Gaon', 'NIBM', 'Jambhulwadi Road',
       'Handewadi Road', 'Pisoli Road', 'bhusari colony',
       'Wadgaon Budruk', 'Paud Road', 'Chikhali Sector 16',
       'Bhairav Nagar', 'Dhanukar Colony', 'Karve Road Kothrud',
       'Wagholi Road', 'Vijay Nagar', 'Kalewadi Phata PimpriChinchwad',
       'Adarsh Nagar Kiwale', 'Kothrud Depot Road', 'Vanaz corner',
       'Ramkrishna Paramhans Nagar', 'Bhelkenagar', 'Chandani Chowk',
       'Eklavya Colony', 'Dhole Patil Road', 'Awhalwadi', 'Kasarwadi',
       'Satar Nagar', 'Lulla Nagar', 'Kausar Baugh', 'Salunke Vihar',
       'Vishal Nagar Main', 'Kolwadi', 'Loni Kalbhor',
       'Bhusari colony right', 'Bhusari colony left', 'Kharadi bypass',
       'Bharati Vidyapeeth', 'Market yard', 'Kalyani Nagar Annexe',
       'Wanawadi Gaon', 'Dehu Road Cantonment', 'Dattavadi',
       'Ambegaon PuneMumbai Hwy', 'Bibwewadi Kondhwa Road', 'Mamurdi',
       'Mulshi', 'Walvekar Nagar', 'BT Kawde', 'Dhankawadi',
       'Kondhwa Khurd', 'Sukhsagar Nagar', 'Shikshak nagar',
       'Pune Satara Road', 'Dhankawadi Road', 'katraj kondhwa road',
       'Kirkatwadi', 'Dhamalwadi Bhekrai Nagar', 'Boat Club Road',
       'Gururaj Society', 'Sector No1 Bhosari', 'Shantiban Society',
       'Teen Hatti Chowk Road', 'Sahakar Nagar II', 'Mohan Nagar',
       'Pune Satara Rd', 'Bharati Vidyapeeth Campus', 'Wakad Pune',
       'Pune Solapur Road', 'Taljai Road', 'Hadapsar Gaon',
       'Wagholi Kesnand Wadegaon Road', 'Yewalewadi',
       'Dashrath Nagar Bhekrai Nagar', 'Raviwar Peth', 'Baner Road',
       'Mahalunge Ingale', 'Someshwarwadi', 'Baner Pashan Link Road',
       'Manjri Village Road', 'Laxman Nagar', 'Rajas Society',
       'National Society', 'Ganesh Peth', 'Jambhul', 'ITI road',
       'L&T Labour Colony', 'Kokane Mala', 'AWHO Hadapsar Colony',
       'Jagdishnagar', 'Subhas Nagar', 'Pandhari Nagar', 'Kranti Nagar',
       'Baner Hill Trail', 'Santhosh Nagar', 'Wakad Chowk Road',
       'Shivajinagar', 'Elite 27', 'Narayan Peth', 'Madhav Nagar',
       'Vardhaman Township Sasane Nagar', 'Dahanukar Colony',
       'MAE Campus', 'Vittalvadi', 'SNBP School Road',
       'Blue Ridge   Paranjpe Schemes', 'Vishal nagar square new dp road',
       'Tilekar Nagar', 'Om Colony', 'Model Colony', 'Prabhat Road',
       'Bhandarkar Road', 'paud', 'Tulaja Bhawani Nagar',
       'Skylights Road', 'EON Free Zone', 'Pune Station',
       'Salunke Vihar Road', 'Sainath Nagar',
       'Megapolis Sunway Internal Road', 'Vascon Paradise Society',
       'Mukai Nagar', 'Ramtekdi Industrial Area', 'kesnand',
       'Vadgoan Sheri Rajendri Nagar', 'Sakal Nagar', 'Uttam Nagar',
       'Siddartha Nagar', 'Phase 2', 'Pisoli', 'Nerhe',
       'Balewadi High Street', 'Kondhwa Budrukh', 'Balewadi Phata',
       'Madhala Vada', 'Salisbury Park', 'Swargate', 'Jambhulwadi',
       'Pune Cantonment', 'Marunji', 'Munjaba Vasti', 'Mukesh Nagar',
       'KondhwaUndriSaswad Road', 'Vasant Vihar', 'Marvel Fria Road',
       'Tapodham', 'Sindhi Colony', 'Gokhalenagar', 'Anand Tirth Nagar',
       'Guruwar Peth', 'Kalwad', 'Baderaj Colony',
       'Shedge Vasti PimpriChinchwad', 'Marunji Road', 'Satavwadi',
       'Nimbalkar Nagar Lohgaon', 'Adarsh Nagar Lohgaon',
       'Varsha Park Society', 'Vallabh Nagar', 'Maan', 'Gulab Nagar Pune',
       'Camp', 'Netaji Nagar', 'BT Kawade Road',
       'Satyapuram Co operative Housing Society', 'Shastri Nagar',
       'Bodkewadi', 'New DP Road', 'Murlidhar Housing Society',
       'Pan Card Club Road', 'Pratibha Nagar', 'New Sanghvi',
       'Sanjay Park', 'chintamani park', 'Munjaba Basti', 'Sharad Nagar',
       'Mundhwa Kharadi Road', 'Sahakar Nagar', 'Varale Pune', 'Kanhe',
       'Indryani nagar', 'Tukaram Nagar', 'Kalewadi Pandhapur Road',
       'Mayur Nagari', 'Senapati Bapat Road', 'Lokmanya Nagar',
       'Jangali Maharaj Road', 'Kondwa khurd road', 'Purnanagar',
       'Balewadi Gaon', 'Empire Estate Phase 1',
       'Shree Sidhivinayaka Nagri', 'Sector 27 Pradhikaran',
       'Nehru Nagar', 'Hanuman Nagar', 'Siddharth Residency', 'Bakhori',
       'Kolte Patil', 'Uruli Devachi', 'Sky Water Road',
       'Sadhu Vaswani Chowk', 'mandai', 'Vadgaon Sheri', 'Porwal Rd',
       'Amar Srushti', 'Phursungi Village Road', 'Dehu', 'Shikrapur',
       'Blue Ridge Approach Road', 'Bopdev Ghat', 'Veerbhadra Nagar',
       'Nigdi Sector 26', 'sinhagad road', 'Dapodi', 'Kunal Icon Road',
       'Mukund Nagar', 'aranyeshwar', 'maharshi nagar', 'Padmavati',
       'Tilak Road', 'Shankarseth Road', 'Shankar Sheth Rd',
       'Shree Sant Eknath Nagar', 'Sant Nagar',
       'Yashwantrao Chavan Nagar', 'Chhatrapati Sambhaji Nagar',
       'Pashan Sus Road', 'Pune Nagar Road', 'Manaji Nagar',
       'Deshmukhwadi', 'Kutwal Colony', 'Garmal', 'Kale Padal',
       'Shindenagar', 'MG Road', 'Wakadkar Wasti', 'Narayangaon',
       'Ram Nagar', 'Kaspate Vasti', 'Kaspate Vasti Road',
       'Vanaz Corner Pedestrian Crossing', 'Maval', 'Pratik Nagar',
       'Kothrud Bus Stand Road', 'Yashwant Nagar', 'Udyog Nagar',
       'Gujrat Colony', 'Ghule Vasti', 'Sector 29', 'Lonikand',
       'Old Sanghvi', 'Dattanagar', 'Bhoirwadi', 'Ranjangaon',
       'Laxmi Chowk Road', 'Bhau Patil Road', 'Bhumkar Das Gugre Road',
       'Marutirao Gaikwad Nagar', 'Mundhwa Manjari Road', 'Saswad',
       'Indrayani Nagar Sector 2', 'Walhekarwadi Chinchwad',
       'Jawalkar Nagar', 'Olkaiwadi', 'Pandav Nagar', 'Kolhewadi',
       'Kiwale', 'Wadarvadi', 'Shirgaon', 'Junnar', 'Sant tukaram Nagar',
       'Rajgurunagar', 'Mangdewadi', 'Gananjay Society Chaitanya Nagar',
       'wadebolhai', 'Somatane', 'Nanded Phata', 'Karve Road Erandwane',
       'Vitthal Wadi', 'Giridhar Nagar', 'Dadachi Wasti',
       'Kondhawe Dhawade', 'Kamshet', 'bhekarai nagar', 'Modi Colony',
       'Chandkhed', 'Shirur', 'Yerwada Village', 'Valvan Lonavla',
       'Dehu Phata', 'Pangoli', 'Digambar Nagar', 'Hingne Budrukh',
       'Bakori Road', 'Tukai Darshan', 'Saibaba Nagar',
       'Mohan Nagar MIDC', 'Indrayani Nagar', 'Talegaon Dhamdhere',
       'Renuka Nagar', 'Gananjay Society', 'Aundh Gaon']
furnish_type=['Unfurnished', 'Semi-Furnished', 'Furnished']












if __name__=='__main__':
    app.run(debug=True)

