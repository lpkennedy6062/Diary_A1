# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Liam Kennedy
# lpkenned@uci.edu
# 81845142

from command_parser import parse_command
from notebook import Notebook, Diary
from pathlib import Path

def main():
    current_notebook = None
    current_path = None
    while True:
        try:
            user_input = input()
            command = parse_command(user_input)
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
                    if option == "-usr":
                        if i + 1 >= len(args):
                            edit_error = True
                        new_username = args[i + 1]
                        current_notebook.username = new_username
                        i += 2
                    elif option == "-pwd":
                        if i + 1 >= len(args):
                            edit_error = True
                        new_password = args[i + 1]
                        current_notebook.password = new_password
                        i += 2
                    elif option == "-bio":
                        if i + 1 >= len(args):
                            edit_error = True
                        new_bio = args[i + 1]
                        current_notebook.bio = new_bio
                        i += 2
                    elif option == "-add":
                        if i + 1 >= len(args):
                            edit_error = True 
                        new_add = args[i + 1]
                        current_notebook.add_diary(Diary(new_add))
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
                    else:
                        edit_error = True
                if edit_error:
                    print("ERROR")
                    break
                try:
                    current_notebook.save(current_path)
                except Exception:
                    print("ERROR")
                    continue

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
                tested = False
                p_error = False
                if current_notebook is None:
                        print("ERROR")
                        continue
                for i, option in enumerate(args):
                    if "-usr" in args:
                        print(current_notebook.username)
                        tested = True
                    if "-pwd" in args:
                        print(current_notebook.password)
                        tested = True
                    if "-bio" in args:
                        print(current_notebook.bio)
                        tested = True
                    if "-diaries" in args:
                        diaries_t = current_notebook.get_diaries()
                        for i, diary in enumerate(diaries_t):
                            print(f"{i}: {diary.entry}") 
                        tested = True

                    if "-diary" in args:
                        i = args.index("-diary")
                        if i + 1 >= len(args):
                            print("ERROR1")
                            p_error = True
                            break
                        try:
                            index_d = int(args[i + 1])
                        except Exception:
                            print("ERROR2")
                            p_error = True
                            break
                        diaries = current_notebook.get_diaries()
                        if 0 <= index_d < len(diaries):
                            print(f"{diaries[index_d].entry}")
                            tested = True
                        else:
                            print("ERROR3")
                            p_error = True
                            break
                    if "-all" in args:
                        print(current_notebook.username)
                        print(current_notebook.password)
                        print(current_notebook.bio)
                        for i, diary in enumerate(current_notebook.get_diaries()):
                            print(f"{diary.entry}")
                        tested = True
                    if not tested:
                        print("ERROR4")
            
                
        except Exception as e:
            print("ERRORR")         
        
if __name__ == "__main__":
    main()