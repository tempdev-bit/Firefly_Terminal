import os
import datetime
import cmd
import random
import subprocess
import platform
import shlex
import psutil
from colorama import Fore, Style, init

# Initialize colorama with autoreset so we don't need to reset manually each time
init(autoreset=True)


#---------------------ASCII ART-------------------#
# Main ASCII art in blue
ASCII_ART = f"""{Fore.BLUE}                           
 _____ _         ___ _     
|   __|_|___ ___|  _| |_ _ 
|   __| |  _| -_|  _| | | |
|__|  |_|_| |___|_| |_|_  |
                      |___|
{Style.RESET_ALL}"""

LUFFY_ART = f"""{Fore.YELLOW}
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
{Style.RESET_ALL}"""

STRAWHAT_ART = f"""{fore.BLUE}
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
{Style.RESET_ALL}"""


#=========================ALL COMMANDS============================#

class fireflyTerminal(cmd.Cmd):
    intro = ASCII_ART + f"{Fore.GREEN}Type 'help' to see all commands!{Style.RESET_ALL}"
    prompt = f"{Fore.BLUE}firefly> {Style.RESET_ALL}"



    #-------------------------BASICS----------------------------#

    #echoes statement
    def do_echo(self, arg):
        print(f"{Fore.GREEN}{arg}{Style.RESET_ALL}")


    #shows memory stats (psutil)
    def do_statmemory(self, arg):
        memory = psutil.virtual_memory()
        print(f"{Fore.GREEN}Total Memory: {memory.total / (1024 ** 3):.2f} GB{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Available Memory: {memory.available / (1024 ** 3):.2f} GB{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Used Memory: {memory.used / (1024 ** 3):.2f} GB{Style.RESET_ALL}")


    #shows disk stats (psutil)
    def do_statdisk(self, arg):
        disk = psutil.disk_usage('/')
        print(f"{Fore.GREEN}Total Disk Space: {disk.total / (1024 ** 3):.2f} GB{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Used Disk Space: {disk.used / (1024 ** 3):.2f} GB{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Free Disk Space: {disk.free / (1024 ** 3):.2f} GB{Style.RESET_ALL}")


    #shows OS, machine, processor using 'platform' (will be remade into a neofetch clone)
    def do_sysinfo(self, arg):
        sys_info = f"""
        {Fore.GREEN}System Info:
        OS: {platform.system()} {platform.release()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        Python Version: {platform.python_version()}
        {Style.RESET_ALL}
        """
        print(sys_info)


    #shows time, will change later to support timezones
    def do_time(self, arg):
        now = datetime.datetime.now()
        print(f"{Fore.GREEN}{now}{Style.RESET_ALL}")


    #simple timer implemetation
    def do_timer(self, arg):
        try:
            seconds = int(arg)
            print(f"{Fore.BLUE}Starting countdown...{Style.RESET_ALL}")
            for remaining in range(seconds, 0, -1):
                print(f"{Fore.GREEN}{remaining} seconds remaining...{Style.RESET_ALL}", end="\r")
                time.sleep(1)
            print(f"{Fore.YELLOW}Time's up!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number of seconds.{Style.RESET_ALL}")
    

    #about
    def do_about(self, arg):
        print(f"{Fore.GREEN}Welcome to Firefly! This is a small demo!{Style.RESET_ALL}")


    #clears the screen
    def do_clear(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ASCII_ART)


    #simple in-terminal python executer
    def do_py(self, arg):
        try:
            result = eval(arg)
            if result is not None:
                print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except Exception:
            try:
                exec(arg)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #simple calculator (+, -, *, /)
    def do_calc(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: calc [expression]{Style.RESET_ALL}")
            return
        try:
            result = eval(arg, {"__builtins__": {}})
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #change directory (cd)
    def do_cd(self, path):
        if not path:
            print(f"{Fore.RED}Usage: cd [path]{Style.RESET_ALL}")
            return
        try:
            os.chdir(os.path.expanduser(path))
            print(f"{Fore.GREEN}Changed directory to {os.getcwd()}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #shows files and folders in directory
    def do_ls(self, arg):
        try:
            entries = os.listdir(os.getcwd())
            for entry in entries:
                full_path = os.path.join(os.getcwd(), entry)
                if os.path.isdir(full_path):
                    print(f"{Fore.BLUE}{entry}/{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}{entry}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #shows current working directory
    def do_pwd(self, arg):
        print(f"{Fore.GREEN}{os.getcwd()}{Style.RESET_ALL}")


    #simple ping implemetation
    def do_ping(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: ping <hostname or IP>{Style.RESET_ALL}")
            return
        args = shlex.split(arg)
        command = ['ping', '-c', '8'] + args
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True) as proc:
                for line in proc.stdout:
                    print(f"{Fore.GREEN}{line}{Style.RESET_ALL}", end='')
        except FileNotFoundError:
            print(f"{Fore.RED}Error: 'ping' command not found.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")


    #exits firefly into terminal
    def do_exit(self, arg):
        print(f"{Fore.YELLOW}Exiting Firefly...{Style.RESET_ALL}")
        return True



    #-------------------------------------FILES & FOLDERS -------------------------------#

    #creates files
    def do_fly(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: fly [filename]{Style.RESET_ALL}")
            return
        try:
            with open(arg, 'x') as f:
                pass
            print(f"{Fore.GREEN}File created: {arg}{Style.RESET_ALL}")
        except FileExistsError:
            print(f"{Fore.RED}File already exists: {arg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #reads and displays files
    def do_cat(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: cat [filename]{Style.RESET_ALL}")
            return
        try:
            with open(arg, 'r') as f:
                print(f"{Fore.GREEN}{f.read()}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}No file found!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #used to edit file
    def do_append(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: append [filename]{Style.RESET_ALL}")
            return
        try:
            with open(arg, 'a') as f:
                print(f"{Fore.BLUE}Enter text to append. Type :wq to save.{Style.RESET_ALL}")
                while True:
                    line = input()
                    if line.strip() == ':wq':
                        break
                    f.write(line + '\n')
            print(f"{Fore.GREEN}Appended to file: {arg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #overwrites everything in file
    def do_overwrite(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: overwrite [filename]{Style.RESET_ALL}")
            return
        try:
            content = []
            print(f"{Fore.BLUE}Enter your text. Type ':wq' to save.{Style.RESET_ALL}")
            while True:
                line = input()
                if line.strip() == ':wq':
                    break
                content.append(line)
            with open(arg, 'w') as f:
                f.write('\n'.join(content) + '\n')
            print(f"{Fore.GREEN}File saved: {arg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #opens file with the default app for your os
    def do_open(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: open [filename]{Style.RESET_ALL}")
            return
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(arg)
            elif system == "Darwin":
                subprocess.run(["open", arg], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", arg], check=True)
            else:
                print(f"{Fore.RED}Unsupported OS: {system}{Style.RESET_ALL}")
                return
            print(f"{Fore.GREEN}Opened: {arg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #removes FILES
    def do_rm(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: rm [filename]{Style.RESET_ALL}")
            return
        try:
            os.remove(arg)
            print(f"{Fore.GREEN}Deleted file: {arg}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}File not found: {arg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #finds FILES
    def do_find(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: find [filename]{Style.RESET_ALL}")
            return
        for root, dirs, files in os.walk('.'):
            if arg in files:
                full_path = os.path.join(root, arg)
                print(f"{Fore.GREEN}Found: {full_path}{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}File not found.{Style.RESET_ALL}")


    #renames FILES
    def do_rename(self, arg):
        parts = arg.split()
        if len(parts) != 2:
            print(f"{Fore.RED}Usage: rename [old] [new]{Style.RESET_ALL}")
            return
        old, new = parts
        try:
            os.rename(old, new)
            print(f"{Fore.GREEN}Renamed: {old} -> {new}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}File not found: {old}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #makes a new directory
    def do_mkdir(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: mkdir [name]{Style.RESET_ALL}")
            return
        try:
            os.makedirs(arg)
            print(f"{Fore.GREEN}Directory created: {arg}{Style.RESET_ALL}")
        except FileExistsError:
            print(f"{Fore.RED}Directory already exists: {arg}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #removes a directory
    def do_rmdir(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: rmdir [name]{Style.RESET_ALL}")
            return
        try:
            os.rmdir(arg)
            print(f"{Fore.GREEN}Directory removed: {arg}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}Directory not found: {arg}{Style.RESET_ALL}")
        except OSError:
            print(f"{Fore.RED}Directory not empty!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    #shows stats for files
    def do_statfile(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: stat [filename]{Style.RESET_ALL}")
            return
        try:
            info = os.stat(arg)
            print(f"{Fore.BLUE}Stats for: {arg}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Size: {info.st_size} bytes{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Modified: {datetime.datetime.fromtimestamp(info.st_mtime)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Created: {datetime.datetime.fromtimestamp(info.st_ctime)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Is Dir: {os.path.isdir(arg)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Is File: {os.path.isfile(arg)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            


    #-------------------------------COOL STUFF------------------------#

    #flips a coin
    def do_flip(self, arg):
        result = random.choice(['Heads', 'Tails'])
        print(f"{Fore.GREEN}You flipped: {result}{Style.RESET_ALL}")


    #rolls a dice (default: 6, range 2:20)
    def do_roll(self, arg):
        try:
            sides = int(arg) if arg else 6
            if not 1 < sides <= 20:
                print(f"{Fore.RED}Please choose a number from 2 to 20{Style.RESET_ALL}")
                return
            result = random.randint(1, sides)
            print(f"{Fore.GREEN}You rolled a {sides}-sided dice: {result}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Usage: roll [sides]{Style.RESET_ALL}")


    #rock-paper-scissors
    def do_rps(self, arg):
        options = ['rock', 'paper', 'scissors']
        user = input(f"{Fore.BLUE}Choose rock, paper, or scissors: {Style.RESET_ALL}").strip().lower()
        if user not in options:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            return
        comp = random.choice(options)
        print(f"{Fore.GREEN}Computer chose: {comp}{Style.RESET_ALL}")
        if user == comp:
            print(f"{Fore.YELLOW}It's a tie!{Style.RESET_ALL}")
        elif (user == 'rock' and comp == 'scissors') or \
             (user == 'paper' and comp == 'rock') or \
             (user == 'scissors' and comp == 'paper'):
            print(f"{Fore.GREEN}You win!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}You lose!{Style.RESET_ALL}")


    #simple 8 ball
    def do_8ball(self, arg):
        answers = [
            "Yes, definitely.", "Ask again later.", "No, it's not looking good.", "DON'T"
            "Absolutely!", "I would not count on it.", "Very likely.", "Don't count on it."
        ]
        print(f"{Fore.GREEN}{random.choice(answers)}{Style.RESET_ALL}")


    #rock-paper-scissors PLUS; includes lizard and spock
    def do_rps_plus(self, arg):
        #Rock beats Scissors and Lizard
        #Paper beats Rock and Spock
        #Scissors beats Paper and Lizard
        #Lizard beats Paper and Spock
        #Spock beats Rock and Scissors
        options = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        user = input(f"{Fore.BLUE}Choose rock, paper, scissors, lizard, or spock: {Style.RESET_ALL}").strip().lower()
        if user not in options:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            return
        comp = random.choice(options)
        print(f"{Fore.GREEN}Computer chose: {comp}{Style.RESET_ALL}")

        # Determine winner
        if user == comp:
            print(f"{Fore.YELLOW}It's a tie!{Style.RESET_ALL}")
        elif (user == 'rock' and comp in ['scissors', 'lizard']) or \
             (user == 'paper' and comp in ['rock', 'spock']) or \
             (user == 'scissors' and comp in ['paper', 'lizard']) or \
             (user == 'lizard' and comp in ['paper', 'spock']) or \
             (user == 'spock' and comp in ['rock', 'scissors']):
            print(f"{Fore.GREEN}You win!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}You lose!{Style.RESET_ALL}")


    #TicTacToe setup
    class TicTacToe:
        def __init__(self):
            self.board = [' ' for _ in range(9)]
            self.current_player = 'X'

        def print_board(self):
            print(f"\n{self.board[0]} | {self.board[1]} | {self.board[2]}")
            print("--+---+--")
            print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
            print("--+---+--")
            print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}\n")

        def play(self, move):
            if self.board[move] == ' ':
                self.board[move] = self.current_player
                self.switch_player()
            else:
                print(f"{Fore.RED}Invalid move! Try again.{Style.RESET_ALL}")

        def switch_player(self):
            self.current_player = 'O' if self.current_player == 'X' else 'X'

        def check_winner(self):
            win_conditions = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
                [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
                [0, 4, 8], [2, 4, 6]              # Diagonals
            ]
            for condition in win_conditions:
                if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ' ':
                    return self.board[condition[0]]
            return None


    #TicTacToe
    def do_tictactoe(self, arg):
        game = TicTacToe()
        while True:
            game.print_board()
            try:
                move = int(input(f"{Fore.BLUE}Player {game.current_player}, choose a move (0-8): {Style.RESET_ALL}"))
                if move < 0 or move > 8:
                    print(f"{Fore.RED}Invalid position! Try again.{Style.RESET_ALL}")
                    continue
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
                continue
            game.play(move)
            winner = game.check_winner()
            if winner:
                game.print_board()
                print(f"{Fore.GREEN}Player {winner} wins!{Style.RESET_ALL}")
                break
            elif ' ' not in game.board:
                game.print_board()
                print(f"{Fore.YELLOW}It's a draw!{Style.RESET_ALL}")
                break


    #LUFFY
    def do_luffy(self, arg):
        print(LUFFY_ART)


    #STRAWHATS
    def do_strawhats(self, arg):
        print(STRAWHAT_ART)



if __name__ == '__main__':
    fireflyTerminal().cmdloop()
