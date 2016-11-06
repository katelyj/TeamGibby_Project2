import sqlite3
import hashlib


## Looks into the story entries DB for story IDs where the user matches the current user logged in
## Returns a list of story IDs that the user is able to read, because they have contributed to them

def storiesICanView():

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    
    ggg = "SELECT storyId FROM story_entries where user == " + str(session['user']) + ";"
    rara = og.execute(ggg)
    stories = []#list of story IDs you're allowed to choose from
    i = 0
    for item in rara:
        if (not(item[0] in stories)):
            stories.append(item[0])
    db.close()
    return stories


## Takes a list of (int) story ids, searches in the story directory for the stories you can view, because you have contributed to them
## returns a form full of buttons, where each button has the text "title, by user" , is named storytoread, and is matched with it's 
## story ID
def buttonifyLinks(storyID):

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    
    Str = "<form action = '/view/'>" 
    command = "SELECT Title, user, storyId FROM story_directory WHERE storyId == " + str(storyID)+ ""
    poe = og.execute(command)
    for item in poe:
        f = ""
        f+= item[0] + " , by "
       # f+= item[1] + 
        Str += "<button type = 'submit' name = 'storytoread' value = " + str(item[2]) + ">  " + f + "</button>"
        Str+= "<br>"
    Str += " </form>  "
    db.close()


##Returns a form full of buttons to the first 10 stories in the story directory database
def storiesToAddTo():

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    
    Str = "form action= '/add/'>"
    command = "SELECT Title, user, storyID FROM story_directory"
    markSloan = og.execute(command)
    num = 0
    for manz in markSloan:
        if (num < 10):
            f = ""
            f += manz[0] + " , by "
            f += manz[1]
            Str +=  "<button type = 'submit' name = 'storytoaddto' value = " + str(manz[2]) + ">" + f +"</button>"
            Str += "<br>"
            num +=1
        else:
            break
    Str+= "</form>"
    db.close()
