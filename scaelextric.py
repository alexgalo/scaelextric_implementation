import pandas as pd
import random
import re
import math
import datetime
import preprocessor as pr
from pandas.core.frame import DataFrame
from twython import Twython
from colored import fg, bg, attr


# Calcula la fecha del día
now= datetime.datetime.now()
day= int(now.day)
month= int(now.month)
year= int(now.year)

# Personaliza el texto de salida
color_titulo = fg(234) + bg(195) + attr('bold')
color_pregunta= fg(186) + attr('bold')
color_sub= fg(203) + attr('bold')
color_texto= fg(231) + attr('bold')
color_line= fg(226) + attr('bold')
color_found= fg(82) + attr('bold')
color_not_found= fg(196) +attr('bold')
color_a= fg(32)+ attr('bold')
color_b= fg(49)+ attr('bold')
res = attr('reset')

line= (color_line+'--------------------------------------------------------------------------'+res)

# Lee el archivo excel
doc= pd.read_excel(r'/home/alexgalo/Desktop/Veale_script_midpoints.xlsx')
doc2= pd.read_excel(r'/home/alexgalo/Desktop/Veale_category_actions.xlsx')
doc3= pd.read_excel(r'/home/alexgalo/Desktop/Veale_NOC_list.xlsx')
doc4= pd.read_excel(r'/home/alexgalo/Desktop/Veale_idiomatic_actions.xlsx')
doc5= pd.read_excel(r'/home/alexgalo/Desktop/Veale_initial_bookend_actions.xlsx')
doc6= pd.read_excel(r'/home/alexgalo/Desktop/Veale_closing_bookend_actions.xlsx')
doc7= pd.read_excel(r'/home/alexgalo/Desktop/Veale_ action_pairs.xlsx')

# Genera DataFrame
df= pd.DataFrame(doc)
df2= pd.DataFrame(doc2)
df3= pd.DataFrame(doc3)
df4= pd.DataFrame(doc4)
df5= pd.DataFrame(doc5)
df6= pd.DataFrame(doc6)
df7= pd.DataFrame(doc7)

# Divide en columnas doc 
before_mp= df['Before Midpoint']
midpoint= df['Midpoint']
after_mp= df['After Midpoint']

# Divide en columnas doc2
category= df2['Category']
whenSubject= df2['When Subject']
whenObject= df2['When Object']

# Divide en columnas doc3
character= df3['Character']
aka= df3['AKA']
canonical= df3['Canonical Name']
gender= df3['Gender']
address_1= df3['Address 1']
address_2= df3['Address 2']
nationality= df3['Address 3']
#nationality= df3['Simone de Beauvoir']
politics= df3['Politics']
marital= df3['Marital Status']
opponent= df3['Opponent']
typical_activity= df3['Typical Activity']
vehicle= df3['Vehicle of Choice']
provocative= df3['provocative T-shirt, spiky hair, black leather jacket']
domains= df3['Domains']
genres= df3['Genres']
fictive= df3['Fictive Status']
portrayed= df3['Portrayed By']
creator= df3['Creator']
creation= df3['Creation']
group_affiliation= df3['Group Affiliation']
fictional= df3['Fictional World']
category_noc= df3['Category']
negative_points= df3['Negative Talking Points']
positive_points= df3['Positive Talking Points']

# Divide en columnas doc4
idiomatic_actions= df4['Action']
idiomatic_forms= df4['Idiomatic Forms']

# Divide en columnas doc5
initial_action= df5['Initial Action']
establishing_action= df5['Establishing Action']

# Divide en columasn doc6
final_action= df6['Final Action']
closing_action= df6['Closing Action']

# Divide en columnas doc7
action_pair= df7['Action Pair']
before= df7['Before']
link= df7['Link']
after= df7['After']


class TwitterCrawler:
    # Instancia para hacer peticiones al API de Twitter
    def __init__(self):
        self.t = Twython(app_key= 't3cyFSkiWB4bSbUCOfKFQfdmU', 
                            app_secret= 'NMNpeBPl4Xb7Fppk3K2jGkuvEqut0X4xHv4Mi0n4PAvHlBMQmr',
                            oauth_token= '612153534-YdrJtLDMP4q5PzXNvlkVKQYAKK8manQOfdIorIfd', 
                            oauth_token_secret= 'wJFbjSZSYT4raoMYMTsaA76WUTklEYgW7gQzMG4h6xNFs')
        self.trends = list()

    # [Y]Obtiene el background cultural del momento
    def getTweets(self):
        
        # Obtiene los primeros 10 tweets de los cinco principales periódicos del mundo
        new_york_times= self.t.get_user_timeline(screen_name= "nytimes", tweet_mode= "extendend", count= 10)
        the_guardian= self.t.get_user_timeline(screen_name= "guardian", tweet_mode= "extendend", count= 10)
        the_wall_street_journal= self.t.get_user_timeline(screen_name= "WSJ", tweet_mode= "extendend", count= 10)
        the_washington_post= self.t.get_user_timeline(screen_name= "washingtonpost", tweet_mode= "extendend", count= 10)
        los_angeles_times= self.t.get_user_timeline(screen_name= "latimes", tweet_mode= "extendend", count= 10)

        nytimes= {'journal': 'The New York Times',
                    'twitter_account': '@nytimes',
                    'tweets': list()}
        guardian= {'journal': 'The Guardian',
                    'twitter_account': '@guardian',
                    'tweets': list()}
        wsj= {'journal': 'The Wall Street Journal',
                    'twitter_account': '@WSJ',
                    'tweets': list()}
        washingtonpost= {'journal': 'The Washington Post',
                    'twitter_account': '@washingtonpost',
                    'tweets': list()}
        latimes= {'journal': 'Los Angeles Times',
                    'twitter_account': '@latimes',
                    'tweets': list()}

        for item in new_york_times:
            text= item['text']
            text= pr.clean(text)
            text= re.sub(r'[^\w\s]', '', text)
            nytimes['tweets'].append(text)
        for item in the_guardian:
            text= item['text']
            text= pr.clean(text)
            text= re.sub(r'[^\w\s]', '', text)
            guardian['tweets'].append(text)
        for item in the_wall_street_journal:
            text= item['text']
            text= pr.clean(text)
            text= re.sub(r'[^\w\s]', '', text)
            wsj['tweets'].append(text)
        for item in the_washington_post:
            text= item['text']
            text= pr.clean(text)
            text= re.sub(r'[^\w\s]', '', text)
            washingtonpost['tweets'].append(text)
        for item in los_angeles_times:
            text= item['text']
            text= pr.clean(text)
            text= re.sub(r'[^\w\s]', '', text)
            latimes['tweets'].append(text)

        cultural_background= list()
        cultural_background.append(nytimes)
        cultural_background.append(guardian)
        cultural_background.append(wsj)
        cultural_background.append(washingtonpost)
        cultural_background.append(latimes)

        return cultural_background


# [Y]Solicita la configuración inicial
def getInput():

    print(color_titulo+'\n\t\t\t~NARRATIVE GENERATOR~ '+res)
    # Lee el numero de tripletas a generar
    try:
        thirds= int(input(color_pregunta+'\n> How many thirds do you need ?: '+res))
    except ValueError:
        print('Your input is not a number.')

    # Lee el tipo de instanciación
    valid_input= False
    while not valid_input:
        instantiation= input(color_pregunta+'> What type of instantiation do you prefer ? D)irect or I)ndirect: '+res)
        instantiation= instantiation.upper()
        if instantiation == 'D' or instantiation == 'I':
            valid_input = True
        else:
            print('Please enter D for direct or I for indirect instantiation.\n')
    
    print('\n'+line+'\n')
    print(color_sub+'THE USER HAS BEEN SELECTED THIS CONFIG:\n'+res)
    print(color_texto+'  Number of thirds: {}'.format(thirds)+res)

    if instantiation == 'D':
        print(color_texto+'  Instantiation: Direct'+res)
    else:
        print(color_texto+'  Instantiation: Indirect'+res)
    print('\n'+line+'\n')

    return thirds, instantiation

# [Y]Elige una acción de los posibles candidatos (*)
def chooseOne(option):
    sentences= str(option)          # castea la celda
    words= sentences.split(',')     # obtiene una lista de opciones
    top= len(words)                 
    index= random.randint(0, top-1)
    word= words[index]              # selecciona una opción
    
    return word

# [Y]Establece una tercia de sentencias de acuerdo al index
def setThirds(index):
    third= list()

    # Establece tripleta de acciones
    A= chooseOne(before_mp[index])  # selecciona una opcion
    A_= re.sub(r'[^\w\s]','',A)     # limpia la cadena
    third.append(A_)                # agrega acción

    B= chooseOne(midpoint[index])
    B_= re.sub(r'[^\w\s]','',B)
    third.append(B_)

    C= chooseOne(after_mp[index])
    C_= re.sub(r'[^\w\s]','',C)
    third.append(C_)

    #setThird= "A: {} / B: {} / C: {}".format(A_, B_, C_) 

    return (third, C_)

# [Y]Busca la sentencia (C=A) en Before Midpoint y devuelve el index
def searchWord(word):
    counta= 0
    before_index= list()
    # colecciona todos los index donde la acción está en before
    for item in before_mp:
        if word == item:
            before_index.append(counta)
        counta += 1
    
    #print(before_index)
    longitud= len(before_index)
    option= random.randint(0, longitud-1) 
    index= before_index[option]
    #print(index)

    return index

# [Y]Busca la primera acción en el cultural background
def getFirstAction(cultural_bckgnd):
    
    before_col= list()
    action= ''
    index= 0
    nyt= ''
    nyt_actions= list()
    guardian= ''
    guardian_actions= list()
    wsj= ''
    wsj_actions= list()
    washington= ''
    washington_actions= list()
    latimes= ''
    latimes_actions= list()
    total_actions= list()


    for item in cultural_bckgnd[0]['tweets']:
        nyt= nyt + item + ' '
    for item in before_mp:
        if str(item) in nyt:
            if item not in nyt_actions:
                #print('NYT', item)
                nyt_actions.append(item)
                total_actions.append(item)
        
    for item in cultural_bckgnd[1]['tweets']:
        guardian= guardian + item + ' '
    for item in before_mp:
        if str(item) in guardian:
            if item not in guardian_actions:
                #print('NYT', item)
                guardian_actions.append(item)
                total_actions.append(item)

    for item in cultural_bckgnd[2]['tweets']:
        wsj= wsj + item + ' '
    for item in before_mp:
        if str(item) in wsj:
            if item not in wsj_actions:
                #print('NYT', item)
                wsj_actions.append(item)
                total_actions.append(item)

    for item in cultural_bckgnd[3]['tweets']:
        washington= washington + item + ' '
    for item in before_mp:
        if str(item) in washington:
            if item not in washington_actions:
                #print('NYT', item)
                washington_actions.append(item)
                total_actions.append(item)

    for item in cultural_bckgnd[4]['tweets']:
        latimes= latimes + item + ' '
    for item in before_mp:
        if str(item) in latimes:
            if item not in latimes_actions:
                #print('NYT', item)
                latimes_actions.append(item)
                total_actions.append(item)

    #print(nyt_actions)
    #print(guardian_actions)
    #print(wsj_actions)
    #print(washington_actions)
    #print(latimes_actions)

    rnd= random.randint(0, len(total_actions)-1)         
    action= total_actions[rnd]
    #print(action)
     
    for item in before_mp:  
        before_col.append(item)
    
    index= before_col.index(action)
    #print(index)

    if action in nyt_actions:
        print(color_texto+'  The New York Times has been tweeted recently something about this topic.'+res)
        print(color_texto+'  Twitter account: ', cultural_bckgnd[0]['twitter_account'], '\n'+res)
    if action in guardian_actions:
        print(color_texto+'  The Guardian has been tweeted recently something about this topic.'+res)
        print(color_texto+'  Twitter account: ', cultural_bckgnd[1]['twitter_account'], '\n'+res)
    if action in wsj_actions:
        print(color_texto+'  The Wall Street Journal has been tweeted recently something about this topic.'+res)
        print(color_texto+'  Twitter account: ', cultural_bckgnd[2]['twitter_account'], '\n'+res)
    if action in washington_actions:
        print(color_texto+'  The Washington Post has been tweeted recently something about this topic.'+res)
        print(color_texto+'  Twitter account: ', cultural_bckgnd[3]['twitter_account'], '\n'+res)
    if action in latimes_actions:
        print(color_texto+'  Los Angeles Times has been tweeted recently something about this topic.'+res)
        print(color_texto+'  Twitter account: ', cultural_bckgnd[4]['twitter_account'], '\n'+res)

    return action, index

# [Y]Crea una las tercias solicitadas por el usuario
def createThirds(tercias, idx): 

    counter= 1
    tripletas= list()

    # Solo una tercia solicitada
    if tercias == 1:
        # La primera tercia de sentencias 
        third, last= setThirds(idx)   # Busca la primera tripleta
        index= searchWord(last)             # ?
        tripletas.append(third)

    # varios tercias solicitadas
    elif tercias > 1:
            third, last= setThirds(idx)   # Busca la primera tripleta
            index= searchWord(last)             # Busca el index para la próxima
            #print(third)
            tripletas.append(third)             # Agrega la tripleta

            while counter < tercias:
                counter += 1                    # Completa las tercias faltantes
                thrd,lst= setThirds(index)
                #print(thrd)
                tripletas.append(thrd)
                index= searchWord(lst)
    


    return tripletas

# [Y]Determina la categoria para una accion inicial 
def searchCategory(word):
    ctr= 0
    cntr= 0
    tmp= list()
    tmp_2= list()
    index_whenSubject= list()
    index_whenObject= list()

    try:
        while ctr < len(whenSubject):   # lo busca en la primera columna
            actions= str(whenSubject[ctr])
            actions= actions.split(',')
            
            for item in actions:          # separa en acciones
                action= re.sub(r'[^\w\s]','',item)
                action= action.strip()
                tmp.append(action)

            if word in tmp:                # si la palabra está en esa celda regresa el index de la misma
                index_whenSubject.append(ctr)
                tmp= []
            else:
                tmp=[]                     # limpia la lista
            ctr += 1


        # Elije aleatoriamente alguna categoría
        rndm= random.randint(0, len(index_whenSubject) -1)
        
        cat= category[index_whenSubject[rndm]]
        #print('Category A: ', cat)

        return cat, 'A'

    except:
        print('Action not found in column whenSubject.')

    try:
        while cntr < len(whenObject):
            actions= str(whenObject[cntr])

            try:
                words= actions.split(',')
            except AttributeError:
                words= list()
                words[0]= actions
                #print('CCC', words)

            #print(words)
            for item in words:
                action_2= re.sub(r'[^\w\s]','',item)
                action_2= action_2.strip()
                tmp_2.append(action_2)
            
            if word in tmp_2:
                index_whenObject.append(cntr)
                tmp_2= []

            else:
                tmp_2= []
                #
            cntr += 1

            # Elije aleatoriamente alguna categoría
            rnd= random.randint(0, len(index_whenObject) -1)
        
            cat_b= category[index_whenObject[rnd]]
            #print('Category B: ', cat_b)

            return cat_b, 'B'
    except:
        print('Action not found in column whenObject.')


# A partir de una categoria selecciona a los personajes A y B
def chooseCharacters(categgory, character_type, instantiation): # (category, 'A', 'D'/'I')
    
    idx= 0
    temp_cat= list()
    possibles= list()
    
    # Crea lista personajes disponibles por categoria
    for item in category_noc: # Celdas
        
        options= str(item)
        categories= options.split(',')

        for item in categories:                         # para cada celda busca la categoria y si aparece agrega el index 
            new_cat= re.sub(r'[^\w\s]','',item)
            new_cat= new_cat.strip()
            temp_cat.append(new_cat)
            
        if categgory in temp_cat:
            possibles.append(idx)
            temp_cat= []
        else:
            #print('Not found')
            temp_cat= []
        idx += 1


    rndm= random.randint(0, len(possibles) -1)
    # El index del caracter uno 
    character_index= possibles[rndm]
    
    # Selección de personaje UNO
    character_1= character[possibles[rndm]]
    #print('character index: ', character_index, character_1)
    
    characters_2= list()

    # instanciación directa
    if instantiation == 'D':

        print(color_texto+'  Searching direct opponents to : ', character_1, '\n'+res)



        # 1 Oponente por rivalidad clásica
        opp= opponent[possibles[rndm]]
        check= isinstance(opp, str)

        # si hay texto en la celda, elige un oponente
        if check == True:
            print(color_found+'> Classic rival found !\n'+res)
            op= opponent[possibles[rndm]]
            opp_1= chooseOne(op)
            characters_2.append(opp_1)
        else: 
            print(color_not_found+'  Unregistered classic rival\n'+res)    



        # 2 Oponente por rivalidad política (directa)
        politic_status= politics[possibles[rndm]]   
        check1= isinstance(politic_status, str)
        
        if check1 == True:
            print(color_found+'> Political rival found !\n'+res)
            po= politics[possibles[rndm]]               # determina la posición política de character 1
            politic= chooseOne(po)
            #print('character_1', politic)

            opponents= list()
            ctr= 0

            # busca contrarios de derecha
            if politic == 'left': 
                while ctr < len(politics):
                    if politics[ctr] == 'right':
                        #print(character[ctr], ctr +2)
                        opponents.append(character[ctr])
                    ctr += 1
                
                """
                # agrega todos los personajes interpretados por el mismo autor
                long_char= len(opponents)
                #print(long_char)
                
                if long_char == 0:
                    characters_2.append('--NoCharactersAdded--')
                else:
                    for item in opponents:
                        characters_2.append(item)
                """
                #print('Real: ', fictive_opponents)
                rndm_2= random.randint(0, len(opponents) -1)
                characters_2.append(opponents[rndm_2])

            # busca oponentes de izquierda
            elif politic == 'right':
                while ctr < len(politics):
                    if politics[ctr] == 'left':
                        opponents.append(character[ctr])
                    ctr += 1
                """
                # agrega todos los personajes interpretados por el mismo autor
                long_char= len(opponents)
                #print(long_char)
                
                if long_char == 0:
                    characters_2.append('--NoCharactersAdded--')
                else:
                    for item in opponents:
                        characters_2.append(item)
                """
            
                rndm_2= random.randint(0, len(opponents) -1)
                characters_2.append(opponents[rndm_2])
        else:
            print(color_not_found+'  Unregistered political status\n'+res)



        # 3 Oponente ficticio vs real (directa)
        fictive_status= fictive[possibles[rndm]]
        check2= isinstance(fictive_status, str)
        fictive_opponents= list()
        ctr= 0

        # se trata de un personaje 1 ficticio
        if check2 == True:

            print(color_found+'> Real rival found !\n'+res)
            while ctr < len(fictive):
                state= isinstance(fictive[ctr], str)
                if state == False:
                    fictive_opponents.append(character[ctr])
                ctr += 1

            #print('Real: ', fictive_opponents)
            rndm_3= random.randint(0, len(fictive_opponents) -1)
            characters_2.append(fictive_opponents[rndm_3])
        
        # se trata de un personaje real
        elif check2 == False:
            print(color_found+'> Fictional rival found !\n'+res)
            while ctr < len(fictive):
                if fictive[ctr] == 'fictional':
                    fictive_opponents.append(character[ctr])
                ctr += 1

            #print('Fictional: ', fictive_opponents)
            rndm_3= random.randint(0, len(fictive_opponents) -1)
            characters_2.append(fictive_opponents[rndm_3])



        # 4 Openente heroes vs villanos
        hero_status= category_noc[possibles[rndm]]
        #hero_status= category_noc[768]
        

        if 'Hero' in hero_status:
            print(color_found+'> Hero status: ', hero_status, '\n'+res)
            bad_guys= list()
            tmp_bad= list()
            count= 0
            for item in category_noc:
                bads= str(item)
                bads= bads.split(',')

                for itm in bads:
                    new_bad= re.sub(r'[^\w\s]','',itm)
                    new_bad= new_bad.strip()
                    tmp_bad.append(new_bad)
                
                if 'Villain' in tmp_bad:
                    bad_guys.append(character[count])
                    tmp_bad= []
                else:
                    tmp_bad= []
                count += 1
            
            rndm= random.randint(0, len(bad_guys) -1)
            characters_2.append(bad_guys[rndm])
        
        elif 'Villain' in hero_status:
            print(color_found+'> Villain status: ', hero_status, '\n'+res)
            good_guys= list()
            tmp_good= list()
            cnt= 0
            for item in category_noc:
                goods= str(item)
                goods= goods.split(',')

                for itm in goods:
                    new_good= re.sub(r'[^\w\s]','',itm)
                    new_good= new_good.strip()
                    tmp_good.append(new_good)
                
                if 'Hero' in tmp_good:
                    good_guys.append(character[cnt])
                    tmp_good= []
                else:
                    tmp_good= []
                cnt += 1
            
            rndm= random.randint(0, len(good_guys) -1)
            characters_2.append(good_guys[rndm])
        else:
            print(color_not_found+'  Unregistered moral status\n'+res)



    # instanciación indirecta +**+
    elif instantiation == 'I':
        
        print(color_texto+'Searching indirect opponents to: ', character_1, '\n'+res)


        # 5 Oponente por interpretación 
        interpreter_status= portrayed[possibles[rndm]]  # identifica si character 1 fué interpretado por alguien
        check5= isinstance(interpreter_status, str)


        if check5 == True:         

            i= portrayed[possibles[rndm]]
            interpreter= chooseOne(i)             
            tmp_inters= list()                      # elige un interpréte 
            interpreters= list()
            ctr= 0
            print(color_found+'> Interpreter: ', interpreter+res)

            for item in portrayed:
                inters= str(item)
                inters= inters.split(',')

                for itm in inters:
                    new_int= re.sub(r'[^\w\s]','',itm)
                    new_int= new_int.strip()
                    tmp_inters.append(new_int)

                if interpreter in tmp_inters:
                    interpreters.append(character[ctr])
                    tmp_inters= []
                else:
                    tmp_inters= []
                ctr += 1
        
    
            # agrega todos los personajes interpretados por el mismo autor
            long_char= len(interpreters)
            #print(long_char)
            
            if long_char == 0:
                characters_2.append('--NoCharactersAdded--')
            else:
                rnd= random.randint(0, len(interpreters) -1)
                characters_2.append(interpreters[rnd])


        else:
            print(color_not_found+'  Unregistered interpreter'+res)
            characters_2.append('--NoCharactersAdded--')


        
        # 6 Oponente USA vs World 
        nation_status= nationality[possibles[rndm]]
        check4= isinstance(nation_status, str)
        nation_opponents= list()
        ctr4= 0

        if check4 == True:
            n= nationality[possibles[rndm]]
            nation= chooseOne(n)
            print(color_found+'> Nationality: ', nation+res)

            if nation == 'USA':
                #print('Este vato es gringo')

                while ctr4 < len(nationality):
                    if nationality[ctr4] != 'USA':
                        #print(character[ctr], ctr +2)
                        nation_opponents.append(character[ctr4])

                    ctr4 += 1

                #print('Derechos: ', opponents)
                rndm_4= random.randint(0, len(nation_opponents) -1)
                characters_2.append(nation_opponents[rndm_4])
                #print(nation_opponents[rndm_4])

        else:
            print(color_not_found+'  Unregistered nation'+res)


    
        # 7 Oponente por sexo 
        gender_status= gender[possibles[rndm]]
        #gender_status= gender[164]
        check_gender= isinstance(gender_status, str)

        if check_gender == True:
            print(color_found+'> Gender: ', gender_status+res)
            
            if gender_status == 'male':
                ctr= 0
                females= list()
                while ctr < len(gender):
                    if gender[ctr] == 'female':
                        females.append(character[ctr])
                    ctr += 1
                
                rdm= random.randint(0, len(females) -1)
                characters_2.append(females[rdm])
            
            elif gender_status == 'female':
                ct= 0
                males= list()
                while ct < len(gender):
                    if gender[ct] == 'male':
                        males.append(character[ct])
                    ct += 1

                rdm= random.randint(0, len(males) -1)
                characters_2.append(males[rdm])
        else:
            print(color_not_found+'  Unregistered gender status'+res)
        

        # 8 Oponente por genero o medio
        genre_status= genres[possibles[rndm]]
        check_genre= isinstance(genre_status, str)

        if check_genre == True:
            print(color_found+'> Genre: ', genre_status+res)

            if ('movies' in genre_status) or ('television' in genre_status) or ('literature' in genre_status):

                counta= 0
                tmp_reals= list()
                reals= list()
                for item in genres:
                    real= str(item)
                    real= real.split(',')

                    for itm in real:
                        new_real= re.sub(r'[^\w\s]','',itm)
                        new_real= new_real.strip()
                        tmp_reals.append(new_real)

                    if ('politics' in tmp_reals) or ('science' in tmp_reals) or ('sport' in tmp_reals):
                        reals.append(character[counta])
                        tmp_reals= []
                    else:
                        tmp_reals= []
                    counta += 1
                  
                rdm= random.randint(0, len(reals) -1)
                characters_2.append(reals[rdm])
        


            elif ('politics' in genre_status) or ('science' in genre_status) or ('sport' in genre_status):

                cnt= 0
                tmp_ficts= list()
                ficts= list()
                for item in genres:
                    real= str(item)
                    real= real.split(',')

                    for itm in real:
                        new_fic= re.sub(r'[^\w\s]','',itm)
                        new_fic= new_fic.strip()
                        tmp_ficts.append(new_fic)

                    if ('movies' in tmp_ficts) or ('television' in tmp_ficts) or ('literature' in tmp_ficts):
                        ficts.append(character[cnt])
                        tmp_ficts= []
                    else:
                        tmp_ficts= []
                    cnt += 1
                  
                rdm= random.randint(0, len(ficts) -1)
                characters_2.append(ficts[rdm])
        
        else:
            print(color_not_found+'  Unregistered genre'+res)
    

    try: 
        characters_2.remove('--NoCharactersAdded--')
    except:
        z= 2032


    # Elección de personaje al azar 
    print(color_sub+'\nAVAILABLE OPPONENTS: '+ res, characters_2)
    rndm_ch2= random.randint(0, len(characters_2) -1)
    character_2= characters_2[rndm_ch2]

    # Asignación de personajes A y B
    if character_type == 'A':
        character_A= character_1
        character_B= character_2
    elif character_type == 'B':
        character_A= character_2
        character_B= character_1


    print(color_texto+'\n  Character assignment:'+res)
    print(color_a+'  A: ', character_A+res)
    print(color_b+'  B: ', character_B+res)


    return character_A, character_B


# Para una lista de tripletas regresa una lista de sus correspondientes idiomatic actions
def generateIdiomaticActions(unalista, A, B):

    #print(unalista) 
    long= len(unalista)

    if long == 0:
        print(' ')

    elif long == 1:
        #print('\n')
        #print(unalista[0])
        a= unalista[0][0]
        #print(a)
        b= unalista[0][1]
        #print(b)
        c= unalista[0][2]
        #print(c)
        

        #print(A, a, B, 'then', A, b, B, 'then', A, c, B)
        #print(a, b, c)
        
        count_a= 0
        for item in idiomatic_actions:
            if a == item:
                a_action= chooseOne(idiomatic_forms[count_a])
                
            count_a += 1

        count_b= 0
        for item in idiomatic_actions:
            if b == item:
                b_action= chooseOne(idiomatic_forms[count_b])
            count_b += 1

        count_c= 0
        for item in idiomatic_actions:
            if c == item:
                c_action= chooseOne(idiomatic_forms[count_c])
            count_c += 1

        ab= getActionPairs(a, b)
        #print(ab)
        bc= getActionPairs(b, c)
        #print(bc)
        a_action= a_action.replace('A', A)
        a_action= a_action.replace('B', B)
        b_action= b_action.replace('A', A)
        b_action= b_action.replace('B', B)
        c_action= c_action.replace('A', A)
        c_action= c_action.replace('B', B)
            
        print(color_texto+'¬ ', a_action, '°', ab,'°', b_action, '°', bc, '°', c_action, '.\n'+res)

        nl= unalista.pop(0)
        #print(' -END')

    elif long >= 2:
        #print('\n')
        
        a_= unalista[0][0]
        b_= unalista[0][1]
        c_= unalista[0][2]
        #d_= unalista[1][0]
        e_= unalista[1][1]
        f_= unalista[1][2]

        """
        print(A, a_, B, 'then', B, b_, A, 'then', A, c_, B, 'then',
            B, 'DEFEAT', A, 'then',
            A, d_, B, 'then', B, e_, A, 'then', A, f_, B )
        """
        #print(a_, b_, c_, d_, e_, f_)

        count_a_= 0
        for item in idiomatic_actions:
            if a_ == item:
                a_action_= chooseOne(idiomatic_forms[count_a_])
            count_a_ += 1

        count_b_= 0
        for item in idiomatic_actions:
            if b_ == item:
                b_action_= chooseOne(idiomatic_forms[count_b_])
            count_b_ += 1

        count_c_= 0
        for item in idiomatic_actions:
            if c_ == item:
                c_action_= chooseOne(idiomatic_forms[count_c_])
            count_c_ += 1
        """
        count_d_= 0
        for item in idiomatic_actions:
            if d_ == item:
                d_action_= chooseOne(idiomatic_forms[count_d_])
            count_d_ += 1
        """
        count_e_= 0
        for item in idiomatic_actions:
            if e_ == item:
                e_action_= chooseOne(idiomatic_forms[count_e_])
            count_e_ += 1

        count_f_= 0
        for item in idiomatic_actions:
            if f_ == item:
                f_action_= chooseOne(idiomatic_forms[count_f_])
            count_f_ += 1

        # adding action pairs
        ab_= getActionPairs(a_, b_)
        bc_= getActionPairs(b_, c_)
        ce_= getActionPairs(c_, e_)
        ef_= getActionPairs(e_, f_)

        a_action_= a_action_.replace('A', A)
        a_action_= a_action_.replace('B', B)

        b_action_= b_action_.replace('A', A)
        b_action_= b_action_.replace('B', B)

        c_action_= c_action_.replace('A', A)
        c_action_= c_action_.replace('B', B)    

        e_action_= e_action_.replace('A', A)
        e_action_= e_action_.replace('B', B)

        f_action_= f_action_.replace('A', A)
        f_action_= f_action_.replace('B', B)

        print(color_texto+'¬ ', a_action_,'°',ab_,'°', b_action_,'°',bc_,'°',c_action_,'°', ce_,'°',e_action_,'°',ef_,'°',f_action_, '.\n'+res)

        # elimina el par de tercias
        for item in range(2):
            unalista.pop(0)

        # se llama a sí misma
        nl= unalista
        generateIdiomaticActions(nl, A, B)

# Conectores para un par de acciones
def getActionPairs(string1, string2):
    c1= 0
    connector= ''
    #print(unalista[0]+ ':' + unalista[1])
    try:
        for item in action_pair:
            if (string1+ ':' +string2) == item:
                connector= link[c1]
            c1 += 1
    except:
        connector= ' '
    #print(connector)
    return connector

# Crea la narrativa initial/idiomatic/final actions
def generateNarrative(tripletas, A, B):
    
    A_action= tripletas[0][0]
    A_action= re.sub(r'[^\w\s]','',A_action)
    A_action= A_action.strip()
    counter= 0

    # Initial bookend actions
    for item in initial_action:
        if A_action == item:
            first_action= chooseOne(establishing_action[counter])
            # sustitute characters
            first_action= first_action.replace('A', A)
            first_action= first_action.replace('B', B)
            print(color_texto+'¬ ', first_action, '\n'+res)
        counter += 1


    # Idiomatic actions
    thirds= tripletas[:]
    generateIdiomaticActions(thirds, A, B)



    # Closing bookend actions
    last_action= tripletas[-1][-1]

    counta= 0
    for item in final_action:
        if last_action == item:
            final_Action= chooseOne(closing_action[counta])
            # sustitute characters
            final_Action= final_Action.replace('A', A)
            final_Action= final_Action.replace('B', B)
            print(color_texto+'¬ ', final_Action, '.\n'+res)
        counta += 1

#
def printThirds(thirds):
    
    for item in range(len(thirds)):
        print(color_texto+'\tA:{} , B: {} , C: {} \n'.format(thirds[item][0], thirds[item][1], thirds[item][2] )+res)

    


# ---Main---
try: 
    # El programa solicita la configuración al usuario
    thirds, instantiation= getInput()

    # Se consulta el background cultural
    print(color_sub+'OBTAINING THE CURRENT CULTURAL BACKGROUND ...\n'+res)
    crawler= TwitterCrawler()
    cultural_background= crawler.getTweets()

    # Obtiene la primera acción apartir del  cultural background
    action, index= getFirstAction(cultural_background)
    print(color_texto+'> First action selected and topic: ', action +res)
    print('\n'+line+'\n')

except:
    print('API CONNECTION FAILED !')
    print('\n'+line+'\n')


# Se establece la estructura semantica
try: 
    print(color_sub+'COLLECTION OF SEMANTIC SETS ...\n'+res)
    tripletas= createThirds(thirds, index)
    print(color_texto+'  Semantic structure:\n'+res)
    printThirds(tripletas)
    print('\n'+line+'\n')
except:
    print(' THERE WAS AN ERROR CREATING THE THIRDS !')
    print('\n'+line+'\n')



# Busca la categoría de la acción, a partir de la primer acción
try:
    print(color_sub+'DETERMINING THE CATEGORY OF THE FIRST ACTION ...\n'+res)
    category, class_= searchCategory(action)
    print(color_texto+'  Category: ', category +res)
    print('\n'+line+'\n')

except:
    print(' THERE WAS AN ERROR, NO CATEGORY WAS SELECTED !')
    print('\n'+line+'\n')


# A partir de una categoria selecciona a los personajes A y B
try:
    print(color_sub+'CHOOSING CHARACTERS ...\n'+res)
    ch_A, ch_B= chooseCharacters(category, class_, instantiation)
    print('\n'+line+'\n')

except:
    print(' THERE WAS AN ERROR CHOOSING THE CHARACTERS !')
    print('\n'+line+'\n')


# Muestra la acción que no puede ser procesada
proof= list()
for item in idiomatic_actions:
    proof.append(item)

for tm in range(len(tripletas)):
    for item in tripletas[tm]:
        idx= proof.index(item)
        #print(item, idx)
        

# A partir de las tripletas y personajes se crea la historia       
try:
    print(color_sub+'\n  STORY: '+res)
    generateNarrative(tripletas, ch_A, ch_B)
    print('\n'+line+'\n')

except:
    print('  THERE WAS AN ERROR CREATING THE NARRATIVE !')
    print('\n'+line+'\n')

