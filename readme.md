### What it is?

It is a simple game that shows how to use [LCDManager](git@bitbucket.org:kosci/lcdmanager.git) **version 0.2.x** 
and [CharLCD](https://bitbucket.org/kosci/charlcd). 
They are libraries for Raspberry Pi that make usage of HD44870 easier.
 In game you control small missile launcher :D that shoots at DMO (Defined Moving Object)
  An in return DMO is dropping bombs at you.
  
  Game shows how to refresh screen and parse events. 
  
  Read more: [koscis.wordpress.com](https://koscis.wordpress.com)
  
## Game displays
  
  Game uses any HD44870 display in fact it may use two of them. First is for game and second for scoreboard.
  If you omnit second display no score is displayed.
  
  See main.py
  
    lcd_one = buffered.CharLCD(20, 4, Gpio(), 0, 0)
    lcd_one.init()

    drv = I2C(0x3a, 1)
    drv.pins['E2'] = 6
    lcd_three = buffered.CharLCD(40, 4, drv, 0, 0)
    lcd_three.init()

    vlcd_main = virtual_buffered.CharLCD(16, 4)
    vlcd_main.add_display(0, 0, lcd_one, 4, 0)
    vlcd_main.init()

    vlcd_support = virtual_buffered.CharLCD(4, 4)
    vlcd_support.add_display(0, 0, lcd_one)
    vlcd_support.init()

    game_manager = manager.Manager(vlcd_main)
    score_manager = manager.Manager(vlcd_support)

    # game_manager = manager.Manager(lcd_one)
    # score_manager = manager.Manager(lcd_three)

    my_game = game.Piader(game_manager, score_manager)
    my_game.main_loop()
    
As you can see three displays are initialized:

    - 20x4 connected by GPIO
    - 40x4 by i2c
    - 16x2 by i2c
    
And as default one 20x4 is used but divided to two vlcds. Vlcd is a concept from CharLCD library. 
You may define virtual display on any number of lcds.    
 
## Events
 
 To control player or move on menu use **WSAD** and **SPACE** keys. 
 There is also simple event server implementaion see event_server. 
 
## Views
 
 View is a separate file with widget description and initialization. By using pane I change active view and display what is required.
 First view is main menu, second options and third game. There are also supporting views like game over and scoreboard.
  See views folder for samples how to use manger and its widgets
  
## Main loop
  This loop takes event from queue, send it to view to parse it and render new frame.
  
  
        while self.option['game_on']:
            start = time.time()
            self.local_keyboard.read()
            action = self._get_action()
            self.views[self.option['gui_current_tab']].loop(action)
            if self.score_manager:
                self.scoreboard_view.loop(action)
            self.tick()

            end = time.time()
            if end - start < self.option['game_tick']:
                t_delta = end - start
                time.sleep(max(0, self.option['game_tick'] - t_delta))
                
        def tick(self):
            """render view"""
            self.game_manager.render()
            self.game_manager.flush()
            if self.score_manager:
                self.score_manager.render()
                self.score_manager.flush()
                                

                                
