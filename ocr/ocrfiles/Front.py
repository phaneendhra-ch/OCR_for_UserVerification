import re
from nltk.corpus import words

#with open('dad.txt','r+') as f:

def frontrawdata(data):
    try:
            data = data.replace("Government of India","")
    except:
            pass
    #print(r'{data}')
    data1 = data.split('\n') #splitting at new line

    for iteration in range(data1.count("")):
    	data1.remove("") #removing null values
    data1 = [each1.lower() for each1 in data1] #case conversion


    def dob():

        for each in data1:
            #print(each)
            each = each.replace(" ","")
            #print(each)
            user_dob = re.search(r'\d{2}/\d{2}/\d{4}',each)
            #print(user_dob)
            if user_dob is not None:
                return user_dob.group()

    def gender():

        for each in data1:
            #print(each)
            #each = each.replace(" ","")
            male = re.findall(r"\bmale"+'\D', each)
            female = re.findall(r"\bfemale"+'\D',each)
            #print(male,female)
            if male!= []:
                    return male[0].replace('\r','')
            elif female!=[]:
                    return female[0].replace('\r','')
            else:
                pass

    def aadharnum():

        for each in data1:
            each = each.replace(" ","")
            pattern = "".join(re.findall("[0-9]",each))
            if len(pattern) == 12:
                return int(pattern)

    def name():
        #print(data1)
        name_list=[]
        for each in data1:
            reg = "[a-zA-z\s]"
            pattern = "".join(re.findall(reg,each))

            if pattern == each:
                    #print(each)
                    name_list.append(each)
                    #return each
            #print(name_list)
        if name_list!=[]:
            for counting in range(0,len(name_list)):
                name_list[counting] = name_list[counting].replace('\r','')
                #print(name_list[counting])
                if name_list[counting] in words.words():
                    #print('removed')
                    name_list.remove(name_list[counting])
            #print(name_list)
            return name_list[-1]
        else:
            return("Name not found")
        return("Name not found")


    UserFrontInfo = {'aadharnum':aadharnum(),
                     'name':name(),
                     'dob':dob(),
                     'gender':gender(),
                     }
    return UserFrontInfo
