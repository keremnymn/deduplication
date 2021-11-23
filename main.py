def get_list(json_file):
    # if given json_file is not a file, create a default one. if it exists, open and load it to python.
    if not os.path.isfile(json_file):
        json_file = os.path.join(os.path.dirname(__file__), 'deduplicated.json')
        with open(json_file, 'w') as f: pass;
        user_list = []
    else:
        with open(json_file, 'r') as f:
            user_list = json.loads(f.read())
            user_list = sorted(user_list, key = lambda x: x['id'])
    return user_list

def check_existing_situation(username, email, existing_user):
    author_names = existing_user['author_names']
    if username not in author_names:
        author_names.append(username)
    author_emails = existing_user['author_emails']
    if email not in author_emails:
        author_emails.append(email)
    return author_names, author_emails

def deduplicate(git_log, json_file):
    # read the log file
    with open(git_log, 'r') as f:
        git_log = f.read()
    
    user_list = get_list(json_file)

    # I prefer using regex to parse git log
    users = re.findall("Author: ([\\s\\S]+?)\n", git_log)

    # after converting the log to a list, let's check those entries.
    for user in users:
        # I use filter here to get rid of empty list items
        username, email = [x.strip().replace('>', '') for x in list(filter(len, re.split(' [<>]', user)))]
        _unique = True
        if user_list != []: # if json_file is a real file and it's not empty
            for existing_user in user_list: # check the existing users
                aliases = [x.split('@')[0] for x in existing_user['author_emails']]
                if email == existing_user['primary_email'] or email.split('@')[0] in aliases or username in existing_user['author_names'] or email in existing_user['author_emails']:
                    _unique = False
                    author_names, author_emails = check_existing_situation(username, email, existing_user)
                    
                    new_info = {
                        'id': existing_user['id'],
                        'author_names': author_names,
                        'author_emails': author_emails,
                        'primary_email': existing_user['primary_email']
                    }

                    #update the existing info
                    user_list.remove(existing_user)
                    user_list.append(new_info)
                    break
                else:
                    _unique = True
        if _unique: # if our user doesn't exist in the json file
            author_names = [username]
            author_emails = [email]
            new_user = {
                'id': 0 if user_list == [] else max(user_list, key=lambda x: x['id'])['id'] + 1, 
                'primary_email': email, 
                'author_emails': author_emails,
                'author_names': author_names
            }
            user_list.append(new_user)
    with open(json_file, 'w') as f:
        f.write(json.dumps(sorted(user_list, key = lambda x: x['id'])))

if __name__ == "__main__":
    # import necessary packages
    import re, os, sys, json
    
    # we need at exactly two arguments
    if len(sys.argv) != 3:
        raise ValueError('You need to give a Git Log history, and a full JSON file path respectively.')
    else:
        deduplicate(sys.argv[1], sys.argv[2])