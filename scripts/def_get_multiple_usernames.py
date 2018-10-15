def get_multiple_usernames(ids):
    # Convert ID to line number by adding 1
    arg = ";".join([str(el + 1) + "p" for el in ids])

    #Invoke shell script that finds the occurrences
    p = subprocess.Popen(['../scripts/get_usernames.sh', arg], stdout=subprocess.PIPE)
    output = p.communicate()[0]

    id_to_username_dict = {line.split(',')[1]:line.split(',')[0] for line in output.split('\n') if line != ""}
    return id_to_username_dict