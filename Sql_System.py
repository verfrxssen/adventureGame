from threading import local
import mysql.connector

class SQL_System():
    def __init__(self, localhost, benutzer, passwort): 
        self.my_db = mysql.connector.connect(host=localhost,
                                        user=benutzer,
                                        password=passwort)
        self.sql = self.my_db.cursor()
        self.setup()

    def setup(self):
        sql = self.sql

        sql.execute("DROP DATABASE IF EXISTS adventure")

        self.sql_dropTB("hero")
        self.sql_dropTB("enemy")
        self.sql_dropTB("heroGruppe")
        self.sql_dropTB("enemyGruppe")
        self.sql_dropTB("weapons")

        self.sql_execute("CREATE DATABASE adventure")

        self.sql_createTB("hero","(name VARCHAR(15), passwort VARCHAR(15) PRIMARY KEY, leben DECIMAL(8,4), kampfkraft DECIMAL(8,4), waffe VARCHAR(15), level INT(3), gruppe VARCHAR(15))")
        self.sql_createTB("enemy","(enemyTag INT(3) PRIMARY KEY, leben DECIMAL(8,4), kampfkraft DECIMAL(8,4),name VARCHAR(15), gruppe VARCHAR(15), waffe VARCHAR(15), level INT(3))")
        self.sql_createTB("heroGruppe","(gruppe VARCHAR(15) PRIMARY KEY, lebenMult DECIMAL(8,4), kampfkraftMult DECIMAL(8,4), waffeStart VARCHAR(15), pngName VARCHAR(15))")
        self.sql_createTB("enemyGruppe","(gruppe VARCHAR(15) PRIMARY KEY, lebenMult DECIMAL(8,4), kampfkraftMult DECIMAL(8,4), waffeStart VARCHAR(15), pngName VARCHAR(15))")
        self.sql_createTB("weapons","(name VARCHAR(20) PRIMARY KEY, damage DECIMAL(8,4), attackSpeed DECIMAL(8,4), namePngDatei VARCHAR(20))")

       
        self.sql_insert("heroGruppe","('Tank', 1.5, 0.5, 'swordSmall', 'Tank.png')")
        self.sql_insert("heroGruppe","('Kaempfer', 0.5, 1.5, 'swordMedium', 'Kaempfer.png')")
   
        self.sql_insert("enemyGruppe","('Org', 1.5, 0.5, 'swordSmall', 'Org.png')")
        self.sql_insert("enemyGruppe","('Troll', 0.5, 1.5, 'swordMedium', 'Troll.png')")
     
        self.sql_insert("weapons","('swordSmall', 10.0, 1.0, 'swordSmall.png')")
        self.sql_insert("weapons","('swordMedium', 20.0, 1.0, 'swordMedium.png')")
        self.sql_insert("weapons","('swordFast', 5.0, 3.0, 'swordFast.png')")
    
    def sql_execute(self, befehl):
        sql = self.sql
        sql.execute(befehl)
        print(">> "+befehl)
    
    def sql_insert(self, nameTable, Values):
        self.sql_execute("INSERT INTO adventure."+nameTable+  " VALUES " +Values)

    def sql_select(self, nameTable, searchObj, condition):
        self.sql_execute("SELECT " +searchObj+" FROM adventure."+nameTable+" WHERE "+condition)
        result = self.sql.fetchone()
        result = result[0]
        return result
    
    def sql_update(self, nameTable, updateObj, updateValue, condition):
        self.sql_execute("UPDATE adventure."+nameTable+" SET "+updateObj+"="+updateValue+" WHERE "+condition)
    
    def sql_createTB(self, nameTable, Values):
        self.sql_execute("CREATE TABLE adventure."+nameTable+" "+Values)

    def sql_dropTB(self, nameTable):
        self.sql_execute("DROP TABLE IF EXISTS adventure."+nameTable)
        
