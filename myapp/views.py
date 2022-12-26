import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

nextId = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is..'},
    {'id': 2, 'title': 'view', 'body': 'View is..'},
    {'id': 3, 'title': 'model', 'body': 'Model is..'},
]

def HTMLTemplate(articleTag, id=None):
    global topics

    items = ''
    for topic in topics:
        items += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <a href="/update/{id}">update</a>
            </li>
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id} />
                    <input type="submit" value="delete"/>
                </form>
            </li>
        '''

    return f'''
        <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {items}
            </ol>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
        </html>
    '''

def index(request):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):

    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"/></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"/></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))

    elif request.method == 'POST':
        global nextId
        topics.append({
            "id": nextId,
            "title": request.POST["title"],
            "body": request.POST["body"]
        })
        nextId += 1
        return redirect('/read/' + str(nextId - 1))

def read(request, id):
    global topics

    article = ''
    for topic in topics:
        if topic["id"] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def update(request, id):
    global topics

    selected = None
    for topic in topics:
        if topic["id"] == int(id):
            selected = topic
    if selected == None:
        logging.error("Topic doesn't exist")

    if request.method == 'GET':
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selected["title"]} /></p>
                <p><textarea name="body" placeholder="body">{selected["body"]}</textarea></p>
                <p><input type="submit"/></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))

    elif request.method == 'POST':
        data = request.POST
        for topic in topics:
            if topic["id"] == int(id):
                topic["title"] = data["title"]
                topic["body"] = data["body"]
        return redirect(f'/read/{id}')


@csrf_exempt
def delete(request):
    global topics

    id = request.POST["id"]
    temp = []
    for topic in topics:
        if topic["id"] != int(id): temp.append(topic)
    topics = temp

    return HttpResponse(HTMLTemplate(f"<h4>Deleted.</h4>"))