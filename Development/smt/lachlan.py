import random

print("Welcome to my CompT Game")
print("Please use numbers in this game only!!")

#character stats

class hero:
    def __init__(self, name, hp, max_hp, ap, dp, sp, mp, max_mp, image):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.ap = ap
        self.dp = dp
        self.sp = sp
        self.mp = mp
        self.max_mp = max_mp
        self.image = image
        
    def reset_stats(self):
        self.hp = self.max_hp
        self.mp = self.max_mp

#enemy stats

class enemy:
    def __init__(self, hp, max_hp, ap, dp, sp, image, enemy_type):
        self.hp = hp
        self.max_hp = max_hp
        self.ap = ap
        self.dp = dp
        self.sp = sp
        self.image = image
        self.enemy_type = enemy_type
        
    def reset_stats_enemy(self):
        self.hp = self.max_hp
        
        
#enemies        
        
enemy_choice = random.randint(1, 2)

if enemy_choice == 1:
    enemy1 = enemy(hp=120, max_hp=120, ap=random.randint(8, 18), dp=random.randint(10, 15), sp=10, 
                   image="like a Ugly & Green ", enemy_type="goblin")
                   
elif enemy_choice == 2:
    enemy1 = enemy(hp=100, max_hp=100, ap=random.randint(10, 15), dp=random.randint(5, 10), sp=8,
                      image="handsome but deadly", enemy_type="dark mage")
    
#Hero class
    
players_class = int(input("Please choose your HERO: 1 = Warrior, 2 = Wizard, 3 = Assassin, 4 = Tank"))

### Warrior class

if players_class == 1:
    hero1 = hero("warrior", hp=120, max_hp=120, ap=random.randint(10, 20), dp=random.randint(10, 15), sp=9, 
                 mp=5, max_mp=5, image="A strong and heavily armed warrior")
    
        
    print("You have selected the", hero1.name, "hero")
    print("You wander into a forest...")
    print("SUDDENLY")
    print("You were jumped by a",enemy1.enemy_type, "!")
    print("he looks ",enemy1.image)
    
    while hero1.hp > 0 or enemy1.hp > 0:
        if enemy1.sp < hero1.sp:

            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Heal 4) Warrior Rage ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                if hero1.mp < 2:
                    print("Unable to use, ran out of MP")
                    print("Hence you got attacked for thinking about it")
                elif hero1.hp == hero1.max_hp:
                    print("Already at full HP")
                else:
                    heal_amount = min(25, hero1.max_hp - hero1.hp)
                    hero1.hp += heal_amount
                    print("Healing for", heal_amount, "HP...")
                    hero1.mp -= 2
                    
            elif action == 4:
                print("Activating Warriors Rage")
                
                if hero1.mp >= 3:
                    WR = random.randint(1,2)
                    if WR == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif WR == 2:
                        enemy1.hp -= random.randint(35,55)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
            
            else:
                print("Hero did not input a valid input! ")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
                
            
            if enemy1.hp < 0:
                print("Hero Has won the battle!")
                break
            elif enemy1.hp >= 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked you")
            
            if hero1.hp <= 0:
                print("Hero has lost!")
                break
        else:
            if enemy1.hp > 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked first")
                
            if enemy1.hp <= 0:
                print("Hero Has won the battle!")
                break
                
            elif hero1.hp <= 0:
                print("Hero has lost!")
                break
            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Heal 4) Warrior Rage ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                if hero1.mp < 2:
                    print("Unable to use, ran out of MP")
                    print("Hence you got attacked for thinking about it")
                elif hero1.hp == hero1.max_hp:
                    print("Already at full HP")
                else:
                    heal_amount = min(25, hero1.max_hp - hero1.hp)
                    hero1.hp += heal_amount
                    print("Healing for", heal_amount, "HP...")
                    hero1.mp -= 2
                    
                    
            elif hero1.hp >= 120:
                print("Already at full HP")
            elif hero1.mp <= 0:
                print("Unable to use, ran out of MP")
                print("Hence you got attacked for thinking about it")
                    
            elif action == 4:
                print("Activating Warriors Rage")
                
                if hero1.mp >= 3:
                    WR = random.randint(1,2)
                    if WR == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif WR == 2:
                        enemy1.hp -= random.randint(35,55)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
##======================================================================================================================
## Wizard class

elif players_class == 2:
    hero1 = hero("Wizard", hp=100, max_hp=100, ap=random.randint(10, 15), dp=random.randint(5, 10), sp=7,
                mp=15, max_mp=15, image="a strong magic user")
    
        
    print("You have selected the", hero1.name, "hero")
    print("You wander into a forest...")
    print("SUDDENLY")
    print("You were jumped by a",enemy1.enemy_type, "!")
    print("he looks ",enemy1.image)
    
    while hero1.hp > 0 or enemy1.hp > 0:
        if enemy1.sp < hero1.sp:

            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Flamethrower 4) Water Spear ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                print("Using flamethrower")
                
                if hero1.mp >= 4:
                    flamethrower = random.randint(1,2)
                    if flamethrower == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif flamethrower == 2:
                        enemy1.hp -= random.randint(35,55)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 4:
                print("Using Water Spear")
                
                if hero1.mp >= 5:
                    waterspear = random.randint(1,2)
                    if waterspear == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif waterspear == 2:
                        enemy1.hp -= random.randint(35,55)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
            
            if enemy1.hp < 0:
                print("Hero Has won the battle!")
                break
            elif enemy1.hp >= 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked you")
            
            if hero1.hp <= 0:
                print("Hero has lost!")
                break
        else:
            if enemy1.hp > 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked first")
                
            if enemy1.hp <= 0:
                print("Hero Has won the battle!")
                break
                
            elif hero1.hp <= 0:
                print("Hero has lost!")
                break
            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Flamethrower 4) Water Spear ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                print("Using flamethrower")
                
                if hero1.mp >= 4:
                    flamethrower = random.randint(1,2)
                    if flamethrower == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif flamethrower == 2:
                        enemy1.hp -= random.randint(35,55)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 4:
                print("Using Water Spear")
                
                if hero1.mp >= 5:
                    waterspear = random.randint(1,2)
                    if waterspear == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif waterspear == 2:
                        enemy1.hp -= random.randint(35,55)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
    
##======================================================================================================================
## Assassin class

elif players_class == 3:
    hero1 = hero("Assassin", hp=80, max_hp=80, ap=random.randint(15, 25), dp=random.randint(10, 15), sp=25,
                mp=5, max_mp=5, image="Stealthy and deadly")
    
        
    print("You have selected the", hero1.name, "hero")
    print("You wander into a forest...")
    print("SUDDENLY")
    print("You were jumped by a",enemy1.enemy_type, "!")
    print("he looks ",enemy1.image)
    
    while hero1.hp > 0 or enemy1.hp > 0:
        if enemy1.sp < hero1.sp:

            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Assassinate 4) Backstab ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                print("Using Assassinate")
                
                if hero1.mp >= 2:
                    assnate = random.randint(1,2)
                    if assnate == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif assnate == 2:
                        enemy1.hp -= random.randint(40,50)
                        hero1.mp -= 2
                elif hero1.mp < 2:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 4:
                print("Using Backstab")
                
                if hero1.mp >= 3:
                    backstab = random.randint(1,2)
                    if backstab == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif backstab == 2:
                        enemy1.hp -= random.randint(35,80)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
                
            
            if enemy1.hp < 0:
                print("Hero Has won the battle!")
                break
            elif enemy1.hp >= 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked you")
            
            if hero1.hp <= 0:
                print("Hero has lost!")
                break
        else:
            if enemy1.hp > 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked first")
                
            if enemy1.hp <= 0:
                print("Hero Has won the battle!")
                break
                
            elif hero1.hp <= 0:
                print("Hero has lost!")
                break
            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Assassinate 4) Backstab ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                print("Using Assassinate")
                
                if hero1.mp >= 2:
                    assnate = random.randint(1,2)
                    if assnate == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif assnate == 2:
                        enemy1.hp -= random.randint(40,50)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 4:
                print("Using Backstab")
                
                if hero1.mp >= 5:
                    backstab = random.randint(1,2)
                    if backstab == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif backstab == 2:
                        enemy1.hp -= random.randint(35,80)
                        hero1.mp -= 5
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
                
##======================================================================================================================
## Tank class

if players_class == 4:
    hero1 = hero("Tank", hp=150, max_hp=150, ap=random.randint(20, 35), dp=random.randint(15, 30), sp=2, 
                 mp=8, max_mp=8, image="solid protector")
    
        
    print("You have selected the", hero1.name, "hero")
    print("You wander into a forest...")
    print("SUDDENLY")
    print("You were jumped by a",enemy1.enemy_type, "!")
    print("he looks ",enemy1.image)
    
    while hero1.hp > 0 or enemy1.hp > 0:
        if enemy1.sp < hero1.sp:

            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Transcendence 4) Tank's Rage ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                if hero1.mp < 3:
                    print("Unable to use, ran out of MP")
                    print("Hence you got attacked for thinking about it")
                elif hero1.hp == hero1.max_hp:
                    print("Already at full HP")
                else:
                    heal_amount = min(40, hero1.max_hp - hero1.hp)
                    hero1.hp += heal_amount
                    print("Healing for", heal_amount, "HP...")
                    hero1.mp -= 3
                    
            elif action == 4:
                print("Activating Tank's Rage")
                
                if hero1.mp >= 4:
                    tanksR = random.randint(1,2)
                    if tanksR == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif tanksR == 2:
                        enemy1.hp -= random.randint(50,70)
                        hero1.mp -= 3
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue
                
            
            if enemy1.hp < 0:
                print("Hero Has won the battle!")
                break
            elif enemy1.hp >= 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked you")
            
            if hero1.hp <= 0:
                print("Hero has lost!")
                break
        else:
            if enemy1.hp > 0:
                hero1.hp -= enemy1.ap
                print("the enemy has attacked first")
                
            if enemy1.hp <= 0:
                print("Hero Has won the battle!")
                break
                
            elif hero1.hp <= 0:
                print("Hero has lost!")
                break
            print("Hero|(HP:", hero1.hp, "/", hero1.max_hp, ")|", enemy1.enemy_type, "|(HP:", enemy1.hp, "/" , enemy1.max_hp, ")" )
            print("what will you do??")
            print("Player action:")
            print("1) Attack 2) Defence 3) Transcendence 4) Tank's Rage ")
            print("")
            print("5) Quit 6) Restart")
            
            action = int(input())
            
            if action == 1:
                enemy1.hp -= hero1.ap
                print(enemy1.enemy_type, "has been attacked")
            
            elif action == 2:
                print("DEFENDING....")
                d = random.randint(1,2)
                if d == 1:
                    print("Not successfull") 
                else:
                    hero1.hp += enemy1.ap
                    print("DEFENDED")
                    
            elif action == 3:
                if hero1.mp < 3:
                    print("Unable to use, ran out of MP")
                    print("Hence you got attacked for thinking about it")
                elif hero1.hp == hero1.max_hp:
                    print("Already at full HP")
                else:
                    heal_amount = min(40, hero1.max_hp - hero1.hp)
                    hero1.hp += heal_amount
                    print("Healing for", heal_amount, "HP...")
                    hero1.mp -= 3
                    
            elif action == 4:
                print("Activating Tank's Rage")
                
                if hero1.mp >= 4:
                    tanksR = random.randint(1,2)
                    if tanksR == 1:
                        print("attack has been fumbled")
                        enemy1.hp -= hero1.ap
                        hero1.mp -= 1     
                    elif tanksR == 2:
                        enemy1.hp -= random.randint(50,70)
                        hero1.mp -= 4
                elif hero1.mp < 3:
                    print("Your ran out of Mana not available")
                    print("Hence you got attacked for thinking about it")
                    
            elif action == 5:
                print("Player has quit the game")
                break
        
            elif action == 6:
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                print("Game has restarted")
                continue
                
            else:
                print("Hero did not input a valid input!")
                hero1.reset_stats()
                enemy1.reset_stats_enemy()
                continue

root = tk.Tk()
root.geometry("1000x600")
game = Frame(root)

root.mainloop()