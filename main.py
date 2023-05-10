import os
import time
from webull import webull, paper_webull
import json
from _secrets import WEBULL_LOGIN_EMAIL, WEBULL_LOGIN_PWD, WEBULL_DEVICE_ID, \
                     WEBULL_TRADING_PIN, WEBULL_SECURITY_DID
from discord_webhook import DiscordWebhook, DiscordEmbed
import traceback

class webullBot:
    
    def __init__(self, paper_trading: bool = False) -> None:
        self._webull = webull()
        self._loggedin = False
  
    def login(self, use_workaround: bool = False) -> bool:
        wb = self._webull
    
        print(f'DID: {WEBULL_SECURITY_DID}')
        if (use_workaround): wb._set_did(WEBULL_SECURITY_DID)

        test = wb.login(username=WEBULL_LOGIN_EMAIL, password=WEBULL_LOGIN_PWD, device_name=WEBULL_DEVICE_ID)
        self._loggedin = wb.get_trade_token(WEBULL_TRADING_PIN)
        self._webull = wb

        return self._loggedin

class positionTracker:
    def __init__(self):
        
        try:
            with open(f"existingPositions.json") as f:
                self.existingPositions = json.load(f)
        except: self.existingPositions = {}
    
    def addPosition(self,position):
        self.existingPositions[position['id']] = position
    
    def pushPositions(self):
        with open("existingPositions.json", "w") as f: f.write(json.dumps(self.existingPositions,indent=4))
    
    def removePosition(self,ID):
        self.existingPositions.pop(ID)
        with open("existingPositions.json", "w") as f: f.write(json.dumps(self.existingPositions,indent=4))
        
class Discord:
    
    def __init__(self):
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        except:
            self.settings = {
                'Webhook URL': '',
                'Username': ''
            }
            with open("settings.json", "w") as f:
                f.write(json.dumps(self.settings, indent=4))
    
        self.wait = True # this will cause the scrip to not immediately call buy alerts from open positions upon start. 
        # useful if you stop the script and start with open positions.
        # unless you're starting the script with 0 open positions in the used webull account every single time, i would not
        # recommend changing this value.
        
        # sell alerts will be called on any existing positions found in the account upon start however.
    
    def sendOrder(self, direction, ticker, strike, side, exp, price):
        
        if self.wait: return
        
        '''
        format A : fancy : plain text message: 
        @yourusername:
        ALERT
        @role @role
        
        format B : clean : plain text message: 
        ALERT
        @role @role
        
        format C : embed : embed message: 
        @role @role
        > embed
        ALERT
        '''
        
        content = f"{direction} {ticker} {strike}{side} {exp} @ {round(float(price),2)}".upper()
        
        '''
        # format a
        webhook = DiscordWebhook(
            url=self.settings['Webhook URL'], 
            username=self.settings['Username'], 
            content=f'<@YOURDISCORDID>:\n**{content.upper()}**\n<@&ROLEID> <@&ROLEID>', 
            rate_limit_retry=True)'''
        
        # default to format B. compatible with nyria's trade bot.
        webhook = DiscordWebhook(
            url=self.settings['Webhook URL'], 
            username=self.settings['Username'], 
            content=f'{content.upper()}\n<@&ROLEID> <@&ROLEID>', 
            rate_limit_retry=True)
        
        '''
        # format c
        webhook = DiscordWebhook(
            url=self.settings['Webhook URL'], 
            username=self.settings['Username'], 
            content=f'<@&ROLEID> <@&ROLEID>', 
            rate_limit_retry=True)
        
        webhook.add_embed(
            DiscordEmbed(title='AddATitleOrRemove', 
                         description=f'>>> {content.upper()}', 
                         color='03b2f8')
        )   '''
             
        response = webhook.execute()
        
       
  
if __name__ == '__main__':
    
    bot = webullBot()
    tracker = positionTracker()
    currentIds = [str(x) for x in tracker.existingPositions.keys()]
    dc = Discord()
    positions = None
    success = "Success!" if (bot.login()) else "Failed!"
    print(f"Logging into webull: {success}")
    tracker.existingPositions = {}
    
    while True:
        
        try:
            while positions is None:
                time.sleep(500/1000)
                try: positions = bot._webull.get_account()['positions']
                except Exception as e:
                    print("[!] critical issue. error info: \n")
                    traceback.print_exc()
                    print() 
                    print('get_account: ')
                    try: print(bot._webull.get_account())
                    except: print('FAILED.')
                    quit()
                    
            for position in positions:
                
                #print(len(tracker.existingPositions.keys())) # used for debugging
                
                ## call a buy alert
                if position['id'] not in tracker.existingPositions.keys():
                    
                    # gather data
                    ticker = position['ticker']['symbol'][:4]
                    try:
                        int(ticker[-1])
                        ticker = ticker[:-1]
                    except: pass
                    direction = 'BTO'
                    side = 'c' if position['optionType'] == 'call' else 'p'
                    
                    # send discord message
                    dc.sendOrder(
                        direction,
                        ticker,
                        position['optionExercisePrice'],
                        side,
                        position['optionExpireDate'].replace('2023-','').replace('-','/'),
                        position['costPrice']
                        )
                    
                    # log internally
                    tracker.addPosition(position)
                    
                else: # position exists already - either an add or a sell
                    
                    # call a buy alert for existing position
                    if int(position['position']) > int(tracker.existingPositions[position['id']]['position']):
                        
                        # gather data
                        ticker = position['ticker']['symbol'][:4]
                        try:
                            int(ticker[-1])
                            ticker = ticker[:-1]
                        except: pass
                        direction = 'BTO'
                        side = 'c' if position['optionType'] == 'call' else 'p'
                        
                        # send discord message
                        dc.sendOrder(
                            direction,
                            ticker,
                            position['optionExercisePrice'],
                            side,
                            position['optionExpireDate'].replace('2023-','').replace('-','/'),
                            position['costPrice']
                            )
                        
                        # log internally 
                        tracker.addPosition(position)
                    
                    # call a trim alert
                    elif int(position['position']) < int(tracker.existingPositions[position['id']]['position']):
                        
                        # gather data
                        ticker = position['ticker']['symbol'][:4]
                        try:
                            int(ticker[-1])
                            ticker = ticker[:-1]
                        except: pass
                        direction = 'TRIM'
                        side = 'c' if position['optionType'] == 'call' else 'p'
                        orders = bot._webull.get_history_orders(status='Filled', count=2)
                        for order in orders:
                            if order['action'] == 'BUY': continue
                            if order['ticker']['symbol'] == position['ticker']['symbol']:
                                price = order['avgFilledPrice']
                                break
                                
                        # send discord message
                        dc.sendOrder(
                            direction,
                            ticker,
                            position['optionExercisePrice'],
                            side,
                            position['optionExpireDate'].replace('2023-','').replace('-','/'),
                            price
                            )
                        
                        # log internally
                        tracker.addPosition(position)
                        
                if position['id'] not in currentIds: currentIds.append(str(position['id']))
            
            # handle sell alerts - which positions aren't there anymore?
            time.sleep(50/1000)
            removeIds = []
            for id, position in tracker.existingPositions.items():
                
                # call a sell alert
                if str(id) not in currentIds:

                    # gather data
                    ticker = position['ticker']['symbol'][:4]
                    try:
                        int(ticker[-1])
                        ticker = ticker[:-1]
                    except: pass
                    direction = 'STC'
                    side = 'c' if position['optionType'] == 'call' else 'p'
                    orders = bot._webull.get_history_orders(status='Filled', count=2)
                    for order in orders:
                        if order['action'] == 'BUY': continue
                        if order['ticker']['symbol'] == position['ticker']['symbol']:
                            price = order['avgFilledPrice']
                            break
                    
                    # send discord message
                    dc.sendOrder(
                        direction,
                        ticker,
                        position['optionExercisePrice'],
                        side,
                        position['optionExpireDate'].replace('2023-','').replace('-','/'),
                        price
                        )
                    
                    # log internally
                    removeIds.append(position['id'])
                    try: currentIds.pop(currentIds.index(str(position['id'])))
                    except: pass
            
            # clean up
            currentIds = []
            for id in removeIds: tracker.removePosition(id)
            tracker.pushPositions()
            print(f"---> {len(tracker.existingPositions.keys())} positions open currently.")   # log
            positions = None
            dc.wait = False
            
            # check again
            
        except Exception as e: 
            traceback.print_exc()
        
                    
            
        
                
        