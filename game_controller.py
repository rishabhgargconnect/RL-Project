class GameController:
        def __init__(self, game_object):
            self.game_object = game_object
            print("hello")

        #alive/dead state
        def get_alive(self):
            return not self.game_object.is_game_over()

        def get_dead(self):
            return self.game_object.is_game_over()    

        #restart
        def restart_game(self):
            return self.game_object.restart_game()


        #actions
        def move_left(self):
            return self.game_object.move_left()

        def move_right(self):
            return self.game_object.move_right()    

        def no_action(self):
            return self.game_object.no_action()
            

        #scores and reward
        def get_high_score(self):
            return self.game_object.get_high_score()

        def get_current_score(self):
            return self.game_object.get_current_score()

        def get_current_reward(self):
            return self.game_object.get_current_reward()            


        #screenshot
        def get_screenshot(self):
            return self.game_object.get_screenshot()



        #Game params

        def set_bullet_speed(self, bullet_speed):
            self.game_object.set_bullet_speed(bullet_speed)

        
        def set_number_of_aliens(self, number_of_aliens):
            self.game_object.set_bullet_speed(number_of_aliens)  

        def set_agent_speed(self, agent_speed):
            self.game_object.set_bullet_speed(agent_speed)   
                      

        def set_alien_speed(self, alien_speed):
            self.game_object.set_bullet_speed(alien_speed)             

        def set_alien_speed_increment(self, alien_speed_increment):
            self.game_object.set_bullet_speed(alien_speed_increment)     

