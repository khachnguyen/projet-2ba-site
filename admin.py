import json
from urllib.request import urlopen
import urllib.request

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

import webbrowser

    
def loaddata():
    '''Return the data, a list of the won games and one of with the lost games'''
    data = urlopen('http://localhost:8080/getscores').read()
    data = json.loads(data.decode('utf-8'))
    titles_win = []
    titles_lose = []
    try:
        for i in range(len(data['scores'])):
            if data['scores'][i]['Choix3'] == ' Go check ' and data['scores'][i]['Choix2'] == ' Drone ':   #Filter the losing and winning choices
                titles_win.append(' Game {} - {} - {}'.format(i + 1, data['scores'][i]['pseudo'], 'Won'))  
            else :
                titles_lose.append(' Game {} - {} - {}'.format(i + 1, data['scores'][i]['pseudo'], 'Lost'))
        
    
    except KeyError:
        del data['scores'][i]
		
    return data['scores'], titles_win, titles_lose
	
class TheGameForm(GridLayout):
    '''Form a grid layout '''
    scores, titles_win, titles_lose = loaddata()
    detail_txt = ObjectProperty()       
    titles_win_spr = ObjectProperty()        
    titles_lose_spr = ObjectProperty() 	
    titles_win_ls_txt = ObjectProperty()
    titles_lose_ls_txt = ObjectProperty()
    label_txt = ObjectProperty()
    i = -1
    
    def result(self, text):
        '''Show the result of the game'''
        if text != ' ':            
            self.i = int(text.split('-')[0].strip().split(' ')[1].strip()) - 1 
            score = self.scores[self.i]
            if score['Choix2'] == ' ' and score['Choix3'] == ' ':               # Show the choices the user made accordinf to their decision
                self.detail_txt.text = '''- Pseudo: {}
- First choice: {}
- Second choice: /
- Third choice: / '''.format(score['pseudo'], score['Choix1'])
            elif score['Choix3'] == ' ':
                self.detail_txt.text = '''- Pseudo: {}
- First choice: {}
- Second choice: {}
- Third choice: /'''.format(score['pseudo'], score['Choix1'],
                            score['Choix2'])
            else :
                self.detail_txt.text = '''- Pseudo: {}
- First choice: {}
- Second choice: {}
- Third choice: {}'''.format(score['pseudo'], score['Choix1'],
                            score['Choix2'], score['Choix3'])
    
    
    def delete(self):     
        '''delete the chosen object form the site and update the interface '''
        data = urlopen('http://localhost:8080/deletescore?i=' + str(self.i))
        data = data.read().decode('utf-8')
        if (data == 'OK'):
            self.detail_txt.text = 'Succesfully deleted'
            self.scores, self.titles_win_spr.values, self.titles_lose_spr.values = loaddata()   #update the text on kivy
            self.titles_win_ls_txt.text , self.titles_lose_ls_txt.text = 'Number of game won :' + str(len(loaddata()[1])), 'Number of game lost :' + str(len(loaddata()[2]))
            self.label_txt.text = str(len(self.scores)) + ' scores loaded.'
			
    def redirecturl(self):
        '''redirect to the site directly'''
        webbrowser.open("http://localhost:8080")
        


class TheGameApp(App):
    title = 'The Game '

TheGameApp().run()