import random
import tkinter as tk
from tkinter import ttk
from PIL import Image , ImageTk

class PlayerCharacter:
    def __init__(self, hp, dp, mp,sp,ap, job_name):
        self.hp = hp
        self.ap = ap
        self.dp = dp
        self.sp = sp
        self.mp = mp
        # self.image = image
        self.job_class = job_name

    def stats(self):
        stats = f"HP: {self.hp}, MP: {self.mp}, AP: {self.ap}, DP: {self.dp}, SP: {self.sp}"
        return stats

    def is_alive(self):
        return self.hp>0

    def DOOMSHOTGUN(self, target):
        damage = self.ap - target.dp
        if damage < 0:
            print("Damage negated")
        else:
            target.hp -= damage
            print(f"{self.job_class} attacks {target.job_class} for {damage} damage.\n")

    def defend(self):
        self.dp += 5
        print(f"{self.job_class} defends, raising defense points.\n")

    def heal(self):
            amount = random.randint(10, 20)
            self.hp += amount
            if self.hp > 100:
                self.hp = 100
            print(f"{self.job_class} heals for {amount} HP.\n")

    def use_skill(self, target):
        if self.job_class == "DOOM":
            if self.mp >= 30:
                self.mp -= 30
                damage = random.randint(10, 30)
                target.hp -= damage
                print(f"{self.job_class} uses HELLSWORD on {target.job_class} for {damage} damage.")
            else:
                print("Not enough MP to use the skill.")
                print("You missed your chance\n")
        elif self.job_class == "MASTER":
            if self.mp >= 20:
                self.mp -= 20
                self.ap += 10
                print(f"{self.job_class} uses ENERGYSWORD. Attack power increased.")
            else:
                print("Not enough MP to use the skill.")
                print("You missed your chance\n")

class mobs:
    def __init__(self, hp, dp, mp,sp,ap, job_name):
        self.hp = hp
        self.max_hp = hp
        self.ap = ap
        self.dp = dp
        self.sp = sp
        self.mp = mp
        # self.image = image
        self.job_class = job_name
    
    def stats(self):
        stats = f"HP: {self.hp}, MP: {self.mp}, AP: {self.ap}, DP: {self.dp}, SP: {self.sp}"
        return stats

    def is_alive(self):
        return self.hp>0

    def attack(self, target):
        damage =  self.ap-target.dp
        if damage < 0:
            print("Damage negated")
            target.dp -= 5
        else:
            target.hp -= damage


def actions(choice, champion, mob):
    match choice:
        case "DOOMSHOTGUN":
            champion.DOOMSHOTGUN(mob)
        case "DEFEND":
            champion.defend()
        case "HEAL":
            champion.heal()
        case "SKILL":
            champion.use_skill(mob)
            

# def main():
#     print ("THE ARENA HAS STARTED")
#     champion = None

#     Choosingroles = input("PLS CHOOSE YOUR CHAMPION, DOOMSLAYER/MASTERCHEIF: ")
#     if Choosingroles == 'DOOMSLAYER':
#         champion = PlayerCharacter(100,20,70,20,30,"DOOM")

#     if Choosingroles == "MASTERCHEIF":
#         champion = PlayerCharacter(100,20,70,30,30,"MASTER")

#     turn = 1
#     mob1 = mobs(100, 10, 30, 30, 30, "mob1")
#     mob2 = mobs(100, 20, 30, 30, 40, "mob2")

#     choices = ["DOOMSHOTGUN", "DEFEND", "HEAL", "SKILL"]
#     print("MOB 1 HAS APPEARED")
#     while champion.is_alive() & mob1.is_alive():
#         print(f"------TURN {turn}------")
#         if champion.sp >= mob1.sp:
#             print("YOU:", champion.stats())
#             print("MOB 1:", mob1.stats())

#             print("DOOMSHOTGUN, DEFEND, \nHEAL, SKILL")
#             choice = input("Choose your actions: ")
#             actions(choice, champion, mob1)

#             print("mob1 is attacking")
#             mob1.attack(champion)
#         else:
#             print("YOU:", champion.stats())
#             print("MOB 1:", mob1.stats())

#             print("mob1 is attacking")
#             mob1.attack(champion)

#             print("DOOMSHOTGUN, DEFEND, \nHEAL, SKILL")
#             choice = input("Choose your actions: ")
#             actions(choice, champion, mob1)

#         turn += 1

#     print("MOB 2 HAS APPEARED")
#     while champion.is_alive() & mob2.is_alive():
#         print(f"------TURN {turn}------")
#         if champion.sp >= mob2.sp:
#             print("YOU:", champion.stats())
#             print("MOB 2:", mob2.stats())

#             print("DOOMSHOTGUN, DEFEND, \nHEAL, SKILL")
#             choice = input("Choose your actions: ")
#             while choice not in choices:
#                 choice = input("Choose your actions: ")
#             actions(choice, champion, mob2)

#             print("mob1 is attacking")
#             mob2.attack(champion)
#         else:
#             print("YOU:", champion.stats())
#             print("MOB 2:", mob2.stats())

#             print("mob2 is attacking")
#             mob1.attack(champion)

#             print("DOOMSHOTGUN, DEFEND, \nHEAL, SKILL")
#             choice = input("Choose your actions: ")
#             while choice not in choices:
#                 choice = input("Choose your actions: ")
#             actions(choice, champion, mob2)

#         turn += 1

#     if champion.is_alive():
#         print("YOU WON!!!")
#     else:
#         print("YOU LOSE!!!")

# if __name__ == "__main__":
#     main()

class Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_screen = None
        self.pack(fill=tk.X, expand=True)

        self.log_textbox = tk.Text(self, height=40, width=30)
        self.log_textbox.pack(side="right", padx=10)

        button_div = tk.Frame(self)
        button_div.pack(side='left', padx=10)

        button_game_settings = tk.Button(button_div, text="Game Settings", command=self.show_game_setting_screen)
        button_game_settings.pack(fill="x")

        button_end_game = tk.Button(button_div, text="End Game", command=self.quit_game)
        button_end_game.pack(fill="x")

        self.show_main_screen()

    def show_main_screen(self):
        self.current_screen = Main(self)
        self.current_screen.pack()

    def show_game_setting_screen(self):
        self.current_screen.pack_forget()
        self.current_screen = Setting(self)
        self.current_screen.pack()

    def show_combat_game_screen(self):
        self.current_screen.pack_forget()
        self.current_screen = Game(self)
        self.current_screen.pack()

    def show_choose_character_screen(self):
        self.current_screen.pack_forget()
        self.current_screen = choose(self)
        self.current_screen.pack()
        #image_bg = Image.open("doomslayer.png")
        #image_bg = image_bg.resize((750, 650))
        #self.starting_page = ImageTk.PhotoImage(image_bg)
        #image_frame = tk.Label(self.frame, image=self.starting_page, anchor="center")
        #image_frame.grid()
        

    def quit_game(self):
        self.parent.destroy()

    def output(self, text):
        self.log_textbox.config(state=tk.NORMAL)
        self.log_textbox.insert(tk.END, text + "\n")
        self.log_textbox.see(tk.END)
        self.log_textbox.config(state=tk.DISABLED)

class Main(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        label = tk.Label(self, text="Main Menu", font=("Calibri", 20))
        label.pack()

        button_start_game = tk.Button(self, text="Start Game", command=self.parent.show_choose_character_screen)
        button_start_game.pack()

class Setting(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        label = tk.Label(self, text="Settings")
        label.pack()

        audio_on_off = tk.IntVar()
        audio_on_off.set(1)  # Default value: Audio on

        label_audio = tk.Label(self, text="Audio:")
        radio_audio_on = tk.Radiobutton(self, text="On", variable=audio_on_off, value=1)
        radio_audio_off = tk.Radiobutton(self, text="Off", variable=audio_on_off, value=0)

        label_language = tk.Label(self, text="Language:")
        languages = ["English", "Chinese", "Japanese", "Korean"]
        dropdown_language = ttk.Combobox(self, values=languages)

        label_difficulty = tk.Label(self, text="Difficulty Level:")
        slider_difficulty = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL)

        label_audio.pack()
        radio_audio_on.pack()
        radio_audio_off.pack()

        label_language.pack()
        dropdown_language.pack()

        label_difficulty.pack()
        slider_difficulty.pack()

class choose(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        label = tk.Label(self, text="Choose your champion")
        label.pack()

        character_select = tk.Frame(self)
        character_select.pack(pady=20)
        
        #button_doomslayer = tk.Button(doomslayer_frame, text="DOOMSLAYER", command=self.Doomslayer)
        #button_master = tk.Button(character_select, text="MASTERCHEIF", command=self.Mastercheif)
        
        doomslayer_frame = tk.Frame(character_select)
        doomslayer_frame.pack(side='left')
        image_bg = Image.open("doomslayer.png")
        image_bg = image_bg.resize((100, 170))
        self.starting_page = ImageTk.PhotoImage(image_bg)
        image_frame = tk.Button(doomslayer_frame, image=self.starting_page, anchor="center",command = self.Doomslayer)
        image_frame.pack()
        
        mastercheif_frame = tk.Frame(character_select)
        mastercheif_frame.pack(side ='left')
        image_mc = Image.open("mastercheif.png")
        image_mc = image_mc.resize((100,170))
        self.imagemc = ImageTk.PhotoImage(image_mc)
        imagemc_frame = tk.Button(mastercheif_frame, image=self.imagemc, anchor="center",command = self.Mastercheif)
        imagemc_frame.pack()
        
        
       
        #button_doomslayer.pack(side="left")
        #button_master.pack(side="left")
    
    def Doomslayer(self):
        Game.champion = PlayerCharacter(100,20,70,20,30,"DOOM")
        self.parent.output("Selected DOOMSLAYER")
        self.parent.show_combat_game_screen()

    def Mastercheif(self):
        Game.champion = PlayerCharacter(100,20,70,30,30,"MASTER")
        self.parent.output("Selected MASTERCHEIF")
        self.parent.show_combat_game_screen()

class Game(tk.Frame):
    champion = None

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Game UI
        # stats_div = tk.Frame(self)
        # stats_div.pack(side="top", pady=10, fill="x")
        # self.champ_stats = tk.Label(stats_div, text="Champ")
        # self.mob_stats = tk.Label(stats_div, text="Mob")
        # self.champ_stats.pack(side="left", padx=(0,200))
        # self.mob_stats.pack(side="right", padx=(200, 0))

        frame_div = tk.Frame(self)
        frame_div.pack()

        champ_div = tk.Frame(frame_div)
        champ_div.pack(side="left", fill="x")
        champ_name = tk.Label(champ_div, text=Game.champion.job_class, font=("Calibri",10))
        champ_name.pack(padx=(0,200))
        champ_img = tk.Label(champ_div, text="img")
        champ_img.pack(anchor="w")
        self.champ_stats = tk.Label(champ_div, text="stats")
        self.champ_stats.pack(anchor="w")

        mob_div = tk.Frame(frame_div)
        mob_div.pack(side="right", fill="x")
        mob_name = tk.Label(mob_div, text="Mob", font=("Calibri",10))
        mob_name.pack(padx=(200,0))
        mob_img = tk.Label(mob_div, text="img")
        mob_img.pack(anchor="e")
        self.mob_stats = tk.Label(mob_div, text="Stats")
        self.mob_stats.pack(anchor="e")

        self.mob1 = mobs(100, 10, 30, 30, 30, "mob1")
        self.mob2 = mobs(100, 20, 30, 30, 40, "mob2")
        self.turn = 1

        if Game.champion.is_alive() & self.mob1.is_alive():
            self.button_doomshotgun = tk.Button(self, text="DOOMSHOTGUN", command=self.doomshotgun_action1)
            self.button_defend = tk.Button(self, text="DEFEND", command=self.defend_action1)
            self.button_heal = tk.Button(self, text="HEAL", command=self.heal_action1)
            self.button_skill = tk.Button(self, text="SKILL", command=self.skill_action1)
            self.button_doomshotgun.pack(side="left", padx=5)
            self.button_defend.pack(side="left", padx=5)
            self.button_heal.pack(side="left", padx=5)
            self.button_skill.pack(side="left", padx=5)
        elif Game.champion.is_alive() & self.mob2.is_alive():
            self.button_doomshotgun = tk.Button(self, text="DOOMSHOTGUN", command=self.doomshotgun_action2)
            self.button_defend = tk.Button(self, text="DEFEND", command=self.defend_action2)
            self.button_heal = tk.Button(self, text="HEAL", command=self.heal_action2)
            self.button_skill = tk.Button(self, text="SKILL", command=self.skill_action2)
            self.button_doomshotgun.pack(side="left", padx=5)
            self.button_defend.pack(side="left", padx=5)
            self.button_heal.pack(side="left", padx=5)
            self.button_skill.pack(side="left", padx=5)

        self.startGame()
    # define a startGame function that handles the game logic.
    # the game logic should be a while loop that checks if the champion and the mob is alive
    # if the champion is alive, then the champion can choose an action
    # if the mob is alive, then the mob will attack the champion
    # the game should end when either the champion or the mob is dead
    # at the start of the turn, the character with the higher speed will go first
    # if the champion and the mob has the same speed, then the champion will go first
    
    def startGame(self):
        choices = ["DOOMSHOTGUN", "DEFEND", "HEAL", "SKILL"]
        self.parent.output("MOB 1 HAS APPEARED")

        # Fight First mob
        if Game.champion.is_alive() & self.mob1.is_alive():
            self.parent.output(f"------TURN {self.turn}------")
            if Game.champion.sp >= self.mob1.sp:
                self.parent.output(f"YOU: {Game.champion.stats()}")
                self.champ_stats.config(text=f"{Game.champion.stats()}")
                self.parent.output(f"MOB 1: {self.mob1.stats()}")
                self.mob_stats.config(text=f"{self.mob1.stats()}")

                self.parent.output("mob1 is attacking")
                self.mob1.attack(Game.champion)
                self.parent.output("------------")
            else:
                self.parent.output(f"YOU: {Game.champion.stats()}")
                self.champ_stats.config(text=f"{Game.champion.stats()}")
                self.parent.output(f"MOB 1: {self.mob1.stats()}")
                self.mob_stats.config(text=f"{self.mob1.stats()}")

                self.parent.output("mob1 is attacking")
                self.mob1.attack(Game.champion)
                self.parent.output("------------")
        # Fight Second mob
        elif Game.champion.is_alive() & self.mob2.is_alive():
            self.parent.output(f"------TURN {self.turn}------")
            if Game.champion.sp >= self.mob1.sp:
                self.parent.output(f"YOU: {Game.champion.stats()}")
                self.champ_stats.config(text=f"{Game.champion.stats()}")
                self.parent.output(f"MOB 2: {self.mob2.stats()}")
                self.mob_stats.config(text=f"{self.mob2.stats()}")

                print("mob2 is attacking")
                self.mob1.attack(Game.champion)
                self.parent.output("------------")
            else:
                self.parent.output(f"YOU: {Game.champion.stats()}")
                self.champ_stats.config(text=f"{Game.champion.stats()}")
                self.parent.output(f"MOB 2: {self.mob2.stats()}")
                self.mob_stats.config(text=f"{self.mob2.stats()}")

                print("mob2 is attacking")
                self.mob1.attack(Game.champion)
                self.parent.output("------------")
        else:
            self.parent.quit_game()

    # mob1
    def doomshotgun_action1(self):
        actions("DOOMSHOTGUN", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    def defend_action1(self):
        actions("DEFEND", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    def heal_action1(self):
        actions("HEAL", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    def skill_action1(self):
        actions("SKILL", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    # mob2
    def doomshotgun_action2(self):
        actions("DOOMSHOTGUN", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    def defend_action2(self):
        actions("DEFEND", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    def heal_action2(self):
        actions("HEAL", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

    def skill_action2(self):
        actions("SKILL", Game.champion, self.mob1)
        self.turn += 1
        self.parent.after(200, self.startGame)

root = tk.Tk()
root.geometry("1000x600")
game = Frame(root)

root.mainloop()


