import random

#Create Class
class PasswordGenerator():
    def __init__(self):
        #Letters list
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 
                        'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                        'V', 'W', 'X', 'Y', 'Z']

        #Numbers list
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        #Symbols list
        self.symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    #Generate Password
    def generate_password(self):

        nr_letters=random.randint(8, 10) #Numbers of letters in password
        nr_symbols=random.randint(2, 4) #Numbers of symbols in password
        nr_numbers=random.randint(2, 4) #Numbers of numbers in password

        password_letters = [random.choice(self.letters) for _ in range(nr_letters)] #Select random letters from letters list
        password_symbols = [random.choice(self.symbols) for _ in range(nr_symbols)] #Select random symbols from symbols list
        password_numbers = [random.choice(self.numbers) for _ in range(nr_numbers)] #Select random numbers from numbers list

        password_list = password_letters + password_symbols + password_numbers #Add selected data in Password list
        random.shuffle(password_list) #Shuffle password list

        password = "".join(password_list) #Add password list in password string

        return password 

