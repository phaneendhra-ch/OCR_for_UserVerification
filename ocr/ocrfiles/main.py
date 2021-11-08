from .emblemcolor1_func import emblemcolor1
from .Front import frontrawdata
from .main2_final import ocr

def insertimg(user_path):
    if (emblemcolor1(user_path) == 1):

        if ocr(user_path)!="":
            get = frontrawdata(ocr(user_path))
            return(get)
        else:
            print('Sorry we couldnt detect any text-raw data from your aadhar card.')
    else:
        print('We found your image to be inappropiate,try uploading another one')


print('im testing here')
