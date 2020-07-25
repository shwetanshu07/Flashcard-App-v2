from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import date
# make word unique
db = 'example.db'
# function to extract meaning from the internet
def workonwords(setname,textboxdata,customboxdata):
    url='https://www.dictionary.com/browse/'
    word_list=textboxdata.split(',')
    dict={}
    notfound=[]    # array of words not found
    for word in word_list:
        page=requests.get(url+word)
        soup=BeautifulSoup(page.content, 'html.parser')
        try:
            meaning=soup.find(class_='css-1o58fj8 e1hk9ate4')
            meaning=meaning.text
            dict[word]=meaning
        except:
            notfound.append(word)
    # adding custom definitions to dictionary
    if customboxdata!='':
        wmpair=customboxdata.split('\n')
        for i in wmpair:
            word=i.split('-')[0]
            meaning=i.split('-')[1]
            dict[word]=meaning
    else:
        pass # as there are no custom words

    add_new_sets(setname)
    add_words_to_database(setname, dict, customboxdata)
    return(notfound)

# function to add word-meaning to database
def add_words_to_database(setname, dict, customboxdata):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE words
        (word text, definition text, setname text, votes numeric)''')
    except:
        pass    # Table already exists
    for key in dict:
        word=key
        meaning=dict[key]
        sql="INSERT INTO words (word,definition,setname,votes) VALUES (?,?,?,?)"
        cur.execute(sql,(word,meaning,setname,0))
    conn.commit()
    conn.close()
    print('Success - Words added to database')


# function to add different new sets to the sets table
def add_new_sets(setname):
    date_created = date.today()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE sets (setname text unique,date_lastrev text)")
    except:
        pass # as table already exists
    cur.execute("INSERT OR IGNORE INTO sets (setname,date_lastrev) VALUES (?,?)", (setname,str(date_created)))
    conn.commit()
    conn.close()
    print('Success - Set added to database')


# function for updating the date
def date_update(setname):
    new_date = date.today()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("UPDATE sets SET date_lastrev=? WHERE setname=?",(str(new_date), setname))
    conn.commit()
    conn.close()

# function for vote update
def vote_update(word):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT votes FROM words WHERE word = ?",(word,))
    vote = cur.fetchone()    #the votes are returned in form of tuple ex (0,)
    vote = vote[0]+1
    cur.execute("UPDATE words SET votes=? WHERE word=?",(vote, word))
    conn.commit()
    conn.close()

# function for ordering dates from last revised to recently revised
def history():
    his_dict={}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sets ORDER BY date_lastrev")
    fetch_results = cur.fetchmany(10)
    conn.close()
    '''for tuple_ in fetch_results:
        his_dict[tuple_[0]] = tuple_[1]
    print(his_dict)'''
    return(fetch_results)

# function returns a list of all the set names for populating listbox
def getallsets():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT setname FROM sets")
    allsets = cur.fetchall()
    conn.close()
    return(allsets)

# function for selecting word-meanings from a set and return as key value pairs of dictionary
def extract_word_meaning(setname):
    wm_pair = {}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT word, definition FROM words WHERE setname=?",(setname,))
    s=cur.fetchall()
    conn.close()
    for pair in s:
        wm_pair[pair[0]]=pair[1]
    return(wm_pair)

def search_by_word(word):
    wm_pair2={}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT word, definition FROM words WHERE word LIKE ? ",('%'+word+'%',))
    s=cur.fetchall()
    conn.close()
    for tuple_ in s:
        wm_pair2[tuple_[0]]=tuple_[1]
    return(wm_pair2)

def search_by_letter(letter_array):
    wm_pair3={}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    for letter in letter_array:
        cur.execute("SELECT word, definition FROM words WHERE word LIKE ? ",(letter+'%',))
        s=cur.fetchall()
        for tuple_ in s:
            wm_pair3[tuple_[0]]=tuple_[1]
    conn.close()
    return(wm_pair3)

def most_voted():
    most_voted_dict={}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT word, definition FROM words ORDER BY votes DESC")
    fetch_results = cur.fetchmany(50)
    conn.close()
    for tuple_ in fetch_results:
        most_voted_dict[tuple_[0]]=tuple_[1]
    return(most_voted_dict)

#workonwords("gjkefijeroi","setname")
#extract_word_meaning('set')
#search_by_letter(['a','i'])
#history()
