from bottle import route, get, post, run, template, error, static_file, request, response, redirect
import json

def read_wikis_from_file():
    '''skapar en fil om det inte finns en'''
    try:
        my_file = open("wikis.json", "r")
        wikis = json.loads(my_file.read())
        my_file.close()

        return wikis
    except FileNotFoundError:
        my_file = open("wikis.json", "w")
        my_file.write(json.dumps([]))
        my_file.close()

        return []

def create_id(wikis):
    '''skapar ett id for wikis'''
    highest_id = 1
    for wiki in wikis:
        if wiki["id"] >= highest_id:
            highest_id = wiki["id"] + 1
    
    return highest_id

@route('/')
def index():
    '''default route'''
    return template('index',wikis=read_wikis_from_file())

@route('/new/')
def new_post():
    '''går till formula som man kan skapa en ny fil'''
    return template('newpost')

@route('/new-wiki/', method='post')
def create_wiki():
    '''skapar en ny wiki OM den är korrekt med metoden POST'''
    wikiTitle = getattr(request.forms, 'wikiTitle')
    wikiText = getattr(request.forms, 'wikiText')
    
    if wikiTitle == "" and wikiText == "":
        titleMessage = "Du måste ange en titel på wikin"
        textMessage = "Du måste ange ett innehåll på din wiki"
        return template('save', errorWikiText = wikiText, errorWikiTitle = wikiTitle, errorTitleMessage = titleMessage, errorTextMessage = textMessage)
    elif wikiTitle == "":
        titleMessage = "Du måste ange en titel på wikin"
        textMessage = ""
        return template('save', errorWikiText = wikiText, errorWikiTitle = wikiTitle, errorTitleMessage = titleMessage, errorTextMessage = textMessage)
    elif wikiText == "":
        titleMessage = ""
        textMessage = "Du måste ange ett innehåll på din wiki"
        return template('save', errorWikiText = wikiText, errorWikiTitle = wikiTitle, errorTitleMessage = titleMessage, errorTextMessage = textMessage)
    else:
        wikis = read_wikis_from_file()
        id = create_id(wikis)

        wikis.append({
            'Title':wikiTitle,
            'Text':wikiText,
            'id':id 
        })
        
        my_file = open("wikis.json", "w")
        my_file.write(json.dumps(wikis, indent=4))
        my_file.close()

        redirect("/")

@route('/wiki/<id>')
def create_wiki(id):
    '''skapar sidan av wiki med id'''
    my_file = open('wikis.json','r')
    data = json.load(my_file)

    #-1 so it corresponds   with the website page number
    newId = int(id)-1

    text = data[newId]['Text']
    title = data[newId]['Title']
    wikiIdPlusOne = int(id)+1

    my_file.close()
    return template('wiki', wikiID = id, wikiText = text, wikiTitle = title, idPlusOne = wikiIdPlusOne)

@route('/wiki/edit/<id>')
def edit_wiki(id):
    '''editar wiki med id som wildcard'''
    my_file = open('wikis.json','r')
    data = json.load(my_file)

    #-1 so it corresponds with the website page number
    newId = int(id)-1

    text = data[newId]['Text']
    title = data[newId]['Title']
    

    my_file.close()
    return template('edit', wikiText = text, wikiTitle = title, wikiId = id)

@route('/update', method = 'post')
def update_wiki():
    '''uppdaterar wikin OM det stämmer med metoden POST'''

    title = getattr(request.forms, 'newWikiTitle')
    text = getattr(request.forms, 'newWikiText')
    theID = getattr(request.forms, 'wikiId')
    theID = int(theID)

    if title == "" and text == "":
        titleMessage = "Du måste ange en titel"
        textMessage = "Du måste ha text"
        return template('update', errorTextMessage = textMessage, errorTitleMessage = titleMessage, wikiTitle = title, wikiText = text, wikiId = theID)
    elif title == "":
        titleMessage = "Du måste ange en titel"
        textMessage = ""
        return template('update', errorTextMessage = textMessage, errorTitleMessage = titleMessage, wikiTitle = title, wikiText = text, wikiId = theID)
    elif text == "":
        titleMessage = ""
        textMessage = "Du måste ha text"
        return template('update', errorTextMessage = textMessage, errorTitleMessage = titleMessage, wikiTitle = title, wikiText = text, wikiId = theID)
    else:
        with open("wikis.json", "r") as f:  
            data = json.load(f)
            for list in data:
                if list['id'] == theID:                
                    list['Title'] = title
                    list['Text'] = text
        
        with open("wikis.json", "w") as f:
            json.dump(data, f)
        
        redirect('/')

@route('/delete/<id>')
def delete_wiki(id):
    '''tar bort wiki med hjälp av ID'''
    theID = int(id)

    with open("wikis.json", "r") as f:  
        data = json.load(f)  
        for list in data:
            if list['id'] == theID:
                data.remove(list)

        for list in data:
            list['id'] = 0

        timesLooped = 1
        for list in data:
            
            list['id'] = list['id'] + timesLooped
            print(f"times looped {timesLooped}")
            timesLooped = timesLooped + 1

    with open("wikis.json", "w") as f:
        json.dump(data, f, indent=4) 
    
    return redirect('/')

@route('/static/<filename:path>')
def server_static(filename):
    '''Handles the routes to our static files
    
    Returns:
        file : the static file requested by URL	
    '''

    return static_file(filename, root='static')

@error(404)
def error404(error):
    return template('error404', error = error)

@error(500)
def error500(error):
    return template('error500',error = error)

run(host="127.0.0.1", port=8080, reloader=True)