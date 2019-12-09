import json
import requests
import string
from PyDictionary import PyDictionary
import pickle

def addCard(word, definition):

        url = "http://localhost:8765"
        payload = {}
        params = {
                'note': {
                        'deckName' : 'english-words',
                        'modelName' : 'Basic',
                        'fields' : {
                                'Front' : word,
                                'Back' : definition
                        },
                        'tags' : ['english-vocabulary']
                }
        }

        payload['action'] = 'addNote'
        payload['version'] = 6
        payload['params'] = params
        payload = json.dumps(payload)

        res = requests.post(url, payload)
        if json.loads(res.text)['error'] != None:
                pass

def getDef(word):

        # dictionary = PyDictionary()
        # res = dictionary.meaning(word)
        # answers = []
        # for pos in res.keys():
        #     partofspeech = "<i>" + pos + ".</i>"
        #     defs = "<br>".join(res[pos][:3])
        #     answers.append('<br>'.join((partofspeech, defs)))
        # return '<br>'.join(answers)

        word_id = word

        app_id = '126e337b'
        app_key = '3065891eb941c4e8598d63fa09dd52a5'
        language = 'en'
        url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + language + '/' + word_id.lower()

        print(f'REQUESTING {word_id}')
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key}).json()
        entries = r['results'][0]['lexicalEntries']
        defs = ''
        examples = ''
        for entry in entries:
                partofspeech = "<i>" + entry['lexicalCategory']['text'] + ".</i>"
                d = ': '.join((partofspeech, entry['entries'][0]['senses'][0]['definitions'][0]))
                defs = "<br>".join((defs, d))
                if 'examples' in entry['entries'][0]['senses'][0].keys():
                    examples = "<br>".join((examples, "<i>e.g.</i> \'" + entry['entries'][0]['senses'][0]['examples'][0]['text'] + "\'"))
                else: examples = ''
        answer = defs + '<br>' + examples
        return answer
         

        

def getWords():
        
        return ['cherub', 'nebbish']

def sync():
        url = "http://localhost:8765"
        payload = {}
        params = {}
        payload['action'] = 'sync'
        payload['version'] = 6
        payload['params'] = params
        payload = json.dumps(payload)

        res = requests.post(url, payload)
        

def main():
        seen = pickle.load(open('../data/seen.pkl', 'rb'))
        words = [word for word in getWords() if word not in seen]

        for word in words:
                try:
                        definition = getDef(word)
                        addCard(word, definition)
                except:
                        pass 
        sync()
        seen.extend(words)
        pickle.dump(seen, open('../data/seen.pkl', 'wb'))


if __name__ == '__main__':
        main()
