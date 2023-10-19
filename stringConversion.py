

def deleteSpace(str):
    return str.replace(" ", "")

def conversionFIOToFamilia(fio):
    fio = fio.strip()
    if fio.find(' ') != -1:
        fio = fio[:fio.find(' ')]
    fio = fio.lower()
    return fio


def conversionFIO(fio):
    if fio.find('(') != - 1:
        fio = fio[:fio.find('(')]
    fio = deleteSpace(fio)
    fio = fio.lower()
    return fio