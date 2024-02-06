from django.shortcuts import render
from .models import Blog

import openai, os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('OPENAI_KEY', None)

def home(request):
    return render(request, 'portal/home.html')
    

def salary_calculator(request):

    tax_credit = 0
    salary = 0
    gross_paya = 0
    paya = 0
    usc = 0

    if request.method == 'POST':
        if request.POST.get('tax_credit') == "":
            tax_credit = 312.50
        else:
            tax_credit = request.POST.get('tax_credit')
            tax_credit = float(tax_credit)
            tax_credit = tax_credit / 12

        if request.POST.get('salary') is not None:
            if request.POST.get('salary') == "":
                salary = 0
            else:
                salary = request.POST.get('salary')
        

    tax_credit = float(tax_credit)

    salary = float(salary)
        
        
    if salary <= 3500:
        gross_paya = salary * 0.2
    else:
        gross_paya = (3500 * 0.2) + (0.4 * (salary - 3500))

    if gross_paya <= 312.50:
        paya = 0
    else:
        paya = gross_paya - tax_credit

    if salary <= 1001:
        usc = salary * 0.005
    elif 1001 < salary <= 2147.66:
        usc = 5.005 + ((salary - 1001) * 0.02)
    elif 2147.66 < (salary) <= 5837:
        usc = 5.005 + 22.933 + ((salary - 2147.66) * 0.04)
    else:
        usc = 5.005 + 22.933 + 147.58 + ((salary - 5837) * 0.08)

    employer_prsi = salary * 0.1105
    employee_prsi = salary * 0.04

    net_salary = (salary - paya - usc - employee_prsi)
                       
    salary = format(salary, ".2f")
    gross_paya = format(gross_paya, ".2f")
    tax_credit = format(tax_credit, ".2f")
    paya = format(paya, ".2f")
    usc = format(usc, ".2f")
    employee_prsi = format(employee_prsi, ".2f")
    employer_prsi = format(employer_prsi, ".2f")
    net_salary = format(net_salary, ".2f")

    context = {
        'gross_salary': salary,
        'gross_paya': gross_paya,
        'tax_credit': tax_credit,
        'paya': paya,
        'usc': usc,
        'employee_prsi': employee_prsi,
        'employer_prsi': employer_prsi,
        'net_salary': net_salary,
    }
    
    return render(request, 'portal/salary_calculator.html', context)

def translator(request):

    chatbot_response = ""
    user_input = ""
    context = {}
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        user_input2 = request.POST.get('language')
        #prompt = user_input
        prompt = f'Translate text provided to {user_input2}: {user_input}'
        #prompt = f"If the question is related to weather answer it: {user_input}, else say. Can't answer this"


        response = openai.completions.create (
            model= 'gpt-3.5-turbo-instruct',
            prompt= prompt,
        )

        #print(response)
        chatbot_response = response.choices[0].text
        if user_input == "":
            chatbot_response = ""

        context = {
            "response": chatbot_response,
            "question": user_input,
        }


    return render(request, 'portal/translator.html', context)


def blog(request):

    posts = Blog.objects.all()
    return render(request, 'portal/blog.html', {'posts': posts})

def post(request, pk):
    post = Blog.objects.get(id=pk)
    return render(request, 'portal/post.html', {'post': post})