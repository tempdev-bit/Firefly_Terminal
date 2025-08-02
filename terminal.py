import os
import datetime
import cmd
import random
import subprocess
import platform
import shlex

ASCII_ART =f"""                           
 _____ _         ___ _     
|   __|_|___ ___|  _| |_ _ 
|   __| |  _| -_|  _| | | |
|__|  |_|_| |___|_| |_|_  |
                      |___|
"""

LUFFY_ART =f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⠀⠀⠀⢠⣾⣧⣤⡖⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠋⠀⠉⠀⢄⣸⣿⣿⣿⣿⣿⣥⡤⢶⣿⣦⣀⡀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡆⠀⠀⠀⣙⣛⣿⣿⣿⣿⡏⠀⠀⣀⣿⣿⣿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠷⣦⣤⣤⣬⣽⣿⣿⣿⣿⣿⣿⣿⣟⠛⠿⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠋⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡆⠀⠀
⠀⠀⠀⠀⣠⣶⣶⣶⣿⣦⡀⠘⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠈⢹⡏⠁⠀⠀
⠀⠀⠀⢀⣿⡏⠉⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡆⠀⢀⣿⡇⠀⠀⠀
⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡘⣿⣿⣃⠀⠀⠀
⣴⣷⣀⣸⣿⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠹⣿⣯⣤⣾⠏⠉⠉⠉⠙⠢⠀
⠈⠙⢿⣿⡟⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣄⠛⠉⢩⣷⣴⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣀⡠⠋⠈⢿⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

STRAWHAT_ART = f"""
⠀⠀⡶⠛⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡶⠚⢲⡀⠀
⣰⠛⠃⠀⢠⣏⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣀⡀⠀⠀⠀⣸⡇⠀⠈⠙⣧
⠸⣦⣤⣄⠀⠙⢷⣤⣶⠟⠛⢉⣁⣠⣤⣤⣤⣀⣉⠙⠻⢷⣤⡾⠋⢀⣠⣤⣴⠟
⠀⠀⠀⠈⠳⣤⡾⠋⣀⣴⣿⣿⠿⠿⠟⠛⠿⠿⣿⣿⣶⣄⠙⢿⣦⠟⠁⠀⠀⠀
⠀⠀⠀⢀⣾⠟⢀⣼⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣷⡄⠹⣷⡀⠀⠀⠀
⠀⠀⠀⣾⡏⢠⣿⣿⡯⠤⠤⠤⠒⠒⠒⠒⠒⠒⠒⠤⠤⠽⣿⣿⡆⠹⣷⡀⠀⠀
⠀⠀⢸⣟⣡⡿⠿⠟⠒⣒⣒⣈⣉⣉⣉⣉⣉⣉⣉⣁⣒⣒⡛⠻⠿⢤⣹⣇⠀⠀
⠀⠀⣾⡭⢤⣤⣠⡞⠉⠉⢀⣀⣀⠀⠀⠀⠀⢀⣀⣀⠀⠈⢹⣦⣤⡤⠴⣿⠀⠀
⠀⠀⣿⡇⢸⣿⣿⣇⠀⣼⣿⣿⣿⣷⠀⠀⣼⣿⣿⣿⣷⠀⢸⣿⣿⡇⠀⣿⠀⠀
⠀⠀⢻⡇⠸⣿⣿⣿⡄⢿⣿⣿⣿⡿⠀⠀⢿⣿⣿⣿⡿⢀⣿⣿⣿⡇⢸⣿⠀⠀
⠀⠀⠸⣿⡀⢿⣿⣿⣿⣆⠉⠛⠋⠁⢴⣶⠀⠉⠛⠉⣠⣿⣿⣿⡿⠀⣾⠇⠀⠀
⠀⠀⠀⢻⣷⡈⢻⣿⣿⣿⣿⣶⣤⣀⣈⣁⣀⡤⣴⣿⣿⣿⣿⡿⠁⣼⠟⠀⠀⠀
⠀⠀⠀⢀⣽⣷⣄⠙⢿⣿⣿⡟⢲⠧⡦⠼⠤⢷⢺⣿⣿⡿⠋⣠⣾⢿⣄⠀⠀⠀
⢰⠟⠛⠟⠁⣨⡿⢷⣤⣈⠙⢿⡙⠒⠓⠒⠓⠚⣹⠛⢉⣠⣾⠿⣧⡀⠙⠋⠙⣆
⠹⣄⡀⠀⠐⡏⠀⠀⠉⠛⠿⣶⣿⣦⣤⣤⣤⣶⣷⡾⠟⠋⠀⠀⢸⡇⠀⢠⣤⠟
⠀⠀⠳⢤⠼⠃⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠘⠷⢤⠾⠁⠀
"""

class fireflyTerminal(cmd.Cmd):
    intro = ASCII_ART + f"Type 'help' to see all commands!"
    

    def do_echo(self,arg):
        "Echo the input text: echo [text]"
        print(f"{arg}")


    def do_time(self,arg):
        "Display current time: time"
        #fix ts stupid bug becuse ts pmo so bad
        now = time = datetime.datetime.now()
        print(time)


    def do_about(self,arg):
        "Display info about the terminal"
        print(f"Welcome to Firefly! This is a small demo!")


    def do_clear(self,arg):
        "Clears the terminal"
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ASCII_ART)


    def do_py(self,arg):
        "Execute python code!"
        try:
            result=eval(arg)
            if result is not None:
                print(f"Result: {result}")
        except Exception:
            try:
                exec(arg)
            except Exception as e:
                print(f"Errror: {e}")
    

    def do_calc(self, arg):
        "Calculator!: calc [mathematical expression; + - * /]"
        if not arg:
            print(f"Usage: calc [mathematical expression; + - * /]")
            return
        try:
            result = eval(arg, {"__builtins__": {}})
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


    def do_cd(self,path):
        "Change directory!"
        if not path:
            print(f"How to use: cd [path name]! ")
            return
        try:
            os.chdir(os.path.expanduser(path))
            print(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print("Errror: {e}")
    

    def do_ls(self,arg):
        "List all files in current directory!"
        try:
            entries = os.listdir(os.getcwd())
            for entry in entries:
                full_path = os.path.join(os.getcwd(), entry)
                if os.path.isdir(full_path):
                    print(f"{entry}/")
                else:
                    print(f"{entry}")
        except Exception as e:
            print(f"Error: {e}")
    

    def do_pwd(self, arg):
        "Show current directory"
        print(f"{os.getcwd()}")


    def do_ping(self, arg):
        "Ping a website!"
        if not arg:
            print("Usage: ping <hostname or IP>")
            return
        args = shlex.split(arg)
        command = ['ping', '-c', '8'] + args  # Send 8 packets by default
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True) as proc:
                for line in proc.stdout:
                    print(line, end='')  # `end=''` to avoid double newlines
        except FileNotFoundError:
            print("Error: 'ping' command not found. Is it installed?")
        except Exception as e:
            print(f"An error occurred: {e}")


    def do_exit(self,arg):
        "Exits the terminal!"
        print("Exiting firefly..")
        return True


    def do_fly(self,arg):
        "Creates a new file!"
        if not arg:
            print(f"Usage: fly [filename]")
            return
        try:
            with open(arg, 'x') as f:
                pass
            print(f"File created: {arg}")
        except FileExistsError:
            print(f"File already exists!: {arg}")
        except Exception as e:
            print(f"Error: {e}")
    

    def do_cat(self,arg):
        "View contents of a text file!"
        if not arg:
            print(f"Usage: cat [filename]")
        try:
            with open(arg, 'r') as f:
                print(f"{f.read()}")
        except FileNotFoundError:
            print(f"No file found!")
        except Exception as e:
            print(f"Error: {e}")


    def do_append(self, arg):
        "Append text to a file: append [filename]"
        if not arg:
            print(f"Usage: append [filename]")
            return
        try:
            with open(arg, 'a') as f:
                print(f"Enter text to append! Type :wq on a new line to save.")
                while True:
                    line = input()
                    if line.strip() == ':wq':
                        break
                    f.write(line + '\n')
            print(f"Appended to file: {arg}")
        except Exception as e:
            print(f"Error: {e}")


    def do_overwrite(self, arg):
        "Edit a text file line-by-line: edit [filename]"
        if not arg:
            print(f"Usage: edit [filename]")
            return
        try:
            content = []
            print(f"Enter your text. Type ':wq' on a new line to save and quit.")
            while True:
                line = input()
                if line.strip() == ':wq':
                    break
                content.append(line)
            with open(arg, 'w') as f:
                f.write('\n'.join(content) + '\n')
            print(f"File saved: {arg}")
        except Exception as e:
            print(f"Error: {e}")

    
    def do_open(self, arg):
        "Open a file using the system's default app: open [filename]"
        if not arg:
            print(f"Usage: open [filename]")
            return
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(arg)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", arg], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", arg], check=True)
            else:
                print(f"Unsupported OS: {system}")
                return
            print(f"Opened: {arg}")
        except Exception as e:
            print(f"Error: {e}")


    def do_rm(self, arg):
        "Deletes a file!"
        if not arg:
            print(f"Usage: rm [filename]")
            return
        try:
            os.remove(arg)
            print(f"Deleted file: {arg}")
        except FileNotFoundError:
            print(f"File not found: {arg}")
        except Exception as e:
            print(f"Error: {e}")


    def do_find(self, arg):
        "Search for a file in CURRENT directory tree: find [filename]"
        if not arg:
            print(f"Usage: find [filename]")
            return
        for root, dirs, files in os.walk('.'):
            if arg in files:
                full_path = os.path.join(root, arg)
                print(f"Found: {full_path}")
                return
        print(f"File is not found / File doesn't exist")


    def do_rename(self, arg):
        "Renames the file: rename [old] [new]"
        print(f"Rename a file: rename [old][new]")
        parts = arg.split()
        if len(parts) != 2:
            print(f"Usage: rename [old] [new]")
        old, new = parts
        try:
            os.rename(old,new)
            print(f"Renamed: {old} -> {new}")
        except FileNotFoundError:
            print(f"File not found: {old}")
        except Exception as e:
            print(f"Error: {e}")


    def do_mkdir(self, arg):
        "Create a new directory!: mkdir [name]"
        if not arg:
            print(f"Usage: mkdir [name]")
            return
        try:
            os.makedirs(arg)
            print(f"Directory created!: {arg}")
        except FileExistsError:
            print(f"Directory already exists!: {arg}")
        except Exception as e:
            print(f"Error: {e}")

    def do_rmdir(self, arg):
        "Deletes directory!: rmdir [name]"
        if not arg:
            print(f"Usage: rmdir [name]")
            return
        try:
            os.rmdir(arg)
            print(f"Directory destroyed!: {arg}")
        except FileNotFoundError:
            print(f"Directory doesn't exists!: {arg}")
        except OSError:
            print(f"Directory not empty!")
        except Exception as e:
            print(f"Error: {e}")

    def do_stat(self, arg):
        "Show details about a file or directory: stat [name]"
        if not arg:
            print(f"Usage: stat [filename or directory]")
            return
        try:
            info = os.stat(arg)
            print(f"Stats for: {arg}")
            print(f"Size      : {info.st_size} bytes")
            print(f"Modified  : {time.ctime(info.st_mtime)}")
            print(f"Created   : {time.ctime(info.st_ctime)}")
            print(f"Is Dir    : {os.path.isdir(arg)}")
            print(f"Is File   : {os.path.isfile(arg)}")
        except Exception as e:
            print(f"Error: {e}")


    def do_flip(self, arg):
        "Flips a coin!"
        result = random.choice(['Heads' , 'Tails'])
        print(f"You flipped: {result}")


    def do_roll(self, arg):
        "Rolls a dice: roll [sides] ; minimum=2 default=6 maximum=20"
        try:
            sides = int(arg) if arg else 6
            if not 1 < sides <= 20:
                print(f"Please choose a number from 2 to 20")
            result = random.randint(1, sides)
            print(f"You rolled a {sides}-sided dice: {result}")
        except ValueError:
            print(f"Usage: roll [sides]")
    

    def do_rps(self, arg):
        "Play Rock-Paper-Scissors!"
        options = ['rock' , 'paper' , 'scissors']
        user = input(f"Choose rock, paper, or scissors:").strip().lower()
        if user not in options:
            print(f"Invalid choice! Choose rock, paper or scissor")
            return
        comp = random.choice(options)
        print(f"Computer chose: {comp}")
        if user == comp:
            print(f"IT'S A TIE!")
        elif (user == 'rock' and comp == 'scissors') or \
        (user == 'paper' and comp == 'rock') or \
        (user == 'scissors' and comp == 'paper'):
            print(f"You win!")
        else:
            print(f"You lose!")


    def do_race(self,arg):
        "Play a race!"
        print(f"Welcome to the Number Race!")
        print(f"First to exactly reach a random number between 40 and 60 wins!")
        score = 0
        turn = 'user'
        randomNumber = random.randint(40, 60)
        while score < randomNumber:
            print(f"Current score: {score}")
            if turn == 'user':
                try:
                    user_choice = int(input(f"Your turn! Add any number from 1 to 10!"))
                    if user_choice not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                        print(f"Invalid! Add any number from 1 to 10")
                        continue
                except ValueError:
                    print(f"Please enter a number!")
                    continue
                score += user_choice
                turn = 'computer'
            else:
                comp_choice = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                print(f"Computer adds: {comp_choice}")
                score += comp_choice
                turn = 'user'
            
            if score > randomNumber:
                print(f"Oops! You went over the number.")
                print(f"Game over. No winner.")
            return
        winner = "You" if turn == 'computer' else "Computer"
        print(f"Final score: {randomNumber}")
        print(f"{winner} wins!")

    def do_games(self, arg):
        "List all available games: games"
        print(f"Available Games:")
        print(f"- flip       : Flip a coin")
        print(f"- roll [n]   : Roll a dice (default 6, max 20)")
        print(f"- rps        : Rock-Paper-Scissors")
        print(f"- race       : Race to a number game (number game)")


    def do_luffy(self,arg):
        "Luffy!"
        print(f"{LUFFY_ART}")


    def do_strawhats(self,arg):
        "THE JOLLY ROGER!"
        print(f"{STRAWHAT_ART}")



if __name__ == '__main__':
    fireflyTerminal().cmdloop()