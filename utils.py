import json


def open_json(file):
    with open(file) as js:
        return json.load(js)


def update_json(file, dct):
    with open(file, "r+", encoding="utf-8") as fichier:
        data = json.load(fichier)
        data.update(dct)
        fichier.seek(0)
        json.dump(data, fichier, indent=4, ensure_ascii=False)
        fichier.truncate()
