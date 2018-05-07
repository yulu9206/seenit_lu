import os
import sqlite3 as sql
import user, db, seenit, post, comment
import postUpvote as pu
import postDownvote as pd
import commentUpvote as cu
import commentDownvote as cd
import getpass
import logging
logging.basicConfig(filename='seenit.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

new_u_id = new_s_id = new_p_id = new_c_id = 5
new_pu_id = 8
new_pd_id = new_cu_id = new_cd_id = 1
this_u_id = 0
admin = False

# run this when database is not created yet
def build_database():
    logging.info("Build database\n")
    db.create_tables()
    db.insert_users()
    db.insert_seenits()
    db.insert_posts()
    db.insert_comments()
    db.insert_post_upvote()
    db.show_seenits()
    db.show_posts()
    db.show_comments()
    db.show_post_upvotes()
        
def register():
    global new_u_id, this_u_id, admin
    logging.info("Register request user response\n")
    print("1 - Register")
    x = input("user name: ")
    z = getpass.getpass('Password:')
    y = input("email: ")
    w = input("Are you an administrator? (y/n)")
    logging.info("Response: ")
    logging.info("user name: ")
    logging.info(x)
    logging.info(" password: ")
    logging.info(z)
    logging.info(" email: ")
    logging.info(y)
    logging.info("Are you administrator? ")
    logging.info(w)
    logging.info("\n")
    user.insert(new_u_id, x, z, y)
    this_u_id = new_u_id
    # print ("this u id is ", this_u_id)
    new_u_id += 1
    if w == 'y':
        admin = True
    main_menu()  

def login():
    global this_u_id, admin
    logging.info("Print login menu - Request user response\n")
    print("-" * 40)
    print ("               Login Menu")
    print("-" * 40)
    login = input('''
1 = Register
2 = Already A Member
3 = Main Menu
4 = Exit
    ''')
    print("-" * 40)
    # print("\n")
    if login == '1':
        logging.info("Response: 1 - Register\n")
        register()
    elif login == '2':
        logging.info("Response: 2 - Already A Member\n")
        logging.info("Print login menu - Request user response\n")
        print("2 - Login")
        x = input("user name:")
        y = getpass.getpass('Password:')
        w = input("Are you an administrator? (y/n)")
        this_u_id = user.login(x, y)
        logging.info("user name: ")
        logging.info(x)
        logging.info(" password: ")
        logging.info(y)
        logging.info(" Are you an administrator? ")
        logging.info(w)
        logging.info("\n")
        if w == 'y':
            admin = True
        main_menu()
    elif login == '3':
        logging.info("Response: 3 - main menu\n")
        main_menu()
    else:
        logging.info("Response: 4 - Exit\n")
        exit()  

def insert_vote(table, vote, id):
    global new_pu_id, new_pd_id, new_cu_id, new_cd_id
    if table == 'post':
        if vote == 'up':
            pu.insert(new_pu_id, id, this_u_id)
            new_pu_id += 1
        else:
            pd.insert(new_pd_id, id, this_u_id)
            new_pd_id += 1
        show_votes('post', id)
    else:
        if vote == 'up':
            cu.insert(new_cu_id, id, this_u_id)
            new_cu_id += 1
        else:
            cd.insert(new_cd_id, id, this_u_id)
            new_cd_id += 1
        show_comment(id)        

def delete_vote(table, vote, id):
    logging.info("delete_vote request user response: Please input id of the one you want to delete\n")
    v_id = input("Please input id of the one you want to delete:")
    logging.info("Response: ")
    logging.info(v_id)
    logging.info("\n")
    if table == 'post':
        if vote == 'up':
            pu.delete(v_id)
        else:
            pd.delete(v_id)
        show_votes('post', id)
    else:
        if vote == 'up':
            cu.delete(v_id)
        else:
            cd.delete(v_id)
        show_comment(id)

def show_votes(table, id):
    if table == 'comment':
        up = cu.read_all(id)
    else:
        up = pu.read_all(id)
    print ("Upvotes:")
    print (up)
    if table == 'comment':
        down = cd.read_all(id)
    else:
        down = pd.read_all(id)
    print ("Downvotes:")
    print (down)
    print("-" * 40)
    print ("                Vote Menu")
    print("-" * 40)
    logging.info("Print show_votes menu - Request user's response\n")
    if admin == True:
        method = input('''   
            1 = Up
            2 = Down
            3 = Delete Up
            4 = Delete Down
            5 = Main Menu
            6 = Exit
            ''')
    else:
        method = input('''   
            1 = Up
            2 = Down
            5 = Main Menu
            6 = Exit
            ''')
    if method == '1':
        logging.info("Response: 1 - Up\n")
        insert_vote(table, 'up', id)
    elif method == '2':
        logging.info("Response: 2 - Down\n")
        insert_vote(table, 'down', id)
    elif method == '3':
        logging.info("Response: 3 - Delete Up\n")
        delete_vote(table, 'up', id)
    elif method == '4':
        logging.info("Response: 4 - Delete Down\n")
        delete_vote(table, 'down', id)
    elif method == '6':
        logging.info("Response: 6 - Exit")
        exit()
    else:
        logging.info("Response: 5 - Main Menu")
        main_menu()

def insert_comment(p_id):
    global new_c_id
    logging.info("insert_comment request user response - Please input your comment\n")
    content = input("Please input your comment:")
    logging.info("Response: ")
    logging.info(content)
    logging.info("\n")
    comment.insert(new_c_id,content,p_id,this_u_id)
    new_c_id += 1
    show_comments(p_id)  

def show_comment(c_id):
    _comment= comment.read_one(c_id)
    print (_comment)
    show_votes('comment', c_id)

def delete_comment(p_id):
    logging.info("delete_comment request user response - Please input id of the one you choose\n")
    c_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(c_id)
    logging.info("\n")
    comment.delete(c_id)
    show_comments(p_id)

def update_comment(p_id):
    logging.info("update_comment request user response - Please input the id of the one you choose\n")
    c_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(c_id)
    logging.info("\n")
    logging.info("update_comment request user response - Please input your comment\n")
    content = input("Please input your comment:")
    logging.info("Response: ")
    logging.info(content)
    logging.info("\n")
    comment.update(c_id,content)
    show_comments(p_id)

def show_comments(p_id):
    print ("Comments:")
    comment.read_all(p_id)
    # print (comments)
    print("-" * 40)
    print ("                Comment Menu")
    print("-" * 40)
    logging.info("Print show_comments menu - Request user response\n")
    if admin == True:
        method = input('''   
            1 = Create One
            2 = Choose One
            3 = Delete One
            4 = Update One
            5 = Main Menu
            6 = Exit
            ''')
    else:
        method = input('''   
            1 = Create One
            2 = Choose One
            5 = Main Menu
            6 = Exit
            ''')        
    if method == '1':
        logging.info("Response: 1 - Create One\n")
        insert_comment(p_id)
    elif method == '2':
        logging.info("Response: 2 - Choose One\n")
        c_id = input("Please input id of the one you choose:")
        show_comment(c_id)
    elif method == '3':
        logging.info("Response: 3 - Delete One\n")
        delete_comment(p_id)
    elif method == '4':
        logging.info("Response: 4 - Update One\n")
        update_comment(p_id);
    elif method == '6':
        logging.info("Response: 6 - Exit\n")
        exit()
    else:
        logging.info("Response: 5 - Main Menu\n")
        main_menu()

def insert_post(s_id):
    global new_p_id
    logging.info("insert_post request user response - Please input your post\n")
    content = input("Please input your post:")
    logging.info("Response: ")
    logging.info(content)
    logging.info("\n")
    post.insert(new_p_id,content,s_id,this_u_id)
    new_p_id += 1
    show_posts(s_id)  

def show_post():
    logging.info("show_post request user response - Please input id of the one you choose\n")
    p_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(p_id)
    logging.info("\n")
    _post= post.read_one(p_id)
    print (_post)
    comment_and_vote_menu(p_id)
    
def comment_and_vote_menu(p_id):
    print("-" * 40)
    print("                Comment/Vote Menu")
    print("-" * 40)
    logging.info("Print comment_and_vote_menu menu - Request user response\n")
    method = input('''   
        1 = Show Comments
        2 = Show Votes
        3 = Main Menu
        4 = Exit
        ''')
    if method == '1':
        logging.info("Response: 1 - Show Comments\n")
        show_comments(p_id)
    elif method == '2':
        logging.info("Response: 2 - Show votes\n")
        show_votes('post', p_id)
    elif method == '4':
        logging.info("Response: 4 - Exit\n")
        exit()
    else:
        logging.info("Response: 3 - Main Menu\n")
        main_menu()  

def delete_post(s_id):
    p_id = input("Please input id of the one you choose:")
    post.delete(p_id)
    show_posts(s_id)

def update_post(s_id):
    logging.info("update_post request user response - Please input id of the one you choose\n")
    p_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(p_id)
    logging.info("\n")
    logging.info("update_post request usr response - Please input your post\n")
    content = input("Please input your post:")
    logging.info("Reponse: ")
    logging.info(content)
    logging.info("\n")
    post.update(p_id,content)
    show_posts(s_id)

def show_posts(s_id):
    print("Posts:")
    post.read_all(s_id)
    # print(posts)
    print("-" * 40)
    print("                Post Menu")
    print("-" * 40)
    logging.info("Print show_posts menu - Request user response\n")
    if admin == True:
        method = input('''   
            1 = Create One
            2 = Choose One
            3 = Delete One
            4 = Update One
            5 = Main Menu
            6 = Exit
            ''')
    else:
        method = input('''   
            1 = Create One
            2 = Choose One
            5 = Main Menu
            6 = Exit
            ''')
    if method == '1':
        logging.info("Response: 1 - Create One\n")
        insert_post(s_id)
    elif method == '2':
        logging.info("Response: 2 - Choose One\n")
        show_post()
    elif method == '3':
        logging.info("Response: 3 - Delete One\n")
        delete_post(s_id)
    elif method == '4':
        logging.info("Response: 4 - Update One\n")
        update_post(s_id);
    elif method == '6':
        logging.info("Response: 6 - Exit\n")
        exit()
    else:
        logging.info("Response: 5 - Main Menu\n")
        main_menu()

def insert_seenit():
    global new_s_id
    logging.info("insert_seenit request user response - Please describe your seenit\n")
    category = input("Please describe your seenit:")
    logging.info("Response: ")
    logging.info(category)
    logging.info("\n")
    seenit.insert(new_s_id, category, this_u_id)
    new_s_id += 1
    show_seenits()  

def show_seenit():
    logging.info("show_seenit request user reponse - Please input id of the one you choose\n")
    s_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(s_id)
    logging.info("\n")
    _seenit = seenit.read_one(s_id)
    print(_seenit)
    show_posts(s_id)

def delete_seenit():
    logging.info("delete_seenit request user reponse - Please input id of the one you choose\n")
    s_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(s_id)
    logging.info("\n")
    seenit.delete(s_id)
    show_seenits()

def update_seenit():
    logging.info("update_seenit request user response - Please input id of the one you choose\n")
    s_id = input("Please input id of the one you choose:")
    logging.info("Response: ")
    logging.info(s_id)
    logging.info("\n")
    logging.info("update_seenit request user response - Please decribe your seenit\n")
    category = input("Please describe your seenit:")
    logging.info("Response: ")
    logging.info(category)
    logging.info("\n")
    seenit.update(s_id, category)
    show_seenits()

def show_seenits():
    seenit.read_all()
    print("-" * 40)
    print("                Seenit Menu")
    print("-" * 40)
    logging.info("Print show_seenits menu - Request user reponse\n")
    if admin == True:
        method = input('''   
            1 = Create One
            2 = Choose One
            3 = Delete One
            4 = Update One
            5 = Main Menu
            6 = Exit
            ''')
    else:
        method = input('''   
            1 = Create One
            2 = Choose One
            5 = Main Menu
            6 = Exit
            ''')
    if method == '1':
        logging.info("Response: 1 - Create One\n")
        insert_seenit()
    elif method == '2':
        logging.info("Response: 2 - Choose One\n")
        show_seenit()
    elif method == '3':
        logging.info("Response: 3 - Delete One\n")
        delete_seenit()
    elif method == '4':
        logging.info("Response: 4 - Update One\n")
        update_seenit();
    elif method == '6':
        logging.info("Response: 6 - Exit\n")
        exit()
    else:
        logging.info("Response: 5 - Main Menu\n")
        main_menu()

def account_profile():
    global this_u_id
    user_info = user.read_one(this_u_id)
    print("Account Information:")
    print(user_info)
    print("-" * 40)
    print("                Account Menu")
    print("-" * 40)
    logging.info("Print account_profile menu - Request user response\n")
    if admin == True:
        method = input('''   
            1 = Update My Account Info
            2 = Delete My Account
            3 = Show All Accounts
            4 = Main Menu
            5 = Exit
            ''')
    else:
        method = input('''   
            1 = Update My Account Info
            2 = Delete My Account
            4 = Main Menu
            5 = Exit
            ''')
    if method == '1':
        logging.info("Response: 1 - Update Account Info\n")
        logging.info("Response 1 request user response\n")
        x = input("user name: ")
        z = getpass.getpass('Password:')
        y = input("email: ")
        logging.info("user name: ")
        logging.info(x)
        logging.info(" password: ")
        logging.info(z)
        logging.info(" email: ")
        logging.info(y)
        logging.info("\n")
        user.update(this_u_id, x, z, y)
        account_profile()
    elif method == '2':
        logging.info("Response: 2 - Delete My Account\n")
        user.delete(this_u_id)
        this_u_id = 0
        main_menu()
    elif method == '3':
        logging.info("Response: 3 - Show All Accounts\n")
        user.read_all()
        # print(all_users)
        account_profile()
    elif method == '5':
        logging.info("Response: 5 - Exit\n")
        exit()
    else:
        logging.info("Response: 4 - Main Menu\n")
        main_menu()

def logout():
    global this_u_id
    this_u_id = 0
    main_menu()

def print_main_menu():
    # MENU DESIGN!
    print (28 * "-", "MAIN MENU", 33 * "-")
    print ('|', 25 * " ", "0. Account Profile", 23 * " ", "|")
    print ('|', 25 * " ", "2. Show Seenits", 26 * " ", "|")
    print ('|', 25 * " ", "3. Logout", 32 * " ", "|")
    print ('|', 25 * " ", "4. Exit", 34 * " ", "|")
    print (72 * "-")

def print_Welcome_menu():
    # MENU DESIGN!
    print (30 * "~", "Welcome", 33 * "~")
    print ('|', 25 * " ", "User ID is", this_u_id, 29 * " ", "|")
    print ('|', 2 * " ", "0 means not logged in yet, other number means logged in already", 1 * " ", "|")
    print (72 * "~")

def print_login_menu():
    # MENU DESIGN!
    print (28 * "-", "MAIN MENU", 33 * "-")
    print ('|', 25 * " ", "1. Login", 33 * " ", "|")
    print ('|', 25 * " ", "4. exit", 34 * " ", "|")
    print (72 * "-")

def print_register_menu():
    # MENU DESIGN!
    print (27 * "-", "LOGIN MENU", 33 * "-")
    print ('|', 25 * " ", "1. Register", 30 * " ", "|")
    print ('|', 25 * " ", "2. Already A Member", 22 * " ", "|")
    print ('|', 25 * " ", "3. Main Menu", 29 * " ", "|")
    print ('|', 25 * " ", "4. Exit", 34 * " ", "|")
    print (72 * "-")

def main_menu():
    logging.info("Printing main menu - Request user response\n")
    print_Welcome_menu()
    if this_u_id:
        print_main_menu()
        method = input()
    else:
        print_login_menu()
        method = input()
    if method == '1':
        logging.info("Response: 1 - Login\n")
        login()
    elif method == '2':
        logging.info("Response: 2 - Show Seenits\n")
        show_seenits()
    elif method == '0':
        logging.info("Response: 0 - Account Profile\n")
        account_profile()
    elif method == '3':
        logging.info("Response: 3 - Logout\n")
        logout()
    else:
        logging.info("Response: 4 - Exit\n")
        exit()

# build_database()
main_menu()