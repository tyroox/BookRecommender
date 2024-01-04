"""
Barış Atakan Aktaş
Elif Şanlıtürk
"""

import random
import stdarray
import stdio

file1 = open('books.txt', 'r') 
Lines1 = file1.readlines() 

file2 = open('ratings.txt', 'r+') 
Lines2 = file2.readlines()


linenumber1 = len(Lines1)       #number of books
linenumber2 = len(Lines2) 
books = []
customers = stdarray.create2D(linenumber2//2, 2)


for line in Lines1:             #database for books
    books.append(line)

a = 0
for i in range(linenumber2//2): #database for users and ratings
    for j in range(2):
        customers[i][j] = Lines2[a].split()
        a += 1

stdio.write("What is your name? ")
user_name = input()

def new_user(name, db=customers): 
    ratings = []
    for i in range(linenumber1):
        ratings.append(0)       #set all ratings to 0
    newuser = [[name], ratings] 
    db += [newuser]             #adding new user's name and ratings to list as one item
    file2.write(name)           #writing new user's name to txt file
    file2.write("\n")

user_names = []
user_names.append(user_name.split())
for i in range(linenumber2//2): 
    if customers[i][0] == user_names[0]:    
        print("Welcome back " + user_name + "!!!")  #a message for old user
stdio.writeln("Before I can recommend some new books for you to read, you need to tell me your opinion on a few books. \n")
stdio.writeln("If you haven’t read the book, answer 0 but otherwise use this scale")
stdio.writeln(" -5  Hated it! \n -3  Didn’t like it. \n  1  OK \n  3  Liked it. \n  5  Really liked it. \n")

"""
first book
vote

second book
vote
.
.
.
thirteenth book
vote

change the ratings of listed books to the new user's given votes
0 ---> 5
0 ---> -3
0 ---> 0

write new user's all votes to txt
0 5 -3 -5 1 0 3 5 5 0 0 3 ...
"""
def book_rating_new_user(db=customers):
    rand_books = random.sample(Lines1, k=13)  #generates 13 random books for new user to rate

    for a_book in rand_books:
        stdio.write(a_book)
        line_no = Lines1.index(a_book)
        b = input()
        if b=="-5" or b=="-3" or b=="0" or b=="1" or b=="3" or b=="5":
            db[(linenumber2)//2][1][line_no] = int(b)
        else:
            print("Your vote is not valid.")
    for i in range(linenumber1):
        file2.write(str(db[(linenumber2)//2][1][i]) + " ")

    file2.write("\n")

"""
first book
vote

second book
vote
.
.
.
thirteenth book
vote

update the ratings of listed books to the old user's given votes
3 ---> 5
0 ---> -3
0 ---> 0

add updated ratings to an empty list

write updated votes of old user's to txt
0 5 -3 -5 1 0 3 5 5 0 0 3 ...
"""
def book_rating_old_user(user_number, db=customers):
    rand_books = random.sample(Lines1, k=13) #generates 13 random books for old user to rate

    for a_book in rand_books:
        stdio.write(a_book)
        line_no = Lines1.index(a_book)
        b = input()
        if b=="-5" or b=="-3" or b=="0" or b=="1" or b=="3" or b=="5":
            db[user_number][1][line_no] = int(b)
        else:
            print("Your vote is not valid.")

    a = []       
    for x in range(linenumber1):        
        a.extend([str(db[user_number][1][x])])
                

    Lines2[(((int(user_number)+1) * 2)-1)] = a[0]
    for z in range(1,linenumber1):
        Lines2[(((int(user_number)+1) * 2)-1)] += " " + a[z]

    Lines2[(((int(user_number)+1) * 2)-1)] += " \n"  
           
    file3 = open('ratings.txt', 'w') 
    file3.writelines(Lines2)
    
            
for i in range(linenumber2//2):             #number of users
    if customers[i][0] == user_names[0]:    #checking if the user exists in database
        book_rating_old_user(i)
        break
    elif i != ((linenumber2//2)-1):
        continue
    else:
        new_user(user_name)
        book_rating_new_user()
        linenumber2 += 2
        
stdio.writeln("I can make recommendations based on 3 different algorithms \nWhich algorithm? A, B or C")
alg_by_user = input()

while not (alg_by_user == "A" or alg_by_user == "B" or alg_by_user == "C" or alg_by_user == "a" or alg_by_user == "b" or alg_by_user == "c"):
    stdio.writeln("\nYou didn't choose any Algorithm, try again.")
    alg_by_user = input()
stdio.writeln("\nRecommending based on Algorithm " + alg_by_user.capitalize())
print("+++++++++++++++++++++++++++++++++++")

def take_first(list):
    return list[0]

def take_second(list):
    return list[1]

"""
What is your name? Ben

Ben ---> first user
which_user() ---> 0
***
What is your name? Atakan

Atakan ---> new user (87th)
which_user() ---> 86
"""
def which_user():
    user_names = []
    user_names.append(user_name.split())
    for i in range(linenumber2//2):
        if customers[i][0] == user_names[0]:
            return i
            break

"""
recommends 10 books to the user that user hasn't read based on top rated books in our database
"""
def Approach_A(db=customers):
    number_of_user = which_user()
    average_rat = []
    for i in range(linenumber1):
        sum1 = 0
        user = 0
        for j in range(linenumber2//2):
            if number_of_user != j:
                if int(db[j][1][i]) == 0:
                    continue
                else:
                    user += 1
                    sum1 += int(db[j][1][i])                
                    average = sum1 / user
        average_rat.append(average)
        
    ratings = []
    for number, rating in enumerate(average_rat):
        a = [number, rating]
        ratings.append(a)

    sorted_ratings = (sorted(ratings, key=take_second, reverse = True))

    recommendedbooks = 0
    for i in range(len(sorted_ratings)):
        book_no = int(sorted_ratings[i][0])
        if int(db[number_of_user][1][book_no]) == 0:
            stdio.write(books[book_no])
            recommendedbooks += 1
        if recommendedbooks == 10:
            break
        
"""
calculate similarity of each user with logged in user
calculate a prediction for each book using similarities and ratings
recommend top 10 books that logged in user hasn't read
"""
def Approach_C(db=customers):
    number_of_user = which_user()
    numbers = []
    for i in range(linenumber2//2):
        c = 0
        if number_of_user != i:
            for j in range(linenumber1):
                product = int(db[i][1][j]) * int(db[number_of_user][1][j])
                c += product
            numbers.append(c)
    prediction_of_books = []
    for k in range(linenumber1):
        predictionsum = 0
        for m in range(linenumber2//2):
            if number_of_user != m:
               prediction = int(numbers[k]) * int(db[m][1][k])
               predictionsum += prediction
        prediction_of_books.append(predictionsum)
    books_w_numbers = []
    for number, values in enumerate(prediction_of_books):
        a = [number, values]
        books_w_numbers.append(a)

    sorted_books_w_numbers = (sorted(books_w_numbers, key=take_second, reverse = True))
    recommendedbooks = 0
    for i in range(len(sorted_books_w_numbers)):
        book_no = int(sorted_books_w_numbers[i][0])
        if int(db[number_of_user][1][book_no]) == 0:
            stdio.write(books[book_no])
            recommendedbooks += 1
        if recommendedbooks == 10:
            break
        
"""
matches user with another user based on their given ratings
recommends 10 books to the user that user hasn't read based on matched user
if the system can't make enough recommendations because the user has already read matched user's favorite books

Dan Brown,The Da Vinci Code
Meg Cabot,The Princess Diaries
Orson Scott Card,Ender's Game

I can recommend you 3 books based on your most similar user.

suggests other algorithms to user or finish the recommendation
"""
def Approach_B(db=customers):
    number_of_user = which_user()
    numbers = []
    for i in range(linenumber2//2):
        c = 0
        if number_of_user != i: 
            for j in range(linenumber1):
                product = int(db[i][1][j]) * int(db[number_of_user][1][j])
                c += product
            numbers.append(c)

    newlist = []
    for number, values in enumerate(numbers):
        a = [number, values]
        newlist.append(a)
    
    sorted_newlist = sorted(newlist, key=take_second, reverse = True)
    matcheduser = sorted_newlist[0][0]
    
    newlist2 = []
    for i in range(linenumber1):
        newlist1 = [int(customers[matcheduser][1][i])],[books[i]]
        if db[number_of_user][1][i] == 0:
            newlist2.append(newlist1)

    sorted_newlist2 = (sorted(newlist2, key=take_first, reverse = True))
    recommended_books = 0
    for i in range(len(sorted_newlist2)):
        stdio.write(sorted_newlist2[i][1][0])
        recommended_books += 1
        if i == 10:
            break
    if recommended_books < 10:
        print("I can recommend you " + str(recommended_books) +" books based on your most similar user.")
        print("Would you like to see recommendations based on other algorithms?\nType yes or no")
        answer = input()
        if answer == "yes":
            print("\nWhich algorithm would you like to use?\nType A or C")
            answer2 = input()
            if answer2 == "a" or "A" :
                Approach_A()
            elif answer2 == "c" or "C":
                Approach_C()
        elif answer == "no":
            print("\nThanks for choosing our system!!!")

if alg_by_user == "A" or alg_by_user == "a":
    Approach_A()

if alg_by_user == "B" or alg_by_user == "b":
    Approach_B()

if alg_by_user == "C" or alg_by_user == "c":
    Approach_C()










