import sys
import zipfile


class Emulator:
    wd = ""


    def __init__(self, path):
        self.wd = ''
        self.img = path


    def execute(self, zipfile):
       sys_files = zipfile.namelist()

       run = True
       while run:
           if(len(self.wd)>1):
                print(f'[root@localhost {self.wd[:-1]}] ', end='')
           else:
               print(f'[root@localhost /] ', end='')
           command = input()
           command = command.split(' ')  # разделяем на команду, аргументы

           if (command[0] == "pwd"):
               print(f'/{self.wd}')

           elif command[0] == "ls":
                path = self.wd
                incorrect_args = []
                if(len(command)>1):
                    path = f'{command[1]}/'
                    if(path[0] == '/'):
                        path=path[1:]
                    if (not path in sys_files) and path != '/':
                        for i in range(1, len(command)):
                            if command[i]!='':
                                incorrect_args.append(command[i])
                if path == '/':
                    path = ''
                if len(incorrect_args)==0:  # all is correct
                    files = set()
                    for file in sys_files:
                        if file.startswith(path):
                            file = file[len(path):]
                            files.add(file.split('/')[0])
                    files = sorted(files)
                    for file in files:
                        if file != '':
                            print(file)
                else:
                    for arg in incorrect_args:
                        print("ls: " + arg + ": No such file or directory")

           elif command[0] == "cd":
                path= ' '.join(command[1:])
                print(path)
                if path == '.':
                    continue
                elif path == '/':
                    self.wd = ''
                elif path == '..':
                    if path != '':
                        temp = self.wd.split('/')
                        temp = temp[:-2] # обрезаем текущую папку
                        temp = '/'.join(temp) # объединяем назад
                        if temp == '/' or temp == '':
                            temp == ''
                        else:
                            temp = temp + '/'
                        self.wd = temp
                elif len(command)>1:
                    if path[0] == '/':
                        temp = f'{path[1:]}/'
                    else:
                        temp = temp = f'{self.wd}{path}/'
                        print(temp)
                        print(temp[:-1])
                    if temp in sys_files:
                        self.wd = temp
                    elif temp[:-1] in sys_files:
                        print(f'sh: cd: can\'t cd to {path}: Not a directory')
                    else:
                        print(f'sh: cd: can\'t cd to {path}: No such file or directory')

           elif command[0] == "cat":
               print(sys_files)
               if len(command)>1:
                   print(self.wd + command[1])
                   path = command[1]
                   if path[0]=='/':
                        path = path[1:]
                   if path in sys_files:
                       with zipfile.open(path, 'r') as file:
                           for line in file.readlines():
                               print(line)
                   elif (self.wd + path) in sys_files:
                       with zipfile.open((self.wd + path), 'r') as file:
                           for line in file.readlines():
                               print(line)
                   elif (self.wd + path + "/") in sys_files or (path + "/") in sys_files:
                        print(f'cat: {path}: Is a directory')
                   else:
                       print(f"cat: {path}: No such file or directory")
           elif command[0] == "exit":
                return
           else:
               print(f'sh: {command[0]}: command not found')


    def run_emulation(self):
        try:
            with zipfile.ZipFile(self.img) as system:
                self.execute(system)
        except Exception as ex:
            print(ex)




if __name__ == '__main__':
    if len (sys.argv)<=1:
        print("No arguments")
    else:
        em = Emulator (sys.argv[1]);
        em.run_emulation();

