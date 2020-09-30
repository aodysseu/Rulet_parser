from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3


class DB:
    def __init__(self):
        self.con = sqlite3.connect('rulet.db')
        self.cursorObj = self.con.cursor()
        self.con.commit()
        
    def create_table_total(self):
        self.cursorObj.execute(
            '''CREATE TABLE IF NOT EXISTS rulet(game_ID integer, times integer, red_bet integer, green_bet integer, black_bet integer, red_count integer,
            green_count integer, black_count integer, total_color text, total_value integer)''')
        self.con.commit()
    
    def create_table_players(self):
        self.cursorObj.execute(
            '''CREATE TABLE IF NOT EXISTS players(game_ID integer, player_ID integer, bet integer, color text)''')
        self.con.commit()
        
    def insert_table_total(self, game_ID, times, red_bet, green_bet, black_bet, red_count, green_count, black_count, total_color, total_value):
        self.cursorObj.execute('''INSERT INTO rulet(game_ID, times, red_bet, green_bet, black_bet, red_count, green_count, black_count, total_color, total_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (game_ID, times, red_bet, green_bet, black_bet, red_count, green_count, black_count, total_color, total_value))
        self.con.commit()


    def insert_table_players(self, game_ID, player_ID, bet, color):
        self.cursorObj.execute('''INSERT INTO players(game_ID, player_ID, bet, color) VALUES (?, ?, ?, ?)''',
                       (game_ID, player_ID, bet, color))
        self.con.commit()
    

db = DB()
db.create_table_total()
db.create_table_players()
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Profile 1")
driver = webdriver.Chrome(executable_path='D:\chromdriver\chromedriver.exe', chrome_options=options)

driver.get("https://csgopolygon.gg/?language=ru")

btn1 =  driver.find_element_by_class_name("window_steam_button")
btn1.click()
btn2 =  driver.find_element_by_class_name("btn_green_white_innerfade")
btn2.click()

for i in range(1000):   
        time.sleep(10)    
        WebDriverWait(driver, 40).until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="progress"]/span[@class="progress_timer"]'), '***ВРАЩЕНИЕ***'))
    
        game = driver.find_element_by_xpath('//li[@class="ball"][10]').get_attribute("data-rollid")
    
        players = driver.find_elements_by_xpath('//div[@id="panel1-7-t"]//li[@class="list_bet"]')
        red_count = len(players)
        for player in players:
            db.insert_table_players(game, player.get_attribute("id")[:-2], 
                                    player.get_attribute("data-amount"), 'red')
        
        players = driver.find_elements_by_xpath('//div[@id="panel0-0-t"]//li[@class="list_bet"]')
        green_count = len(players)
        for player in players:
            db.insert_table_players(game, player.get_attribute("id")[:-2], 
                                    player.get_attribute("data-amount"), 'green')
        
        players = driver.find_elements_by_xpath('//div[@id="panel8-14-t"]//li[@class="list_bet"]')
        black_count = len(players)
        for player in players:
            db.insert_table_players(game, player.get_attribute("id")[:-2], 
                                    player.get_attribute("data-amount"), 'black')
        
        WebDriverWait(driver, 10).until(lambda driver: "Выпало число" in driver.find_element(By.XPATH, 
                                    '//div[@class="progress"]/span[@class="progress_timer"]').text)
    
        total_number =  driver.find_element(By.XPATH, '//div[@class="progress"]/span[@class="progress_timer"]').text
        total_bets =  driver.find_elements_by_class_name("total")
        times = time.time()
    
        if int(total_number[13:-1]) == 0:
            total_color = 'green'
        elif int(total_number[13:-1]) <= 7:
            total_color = 'red'     
        else:
            total_color = 'black'
            
        total_value = int(total_bets[0].text) + int(total_bets[1].text) + int(total_bets[2].text)
        
        db.insert_table_total(game, times, total_bets[0].text, total_bets[1].text, total_bets[2].text, 
                          red_count, green_count, black_count, total_color, total_value)

driver.quit()
