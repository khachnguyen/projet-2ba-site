#Nguyen Khac Huy
#Musungayi Victor
#Khazoum Noelle
import os
import json
import cherrypy
from cherrypy.lib.static import serve_file

import jinja2

import jinja2plugin
import jinja2tool



class TheGame():
    def __init__(self):
            self.scores = self.loadscores()

### The following functions display our different pages ###

    @cherrypy.expose
    def index(self):
        '''Main page '''
        return serve_file(os.path.join(ROOT,'templates/index.html'))

    @cherrypy.expose
    def leaderboard(self):   
        '''Page with the choices you made'''
        if len(self.scores) == 0:
            scores = '<p>No game, no score. Begin a game to see some adventures !</p>'
        else:
            try:
                scores = '<ol id="scores">'
                for i in range(len(self.scores)):
                    score = self.scores[i]
                    if score['Choix2'] == ' ' and score['Choix3'] == ' ':
                        scores += '''<li> <b> GAME {} </b>: Because {} decided to {} like the coward he is,
                        he will never kown what was about to be unfold...
                        <p>Recap : {}, {}</p>
                        </li>'''.format(i+1,score['pseudo'],score['Choix1'],score['pseudo'],score['Choix1'] )
                    elif score['Choix3'] == ' ':
                        scores += '''<li> <b>GAME {} </b>: {} though that to {} was a really good idea 
                        and decided to follow it... It was a decision he was about to regret, 
                        dead thanks to a rabbit.Shame
                        <p>Recap : {}, {}, {}</p>
                        </li>'''.format(i+1,score['pseudo'],score['Choix1'],score['pseudo'],score['Choix1'],score['Choix2'] )
                    elif score['Choix3'] == ' Go check ' and score ['Choix2'] == ' Drone ':
                        scores += '''<li><b>GAME {} </b>: Like a good boy he is, {} went to {} and took a {}. 
                        It manage to distract the weird thingy and {} went 
                        home like a champs
                        <p>Recap : {}, {}, {}, {}</p>
                        </li>'''.format( i+1,score['pseudo'],score['Choix1'],score['Choix2'],score['pseudo'],score['pseudo'],score['Choix1'],score['Choix2'],score['Choix3'])
                    elif score ['Choix2'] == 'Go to the car':
                        scores += '''<li><b>GAME {} </b>: Like a smart boy he is, {}, after a little {}, decided to {} and to{}. 
                        Not so smart after all.. He just had to be more 
                        brave instead of leaving...
                        <p>Recap : {}, {}, {}, {}</p>
                        </li>'''.format( i+1 ,score['pseudo'],score['Choix1'],score['Choix2'],score['Choix3'],score['pseudo'],score['Choix1'],score['Choix2'],score['Choix3'])
                    else:
                        scores += '''<li><b>GAME {} </b>: Like a good boy he is, {} went to {} and took a {}. 
                        It was a good idea but the execution was not there.. 
						<p> Recap : {}, {}, {}, {}</p>
						</li>'''.format( i+1,score['pseudo'],score['Choix1'],score['Choix2'],score['pseudo'],score['Choix1'],score['Choix2'],score['Choix3'])
                scores += '</ol>'
            except KeyError:         #Si le joueur va sur la page des scores, on supprime ses choix de la db.json
                cherrypy.log('Someone didn\'t finish to play')
                del self.scores[i]
                self.savescores()

        return {'scores': scores}

        
    @cherrypy.expose
    def situation1(self):   #Base situation
        '''Return the first situation'''
        return serve_file(os.path.join(ROOT,'templates/situation1.html'))

        
    @cherrypy.expose
    def choix1(self):  #CHOICE 1
        '''Page with the first choice'''
        return serve_file(os.path.join(ROOT,'templates/choix1.html')) 
    @cherrypy.expose
    def choix1A(self):
        return serve_file(os.path.join(ROOT,'templates/choix1A.html')) 
    @cherrypy.expose
    def choix1AA(self):
        return serve_file(os.path.join(ROOT,'templates/choix1AA.html')) 
    @cherrypy.expose
    def choix1AB(self):
        return serve_file(os.path.join(ROOT,'templates/choix1AB.html'))       
    @cherrypy.expose
    def choix1B(self):
        return serve_file(os.path.join(ROOT,'templates/choix1B.html')) 

        
    @cherrypy.expose
    def choix2(self):   #CHOICE 2
        '''Page with the second choice'''
        return serve_file(os.path.join(ROOT,'templates/choix2.html')) 
    @cherrypy.expose
    def choix2A(self):
        return serve_file(os.path.join(ROOT,'templates/choix2A.html'))
    @cherrypy.expose
    def choix2AA(self):
        return serve_file(os.path.join(ROOT, 'templates/choix2AA.html'))
    @cherrypy.expose
    def choix2AB(self):
        return serve_file(os.path.join(ROOT, 'templates/choix2AB.html'))
    @cherrypy.expose
    def choix2B(self): 
        return serve_file(os.path.join(ROOT,'templates/choix2B.html')) 
    @cherrypy.expose
    def choix2BA(self):
        return serve_file(os.path.join(ROOT,'templates/choix2BA.html')) 
    @cherrypy.expose
    def choix2BB(self):
        return serve_file(os.path.join(ROOT,'templates/choix2BB.html'))
    @cherrypy.expose
    def choix2C(self):
        return serve_file(os.path.join(ROOT, 'templates/choix2C.html'))
    @cherrypy.expose
    def choix2CA(self):
        return serve_file(os.path.join(ROOT, 'templates/choix2CA.html'))
    @cherrypy.expose
    def choix2CB(self):
        return serve_file(os.path.join(ROOT, 'templates/choix2CB.html'))

        
    @cherrypy.expose
    def choix3(self):   #CHOICE 3
        '''Page with the third choice'''
        return serve_file(os.path.join(ROOT,'templates/choix3.html'))

    @cherrypy.expose  #Error 404 
    def default(self, attr = 'abc'):
        '''Default message of Error 404'''
        return '<h1> Wait you\'re not suppose to be here \\o/  </h1><p> Are you lost my child ?</p><a href = "/"> Return to the homepage</a>'.encode('utf-8')       

### The following functions add the choices you made into the database ###       
        
    @cherrypy.expose    
    def addPseudo(self, pseudo):  #pseudo
        '''Add the pseudo in the database'''
        if pseudo != ' ' :
            self.scores.append({'pseudo' : pseudo})
            self.savescores()
        raise cherrypy.HTTPRedirect('/situation1')
    
    @cherrypy.expose
    def addchoix1(self, choix):  #CHOIX 1
        '''Add the choice in the database'''        
        self.scores[len(self.scores)-1]['Choix1'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix1')

    @cherrypy.expose
    def addchoix1A(self, choix):  #choix 1A       
        self.scores[len(self.scores)-1]['Choix2'] = choix
        self.scores[len(self.scores) - 1]['Choix3'] = " "
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix1A')
    @cherrypy.expose
    def addchoix1AA(self, choix):    
        self.scores[len(self.scores)-1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix1AA')
    @cherrypy.expose
    def addchoix1AB(self, choix):      
        self.scores[len(self.scores)-1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix1AB')
    @cherrypy.expose
    def addchoix1B(self, choix):   #choix 1B       
        self.scores[len(self.scores)-1]['Choix2'] = choix
        self.scores[len(self.scores)-1]['Choix3'] = " "
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix1B')

     
    @cherrypy.expose
    def addchoix2(self, choix):  #CHOIX 2      
        self.scores[len(self.scores)-1]['Choix1'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2')

    @cherrypy.expose
    def addchoix2A(self, choix): #choix2A   
        self.scores[len(self.scores)-1]['Choix2'] = choix
        self.scores[len(self.scores)-1]['Choix3'] = " "
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2A')
    @cherrypy.expose
    def addchoix2AA(self, choix):    
        self.scores[len(self.scores) - 1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2AA')
    @cherrypy.expose
    def addchoix2AB(self, choix):  
        self.scores[len(self.scores) - 1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2AB')
    @cherrypy.expose
    def addchoix2B(self, choix):  #choix2B   
        self.scores[len(self.scores)-1]['Choix2'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2B')
    @cherrypy.expose
    def addchoix2BA(self, choix):  
        self.scores[len(self.scores)-1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2BA')
    @cherrypy.expose
    def addchoix2BB(self, choix):  
        self.scores[len(self.scores)-1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2BB')
    @cherrypy.expose
    def addchoix2C(self, choix): #choix2C
        self.scores[len(self.scores)-1]['Choix2'] = choix
        self.scores[len(self.scores)-1]['Choix3'] = " "
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2C')
    @cherrypy.expose
    def addchoix2CA(self, choix):   
        self.scores[len(self.scores) - 1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2CA')
    @cherrypy.expose
    def addchoix2CB(self, choix):   
        self.scores[len(self.scores)-1]['Choix3'] = choix
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix2CB')

    @cherrypy.expose
    def addchoix3(self, choix):  #CHOIX 3    
        self.scores[len(self.scores)-1]['Choix1'] = choix
        self.scores[len(self.scores)-1]['Choix2'] = " "
        self.scores[len(self.scores)-1]['Choix3'] = " "
        self.savescores()
        raise cherrypy.HTTPRedirect('/choix3')

### Functions that are called by the admin.py and allowed to get  ###
###                     and delete the data                       ###
 
    @cherrypy.expose
    def getscores(self):  
        """GET route to get aself.scores the links."""
        return json.dumps({
            'scores': self.scores
        }, ensure_ascii=False).encode('utf-8')

    @cherrypy.expose
    def deletescore(self, i):
        """GET route to delete a link."""
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.scores):
            del(self.scores[i])
            result = 'OK'
        return result.encode('utf-8')  

### Acces directly to admin.py thanks to a password and a username ###

    @cherrypy.expose
    def admin(self):
        return serve_file(os.path.join(ROOT,'templates/admin.html'))
        
    @cherrypy.expose
    def login(self, username, password):
        if username =='admin' and password == 'admin':
            os.startfile('admin.py')
            raise cherrypy.HTTPRedirect('/')
        elif username =='root':
            os.startfile('admin.py')
            raise cherrypy.HTTPRedirect('/')
        else:
            raise cherrypy.HTTPRedirect('admin')
			
    @cherrypy.expose
    def shutdown(self):
        '''Shutdown the server'''
        cherrypy.engine.exit()
        
### Database functions  ### 
    
    def loadscores(self):
        """Load scores' database from the 'db.json' file."""
        try:
            with open('db.json', 'r') as file:
                content = json.loads(file.read())
                return content['scores']
        except:
            cherrypy.log('Loading database failed.')
            return []
                                
    def savescores(self):
        '''save the data'''
        try:
            with open('db.json', 'w') as file:
                file.write(json.dumps({
                    'scores': self.scores
                }, ensure_ascii=False))
        except:
            cherrypy.log('Saving database failed.')


    
if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()
    # Launch web server
    ROOT = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(TheGame(), '', 'server.conf')
