# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python
# Replace the following placeholders with your information.
# Liam Kennedy
# lpkenned@uci.edu
# 81845142

from command_parser import parse_command
from notebook import Notebook, Diary
from pathlib import Path
import traceback
def main() -> None:
    """Contains the main logic and command loop needed to run the Diary program.
    Takes user commands (Q, C, O, E, P) and then with those inputs it will implement 
    the code to the respected command."""
    current_notebook = None
    current_path = None
    while True:
        try:
            user_input = input()
            if not user_input.strip():
                print("ERROR")
                continue
            try:
                command = parse_command(user_input)
            except Exception:
                print("ERROR")
                continue
            if command["type"] == "Q":
               break
       
            elif command["type"] == "C":
                args = command["args"]
                if "-n" not in args or len(args) < 3:
                    print("ERROR")
                    continue
                path_index = args.index("-n") - 1
                if path_index < 0:
                    print("ERROR")
                    continue

                path_str = args[path_index]
                notebook_name = args[args.index("-n") +1]

                path = Path(path_str)
                if not path.exists() or not path.is_dir():
                    print("ERROR")
                    continue
                
                notebook_file = path / f'{notebook_name}.json'
                
                if notebook_file.exists():
                    print("ERROR")
                    continue

                username = input("")
                password = input("")
                bio = input("")

                new_notebook = Notebook(username, password, bio)
                new_notebook.save(notebook_file)

                print(f"{str(notebook_file.resolve()).strip()} CREATED")
                current_notebook = new_notebook
                current_path = notebook_file

            elif command["type"] == "O":
                args = command["args"]
                if len(args) != 1:
                    print("ERROR")
                    continue

                path = Path(args[0])
                if not path.exists() or path.suffix != ".json":
                    print("ERROR")
                    continue

                username = input("")
                password = input("")

                try:
                    notebook_temp = Notebook("", "", "")
                    notebook_temp.load(path)
                    notebook = notebook_temp
                except:
                    print("ERROR")
                    continue
                
                if notebook.username == username and notebook.password == password:
                    print("Notebook loaded.")
                    print(notebook.username)
                    print(notebook.bio)
                    current_notebook = notebook
                    current_path = path
                else:
                    print("ERROR")
            elif command["type"] == "E":
                if current_notebook is None or current_path is None:
                    print("ERROR")
                    continue
                args = command["args"]
                i = 0
                edit_error = False
                while i < len(args):
                    option = args[i]
                    try:
                        if option == "-usr":
                            if i + 1 >= len(args):
                                edit_error = True
                            new_username = args[i + 1]
                            current_notebook.username = new_username
                            current_notebook.save(current_path)
                            i += 2
                        elif option == "-pwd":
                            if i + 1 >= len(args):
                                edit_error = True
                            new_password = args[i + 1]
                            current_notebook.password = new_password
                            current_notebook.save(current_path)
                            i += 2
                        elif option == "-bio":
                            if i + 1 >= len(args):
                                edit_error = True
                            new_bio = args[i + 1]
                            current_notebook.bio = new_bio
                            current_notebook.save(current_path)
                            i += 2
                        elif option == "-add":
                            if i + 1 >= len(args):
                                edit_error = True 
                            new_add = args[i + 1]
                            current_notebook.add_diary(Diary(new_add))
                            current_notebook.save(current_path)
                            i += 2
                        elif option == "-del":
                            if i + 1 >= len(args):
                                edit_error = True
                            try:
                                del_index = int(args[i + 1])
                            except Exception:
                                edit_error = True
                            if not current_notebook.del_diary(del_index):
                                edit_error = True
                            i += 2
                            current_notebook.save(current_path)
                        else:
                            edit_error = True
                        if edit_error:
                            print("ERROR")
                            break  
                    except Exception:
                        print("ERROR")
                        break

            elif command["type"] == "D":
                args = command["args"]
                if len(args) != 1:
                    print("ERROR")
                    continue
                path = Path(args[0])
                if not path.exists() or path.suffix != ".json":
                    print("ERROR")
                    continue
                try:
                    path.unlink()
                    print(f"{str(path.resolve()).strip()} DELETED")
                except Exception:
                    print("ERROR")
                    continue

            elif command["type"] == "P":
                args = command["args"]
                error_p = False
                i = 0
                if current_notebook is None:
                        print("ERROR")
                        continue
                while i < len(args):
                    option = args[i]
                    if option == "-usr":
                        print(current_notebook.username)
                        i += 1
                    elif option == "-pwd":
                        print(current_notebook.password)
                        i += 1
                    elif option == "-bio":
                        print(current_notebook.bio)
                        i += 1
                    elif option == "-diaries":
                        diaries_t = current_notebook.get_diaries()
                        for i, diary in enumerate(diaries_t):
                            print(f"{i}: {diary.entry}") 
                        i += 1
                    elif option == "-diary":
                        if i + 1 >= len(args):
                            error_p = True
                            break
                        try:
                            index_d = int(args[i + 1])
                        except Exception:
                            error_p = True
                            break
                        diaries_test = current_notebook.get_diaries()
                        if 0 <= index_d < len(diaries_test):
                            print(f"{diaries_test[index_d].entry}")
                        else:
                            error_p = True
                            break
                        i += 2
                    elif option == "-all":
                        print(current_notebook.username)
                        print(current_notebook.password)
                        print(current_notebook.bio)
                        for i, diary in enumerate(current_notebook.get_diaries()):
                            print(f"{diary.entry}")
                        i += 1
                    else:
                        error_p = True
                        break
                if error_p:
                    print("ERROR")
            else:
                print("ERROR")
                continue
        except Exception as e:
            print("ERROR")  
            traceback.print_exc()  

if __name__ == "__main__":
    """Runs the main command look for the Diary program.
       Takes user inputs and sorts through commands."""
    main()