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
        cur=query
        if(choice=='0'):
            #story
            query=request.session['prvs_prompts']=request.session['prvs_prompts']+'\n'+query
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
            query=request.session['prvs_prompts']=request.session['prvs_prompts']+'\n'+query+'->'
            response = openai.Completion.create(
            model="davinci:ft-personal-2022-11-17-22-42-18",
            prompt="What kinda porn do you watch? -> One's with you mom in it.\nDo you wanna come over and do it? -> No, I'm just not interested in sleeping with someone whose IQ is lower then their ballsack.\nDo you wanna come over and do it? -> When Hell freezes over.\n {} ->".format(query),
            temperature=0.3,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["->"]
            )
        if 'choices' in response:
            if len(response['choices']) > 0:
                answer = response['choices'][0]['text']
            else:
                answer = 'You are strong.'
        else:
            answer = 'You are strong.'
        request.session['prvs_prompts']=query+'\n'+answer+'\n'
        return render(request,'story.html',{'answer':answer,'choice':choice,'prompt':cur})        
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