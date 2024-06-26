from  django.shortcuts import render,redirect
import numpy as np
import pandas as pd
import pickle
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User
from main.models import Detail_User_data1,Symptom,Contactus
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Symptom
from django.template.loader import get_template
import io


# Importing the datasets
sym_des = pd.read_csv("C:/Users/91983/Desktop/value/medical_1/datasets/symtoms_df.csv")
precaution_df = pd.read_csv("C:/Users/91983/Desktop/value/medical_1/datasets/precautions_df.csv")
workout_df = pd.read_csv("C:/Users/91983/Desktop/value/medical_1/datasets/workout_df.csv")
description_df = pd.read_csv("C:/Users/91983/Desktop/value/medical_1/datasets/description.csv")
medication_df = pd.read_csv("C:/Users/91983/Desktop/value/medical_1/datasets/medications.csv")
diets_df = pd.read_csv("C:/Users/91983/Desktop/value/medical_1/datasets/diets.csv")

# Loading the model
svc = pickle.load(open("C:/Users/91983/Desktop/value//medical_1/model/svc.pkl",'rb'))

def index(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user:
            login(request,user)
            return redirect("/prediction/")
        else:
            return render(request, 'login.html',{'msg':"Username or password is incorrect !!"})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        adhaar = request.POST.get('aadhaar')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm-password')
        mail = request.POST.get('mail')

        if password1 != password2:
            return render(request, 'signup.html', {'msg': 'Passwords do not match'})
        
        try:
            user = User.objects.create_user(username=name,password=password1)
            user.save()
            det_user = Detail_User_data1(user=user,age=age,adhaar_number=adhaar)
            det_user.save()
            user = authenticate(username=name, password=password1)
            # login(request, user)
            print("duhvkdvh")
            return render(request, 'signup.html',{'msg':"Data Saved Successfully !! "})
        except Exception as e:
            return render(request, 'signup.html', {'msg':"Username  already exist !! "})
    else:
        return render(request, 'signup.html')
    
            
def helper(dis):
    desc = description_df[description_df['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precaution_df[precaution_df['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medication_df[medication_df['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    diet = diets_df[diets_df['Disease'] == dis]['Diet']
    diet = [die for die in diet.values]

    workout = workout_df[workout_df['disease'] == dis]['workout']

    return desc,pre,med,diet,workout


symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

def get_predicted_value(symtom):
    input_vec = np.zeros(len(symptoms_dict))
    for item in symtom:
        input_vec[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vec])[0]]

def helper_functions(str):
    ls = []
    dot=0
    st1=""
    for item in str:
        if item=="'":
            if dot==1:
                dot=0
                ls.append(st1)
                st1=""
            else:
                dot=1
        if item!="'" and item!="[" and item!="]" and item!=",":
            st1+=item    
    return ls

def predictions(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            symptom = request.POST.get('symptom')
            user_symptoms = [s.strip() for s in symptom.split(',')]
            user_symptoms = [s.strip() for s in user_symptoms]
            predicted_disease = get_predicted_value(user_symptoms)
            print(predicted_disease)
            desc,pre,med,diet,workout = helper(predicted_disease)
            # med = helper_functions(med[0])
            # diet = helper_functions(diet[0])

            def convert_to_list_if_series(data):
                if isinstance(data, pd.Series):
                    return data.tolist()
                elif isinstance(data, np.ndarray):
                    return data.tolist()
                return data

            med2 = convert_to_list_if_series(med)
            diet2 = convert_to_list_if_series(diet)
            pre2 = convert_to_list_if_series(pre)
            workout2 = convert_to_list_if_series(workout)

            user = request.user
            
            med1 = str(med2[0])
            diet1 =  str(diet2[0])
            pre1 = str(pre2[0])
            workout1 = str(workout2)
            print(pre[0])
            sym_obj = Symptom(user=user,symptoms=user_symptoms,diet=diet1,workout=workout1,description=desc,medication=med1,precautions=pre1,disease=predicted_disease)
            sym_obj.save()
            res = sym_obj.id
            print("res : ",res)
            return render(request,'predicted.html',{'desc':desc,'pre':pre[0],'med':med,'diet':diet,'workout':workout,'symptom':res})
        else:
            return render(request,"prediction.html")
    else:
        return render(request,'login.html')

def aboutus(request):
    return render(request,"aboutus.html")

def logout_view(request):
    logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('/login/')

def contactus(request):
    if request.method =="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        contact_obj = Contactus(name=name, email=email, subject=subject, message=message)
        contact_obj.save()
        return render(request,'contactus.html')
    else:
        return render(request,"contactus.html")
    

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_pdf(request,symptom_id):
    symptom = get_object_or_404(Symptom, id=symptom_id)
    data = {
        'description': symptom.description,
        'disease':symptom.disease,
        'medications':symptom.medication,
        'diet':symptom.diet,
        'precautions':symptom.precautions,
        'workout':symptom.workout
    }
    pdf = render_to_pdf('pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def history(request):
    user = request.user.id
    symp_obj = Symptom.objects.filter(user_id=user).values()
    list_item = []
    for item in symp_obj:
        list_item.append(item)
    final_list = []
    for item in list_item:
        final_list.append(item)
    # print(final_list)
    # print(type(final_list[0]))
    return render(request, 'history.html',{'res':final_list})


        