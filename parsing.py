import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as Soup
from fontConversionTelegram import bold
from stringConversion import conversionFIOToFamilia, conversionFIO

#constant for parsing
FIND_TELEFON = "Тел.:"
FIND_VN_TELEFON = "Вн.тел.:"
FIND_KAB = "Кабинет:"
FIND_FAX = "Факс:"

#constant for create card(карочка-сообщение, которое отправится пользователю)
CARD_POST_DEP = "Депортамент: "
CARD_POST_TEXT = "Пост: "
CARD_FIO_TEXT = "ФИО: "
CARD_TELEFON_TEXT = "Телефон: "
CARD_TELEFON_VN_TEXT = "Внутренний телефон: "
CARD_FAX_TEXT = "Факс: "
CARD_KAB_TEXT = "Кабинет: "
CARD_EMPTY_TEXT = "По вашему запросу ничего не найдено!"

#constant for request
URL = 'https://admhmao.ru/organy-vlasti/telefonnyy-spravochnik-ogv-hmao/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}


class Worker:
    dep = ""
    post = ""
    fio = ""
    telefon = ""
    telefonVn = ""
    fax = ""
    kab = ""

    #create card(сообщение, которое отправится пользователю)
    def makeCard(self):
        card = ""
        if self.dep != "":
            card += bold(CARD_POST_DEP) + self.dep
        if self.post != "":
            card += bold(CARD_POST_TEXT) + self.post + "\n"
        if self.fio != "" and self.fio != "-":
            card += bold(CARD_FIO_TEXT) + self.fio + "\n"
        if self.telefon != "" and self.telefon != "-":
            card += bold(CARD_TELEFON_TEXT) + self.telefon + "\n"
        if self.telefonVn != "" and self.telefonVn != "-":
            card += bold(CARD_TELEFON_VN_TEXT) + self.telefonVn + "\n"
        if self.fax != "":
            card += bold(CARD_FAX_TEXT) + self.fax + "\n"
        if self.kab != "":
            card += bold(CARD_KAB_TEXT) + self.kab + "\n"
        return card



#parsing from site to class
def getArraySotr():
    arrayWorkers = []

    response = requests.get(URL, headers=HEADERS)
    print(response)

    bs = BeautifulSoup(response.text, "html.parser")
    arraySotrForParsing = bs.find_all("li", {"class" : "sotr"})
    
    for sotr in arraySotrForParsing:
        worker = Worker()

        deportament = ""
        passParent = False
        for dep in sotr.parents:
            passParent = not passParent
            if passParent:
                continue
            temp = dep.find("span", {"class" : "section-title"}, recursive=False)
            if temp == None:  
                break
            deportament = temp.text + "\n" + deportament
        worker.dep = deportament

        post = sotr.find("div", {"class" : "post"})
        if post != None:
            worker.post = str(post.text)

        fullName = sotr.find("div", {"class" : "fio"})
        if fullName != None:
            worker.fio = str(fullName.text)

        email = sotr.find("a")
        if email != None:
            worker.email = str(email.text)

        telefonTag = sotr.find(string = FIND_TELEFON)
        if telefonTag != None:
            parentTagTelefon = telefonTag.parent.parent
            parentTagTelefon.span.decompose()
            worker.telefon = str(parentTagTelefon.text)[1:]

        telefonVnTag = sotr.find(string = FIND_VN_TELEFON)
        if telefonVnTag != None:
            parentTelefonVnTag = telefonVnTag.parent.parent
            parentTelefonVnTag.span.decompose()
            worker.telefonVn = str(parentTelefonVnTag.text)[1:]

        kabTag = sotr.find(string = FIND_KAB)
        if kabTag != None:
            parentKabTag =  kabTag.parent.parent
            parentKabTag.span.decompose()
            worker.kab = str(parentKabTag.text)[1:]

        faxTag = sotr.find(string = FIND_FAX)
        if faxTag != None:
            parentfaxTag = faxTag.parent.parent
            parentfaxTag.span.decompose()
            worker.fax = str(parentfaxTag.text)[1:]
        arrayWorkers.append(worker)

    return arrayWorkers


def getArraySotrForDB():
    arrayWorkers = getArraySotr()
    ArraySotrForDB = []
    for worker in arrayWorkers:
        if conversionFIOToFamilia(worker.fio) == "" or conversionFIO(worker.fio) == "":
            continue
        row = (conversionFIOToFamilia(worker.fio), conversionFIO(worker.fio), worker.makeCard())
        ArraySotrForDB.append(row)
    return ArraySotrForDB