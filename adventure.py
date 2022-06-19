from asyncio.windows_events import NULL
import os
import sys
import random
import pygame
import Sql_System as Sql

from Werkzeugkasten import Button
from Werkzeugkasten import InputBox


RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)



BUTTON_STYLE = {"hover_color" : BLUE,
                "clicked_color" : GREEN,
                "clicked_font_color" : BLACK,
                "hover_font_color" : ORANGE}


sql = Sql.SQL_System("localhost", "root", "test")



class Hero():
    def __init__(self, datenbank, name, password, gruppe):
        self.db = datenbank
        self.name = name
        self.password = password
        self.gruppe = gruppe

        startLeben = 100.0
        startKampkraft = 100.0
        startLevel = 1

        lebenMult = self.db.sql_select("heroGruppe", "lebenMult","gruppe="+gruppe)
        kampfkraftMult = self.db.sql_select("heroGruppe","kampfkraftMult","gruppe="+gruppe)
        leben = startLeben*float(lebenMult)
        kampfkraft = startKampkraft*float(kampfkraftMult)
        leben = str(leben)
        kampfkraft = str(kampfkraft)
        startLevel = str(startLevel)
        startWaffe = r"'"+self.db.sql_select("heroGruppe", "waffeStart","gruppe="+gruppe)+r"'"

        self.db.sql_insert("hero","("+name+","+password+" , "+leben+", "+kampfkraft+", "+startWaffe+", "+startLevel+", "+gruppe+")")
    
    def get_name(self):
        return self.db.sql_select('hero', 'name', f"passwort={self.password}")
    def get_leben(self):
        return float(self.db.sql_select('hero', 'leben', f"passwort={self.password}"))
    def get_kampkraft(self):
        return float(self.db.sql_select('hero', 'kampfkraft', f"passwort={self.password}"))
    def get_level(self):
        return int(self.db.sql_select('hero', 'level', f"passwort={self.password}"))
    def get_gruppe(self):
        return self.db.sql_select('hero', 'gruppe', f"passwort={self.password}")
    def get_waffe(self):
        return self.db.sql_select('hero', 'waffe', f"passwort={self.password}")
    
    def set_name(self, name):
        self.db.sql_update('hero', 'name',f"{name}",f'passwort={self.password}')
    def set_leben(self, leben):
        self.db.sql_update('hero', 'leben',f"{str(leben)}",f'passwort={self.password}')
    def set_kampfkraft(self, kampfkraft):
        self.db.sql_update('hero', 'kampfkraft',f"{str(kampfkraft)}",f'passwort={self.password}')
    def set_level(self, level):
        self.db.sql_update('hero', 'level',f"{str(level)}",f'passwort={self.password}')                  
    def set_gruppe(self, gruppe):
        self.db.sql_update('hero', 'gruppe',f"{gruppe}",f'passwort={self.password}')
    def set_waffe(self, waffe):
        self.db.sql_update('hero', 'waffe',f"{waffe}",f'passwort={self.password}')

class Login(object):
    benutzer = ""
    passwort = ""
    gruppe = ""
    def __init__(self):
        self.WIDTH, self.HEIGHT = 500, 500
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("Login")
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
        self.fps = 60.0
        self.color = WHITE
        message = "Login"
        self.login_button = Button((0,0,200,50),RED, self.create_hero,
                             text=message, **BUTTON_STYLE)
        self.login_button.rect.center = (self.screen_rect.centerx,(self.HEIGHT//5)*4)
        self.buttons = [self.login_button]
        self.textfeld_benutzer = InputBox((0,0,140,32))
        self.textfeld_benutzer.rect.center = (self.screen_rect.centerx,self.HEIGHT//5)
        self.textfeld_passwort = InputBox((0,0,140,32))
        self.textfeld_passwort.rect.center = (self.screen_rect.centerx,(self.HEIGHT//5)*2)
        self.textfeld_gruppe = InputBox((0,0,140,32))
        self.textfeld_gruppe.rect.center = (self.screen_rect.centerx,(self.HEIGHT//5)*3)
        self.textfelder = [self.textfeld_benutzer, self.textfeld_passwort, self.textfeld_gruppe]

    def create_hero(self):
        if len(self.textfeld_benutzer.text) > 4 and len(self.textfeld_passwort.text) > 4 and (self.textfeld_gruppe.text == 'Tank' or self.textfeld_gruppe.text == 'Kaempfer'):
            self.benutzer = self.textfeld_benutzer.text
            self.passwort = self.textfeld_passwort.text
            self.gruppe = self.textfeld_gruppe.text
            self.done = True
            
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            for button in self.buttons:
                button.check_event(event)
            for textfeld in self.textfelder:
                textfeld.handle_event(event)

    def main_loop(self):
        while not self.done:
            self.clock.tick(self.fps)
            self.event_loop()
            for textfeld in self.textfelder:
                textfeld.update()
            self.screen.fill(self.color)
            for textfeld in self.textfelder:
                textfeld.draw(self.screen)
            for button in self.buttons:
                button.update(self.screen)
            pygame.display.update()
            


if __name__ == "__main__":
    run_it = Login()
    run_it.main_loop()
    spieler = Hero(sql, r"'"+run_it.benutzer+r"'", r"'"+run_it.passwort+r"'", r"'"+run_it.gruppe+r"'")
    
    print(spieler.get_name())
    print(spieler.get_leben())
    print(spieler.get_kampkraft())
    print(spieler.get_gruppe())
    print(spieler.get_waffe())
    print(spieler.get_level())    
    
    spieler.set_name("'hasi'")
    spieler.set_leben(2.0)
    print(spieler.get_name())
    print(spieler.get_leben())
    
    pygame.quit()
    sys.exit()