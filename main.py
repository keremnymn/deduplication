def deduplicate(git_log, json_file):
    with open(git_log, 'r') as f:
        git_log = f.read()
    if not os.path.isfile(json_file):
        json_file = os.path.join(os.path.dirname(__file__), 'deduplicated.json')
        with open(json_file, 'w') as f:
            pass
        user_list = []
        max_id = 0
    else:
        with open(json_file, 'r') as f:
            user_list = json.loads(f.read())
            user_list = sorted(user_list, key = lambda x: x['id'])
            max_id = max(user_list, key=lambda x: x['id'])
            max_id = max_id['id']

    users = re.findall("Author: ([\\s\\S]+?)\n", git_log)
    for user in users:
        username, email = list(filter(len, re.split(' [<>]', user)))
        email = email[:-1]
        _unique = True
        if user_list != []:
            for existing_user in user_list:
                if email == existing_user['primary_email'] or (username in existing_user['author_names'] or email in existing_user['author_emails']):
                    _unique = False
                    author_names = existing_user['author_names']
                    if username not in author_names:
                        author_names.append(username)
                    author_emails = existing_user['author_emails']
                    if email not in author_emails:
                        author_emails.append(email)
                    new_info = {
                        'id': existing_user['id'],
                        'author_names': author_names,
                        'author_emails': author_emails,
                        'primary_email': existing_user['primary_email']
                    }
                    user_list.remove(existing_user)
                    user_list.append(new_info)
                    break
                else:
                    _unique = True
        if _unique:
            author_names = [username]
            author_emails = [email]
            new_user = {
                'id': 0 if user_list == [] else max(user_list, key=lambda x: x['id'])['id'] + 1, 
                'primary_email': email, 
                'author_emails': author_emails,
                'author_names': author_names
            }
            user_list.append(new_user)
        max_id += 1
    with open(json_file, 'w') as f:
        f.write(json.dumps(sorted(user_list, key = lambda x: x['id'])))

if __name__ == "__main__":
    import re, os, ast, sys, json
    print(sys.argv)
    if len(sys.argv) != 3:
        raise ValueError('You need to give a Git Log history, and a full JSON file path respectively.')
    else:
        deduplicate(sys.argv[1], sys.argv[2])