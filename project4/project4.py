#parses text file, returns a dict of lists-- one for each distinct email
#each list contains all unique words in that email
import re
import string
import math

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

#takes ham and spam emails, returns probabilities
def train(spam_emails, ham_emails):
    num_of_spam = len(spam_emails)
    num_of_ham = len(ham_emails)
    print("# of spam: " + str(num_of_spam))
    print("# of ham: " + str(num_of_ham))

    probability_spam = num_of_spam / (num_of_ham + num_of_spam)
    probability_ham = 1 - probability_spam

    #count instances of words in spam, store in dict
    spam_word_count = {}
    for email in spam_emails:
        for word in spam_emails[email]:
            if word not in spam_word_count.keys():
                spam_word_count[word] = 1
            else:
                spam_word_count[word] += 1
    #count instances of words in ham, store in dict
    ham_word_count = {}
    for email in ham_emails:
        for word in ham_emails[email]:
            if word not in ham_word_count.keys():
                ham_word_count[word] = 1
            else:
                ham_word_count[word] += 1
    
    prob_given_spam = {}
    prob_given_ham = {}

    #set of ALL unique words
    word_set = set(list(spam_word_count.keys()) + list(ham_word_count.keys()))
    print("Word count: " + str(len(word_set)))

    for word in word_set:
        #spam prob
        if word in spam_word_count:
            prob_given_spam[word] = (spam_word_count[word] + 1) / (num_of_spam + 2)
        else:
            prob_given_spam[word] = 1 / (num_of_spam + 2)
        
        #ham prob
        if word in ham_word_count:
            prob_given_ham[word] = (ham_word_count[word] + 1) / (num_of_ham + 2)
        else:
            prob_given_ham[word] = 1 / (num_of_ham + 2)
    
    output = {
        "word_set": word_set,
        "prob_spam": probability_spam,
        "prob_ham": probability_ham,
        "prob_given_spam": prob_given_spam,
        "prob_given_ham": prob_given_ham
    }
    
    return output

#goes through a list of email
#params: dictionary from train function, email_set dictionary, string "spam" or "ham" 
#of correct classification
def test_email_set(training_data, email_set, spam_or_ham):
    vocab_size = len(training_data["word_set"])
    prob_given_spam = training_data["prob_given_spam"]
    prob_given_ham = training_data["prob_given_ham"]

    size_of_email_set = len(email_set)
    correct_predictions = 0

    #loop through emails in email set
    for email in email_set:
        spam_log_prob = 0
        ham_log_prob = 0
        #variable to keep track of number of words from
        #vocab that are true in this email
        true_words = 0
        for word in training_data["word_set"]:
            if word in email_set[email]:
                spam_log_prob += math.log(prob_given_spam[word])
                ham_log_prob += math.log(prob_given_ham[word])
                true_words += 1
            else:
                #"negative" features - absence of a word
                spam_log_prob += math.log(1 - prob_given_spam[word])
                ham_log_prob += math.log(1 - prob_given_ham[word])
        #round log prob to 3 decimals
        #spam_log_prob = round(spam_log_prob, 3)
        #ham_log_prob = round(ham_log_prob, 3)
        #make prediction based on highest log-probability
        if spam_log_prob > ham_log_prob:
            h_map = "spam"
        else:
            h_map = "ham"

        #see if prediction is right or wrong
        if h_map == spam_or_ham:
            correct_predictions += 1
            right_or_wrong = "right"
        else:
            right_or_wrong = "wrong"

        
        output_str = ("TEST " + str(email) + " " + str(true_words) + "/" + str(vocab_size)
                     + " features true " + str(spam_log_prob) + " " + str(ham_log_prob)
                     + " " + h_map + " " + right_or_wrong)
        print(output_str)

    

def main():
    spam_training_emails = parse_text_file('train-spam.txt')
    ham_training_emails = parse_text_file('train-ham.txt')
    
    training_data = train(spam_training_emails, ham_training_emails)

    spam_test_emails = parse_text_file('test-spam.txt')
    
    test_email_set(training_data, spam_test_emails, "spam")




if __name__ == '__main__':
    main()