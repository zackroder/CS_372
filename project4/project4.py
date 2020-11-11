#parses text file, returns a dict of lists-- one for each distinct email
#each list contains all unique words in that email
import re
import string

def parse_text_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    
    email_count = 0

    #dictionary of emails
    emails = {}

    for line in lines:
        if line.strip() == '<SUBJECT>':
            if email_count != 0:
                emails[email_count] = set(emails[email_count])    
            email_count += 1
            emails[email_count] = []
        if line.strip() not in ('<SUBJECT>', '</SUBJECT>', '<BODY>', '</BODY>'):
            words = re.sub('['+string.punctuation+']', '', line).lower().split()
            if len(words) > 0:
                emails[email_count] += words

    emails[email_count] = set(emails[email_count])

    return emails

#takes dictionary outputted from parse_text_file and creates probabilities
#returns dict of probabilities for every word
#TODO acutally needs to take dictionaries for both spam and ham training data
def train()

def main():
    emails = parse_text_file('train-spam-small.txt')
    print(emails)


if __name__ == '__main__':
    main()