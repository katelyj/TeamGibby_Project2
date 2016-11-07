import sqlite3
import hashlib



def wholeStory(storyID):
    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    command = "SELECT content, entryNum FROM story_entries WHERE storyID ==" + str(storyID)
    alvin = og.execute(command)
    liz = []
    for chipmunks in alvin:
        liz.append("Entry " + str(chipmunks[1]) + ": " + chipmunks[0])
    db.close()
    return liz
        
    


def contributed(username, storyID):
    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    
    q = "SELECT user FROM story_entries WHERE storyID == " + storyID 
    stuff = og.execute(q)
    ret = False
    for thing in stuff:
	print thing[0]
        if thing[0] == username:
            ret = True
    db.close()
    return ret

def storyIDExist(storyID):
    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    
    q = "SELECT storyID FROM story_id WHERE storyID == " + storyID
    stuff = og.execute(q)
    if not stuff:
        return False
    else: 
        return True
## Looks into the story entries DB for story IDs where the user matches the current user logged in
## Returns a list of story IDs that the user is able to read, because they have contributed to them

def storiesICanView(user):

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    
    ggg = "SELECT storyID FROM story_entries where user == '" + str(user) + "';"
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
    for i in storyID:
        command = "SELECT title, creator, storyID FROM story_directory WHERE storyId == " + str(i)
        poe = og.execute(command)
        for item in poe:
            f = ""
            f+= item[0] + " , by "
            f+= item[1] 
            Str += "<button type = 'submit' name = 'storytoread' value = " + str(item[2]) + ">  " + f + "</button>"
            Str+= "<br>"
    Str += " </form>  "
    db.close()


##Returns a form full of buttons to the first 10 stories in the story directory database
def storiesToAddTo(user):

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    command = "SELECT storyID FROM story_directory"
    markSloan = og.execute(command)
    num = 0
    listA = [] #id title crea
    for manz in markSloan:
            listA.append(manz[0])
    
    command2 = "SELECT storyID from story_entries WHERE user == '" + user + "'"
    lexie = og.execute(command2)
    for idk in lexie:
        if (idk[0] in listA):
            listA.remove(idk[0])
    return listA
    db.close()
