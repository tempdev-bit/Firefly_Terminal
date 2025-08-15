import os
import datetime
import cmd
import random
import subprocess
import platform
import shlex
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

# Yellow ASCII art for fun
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

STRAWHAT_ART = f"""{Fore.YELLOW}
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
    def do_echo(self, arg):
        print(f"{Fore.GREEN}{arg}{Style.RESET_ALL}")

    import psutil

    def do_statmemory(self, arg):
        memory = psutil.virtual_memory()
        print(f"{Fore.GREEN}Total Memory: {memory.total / (1024 ** 3):.2f} GB{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Available Memory: {memory.available / (1024 ** 3):.2f} GB{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Used Memory: {memory.used / (1024 ** 3):.2f} GB{Style.RESET_ALL}")

    def do_time(self, arg):
        now = datetime.datetime.now()
        print(f"{Fore.GREEN}{now}{Style.RESET_ALL}")


    def do_about(self, arg):
        print(f"{Fore.GREEN}Welcome to Firefly! This is a small demo!{Style.RESET_ALL}")


    def do_clear(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ASCII_ART)


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


    def do_calc(self, arg):
        if not arg:
            print(f"{Fore.RED}Usage: calc [expression]{Style.RESET_ALL}")
            return
        try:
            result = eval(arg, {"__builtins__": {}})
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


    def do_cd(self, path):
        if not path:
            print(f"{Fore.RED}Usage: cd [path]{Style.RESET_ALL}")
            return
        try:
            os.chdir(os.path.expanduser(path))
            print(f"{Fore.GREEN}Changed directory to {os.getcwd()}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


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

    def do_pwd(self, arg):
        print(f"{Fore.GREEN}{os.getcwd()}{Style.RESET_ALL}")


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

    def do_exit(self, arg):
        print(f"{Fore.YELLOW}Exiting Firefly...{Style.RESET_ALL}")
        return True


    #-------------------------------------FILES & FOLDERS -------------------------------#
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


    def do_stat(self, arg):
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
    def do_flip(self, arg):
        result = random.choice(['Heads', 'Tails'])
        print(f"{Fore.GREEN}You flipped: {result}{Style.RESET_ALL}")


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


    def do_luffy(self, arg):
        print(LUFFY_ART)


    def do_strawhats(self, arg):
        print(STRAWHAT_ART)



if __name__ == '__main__':
    fireflyTerminal().cmdloop()
