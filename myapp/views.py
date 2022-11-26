from django.shortcuts import redirect, render
from django.http import HttpResponse
from requests import request
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . models import Feature
import openai
def index(request):
    request.session['prvs_prompts']=''
    return render(request,'index.html')
def story(request):
    choice = request.POST['choice']
    if 'text' not in request.POST:
        request.session['prvs_prompts']=''
        return render(request,'story.html',{'choice':choice})
    else:
        openai.api_key = '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'
        query = request.POST['text']
        query=request.session['prvs_prompts']=request.session['prvs_prompts']+query
        if(choice=='0'):
            #story
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt="write a long story that includes these words and previous generated Prompts: {}".format(query),
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)
        elif(choice=='1'):
            #image
            response = openai.Image.create(
            prompt="{}".format(query),
            n=1,
            size="1024x1024"
            )
            image_url = response['data'][0]['url']
            return render(request,'showIm.html',{'url':image_url})
        else:
            response = openai.Completion.create(
            model="davinci:ft-personal-2022-11-17-22-42-18",
            prompt="{}".format(query),
            temperature=0.5,
            max_tokens=15,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0
            )
        if 'choices' in response:
            if len(response['choices']) > 0:
                answer = response['choices'][0]['text']
            else:
                answer = 'You are strong.'
        else:
            answer = 'You are strong.'
        return render(request,'story.html',{'answer':answer,'choice':choice,'prompt':query})        
def showIm(request):
    return render(request,'showIm.html')
def landingpage(request):
    f1=Feature()
    f2=Feature()
    f3=Feature()
    f1.name='Story Generation'
    f1.deatils='Generation of story based on current and previously generated prompts'
    f1.ids=0
    f2.name='Image Generation'
    f2.deatils='Generation of Images based on Prompt provided (Geared towards Creativeness'
    f2.ids=1
    f3.name='Sarcastic Bot'
    f3.deatils='Generation of Sarcastic/insulting answers based on prompt given (R-18!)'
    f3.ids=2
    features = [f1,f2,f3]
    return render(request,'landingpage.html',{'features':features})
def show(request):
    openai.api_key = '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'
    query = request.POST['text']
    choice = request.POST['choice']
    if(choice=='0'):
        #story
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt="write a long story that includes these words and previous generated Prompts: {}".format(query),
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)
    elif(choice=='1'):
        #image
        response = openai.Image.create(
        prompt="{}".format(query),
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return render(request,'showIm.html',{'url':image_url})
    else:
        response = openai.Completion.create(
        model="text-davinci-002",
        prompt="Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\nYou: What time is it?\nMarv:{}".format(query),
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
        )
    if 'choices' in response:
        if len(response['choices']) > 0:
            answer = response['choices'][0]['text']
        else:
            answer = 'You are strong.'
    else:
        answer = 'You are strong.'
    return render(request,'show.html',{'answer':answer,'choice':choice})
