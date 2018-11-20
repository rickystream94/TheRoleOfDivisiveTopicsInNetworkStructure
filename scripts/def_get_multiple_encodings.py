def iterchunks(stuff, chunksize=100):
    i = 0
    while i < len(stuff):
        yield stuff[i: i+chunksize]
        i += chunksize

def get_multiple_usernames(usernames):
    # Proceed in batches
    username_to_id_dict = {}
    for chunk in iterchunks(usernames):
        # Build regex
        arg = "|".join(("^" + username + "," for username in chunk))

        #Invoke shell script that finds the occurrences
        p = subprocess.Popen(['../scripts/get_encodings.sh', arg], stdout=subprocess.PIPE)
        output = p.communicate()[0]
        
        # Add entries to dict
        for line in output.split('\n'):
            if line != "":
                username = line.split(',')[0]
                encoding = line.split(',')[1]
                username_to_id_dict[username] = encoding
    return username_to_id_dict