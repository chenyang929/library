
def user_add():
    with open('user/email', encoding='utf-8') as f:
        email_list = [email.strip() for email in f.readlines()]
    with open('user/name', encoding='utf-8') as f1:
        name_list = [username.strip() for username in f1.readlines()]
    zipped = zip(email_list, name_list)
    return zipped


if __name__ == "__main__":
    print(list(user_add()))
