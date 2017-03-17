#pick a random word from dictionary
#option to pick another random word
#find all subwords that can be made from that word
#collect users guesses
#compare against acceptable words
#point for every word, 3 points for every word made with the same length of the original words
#keep a record
import random
from itertools import permutations
import collections

def read_dictionary():
        words = open("words.txt").readlines()
        length = len(words)
        for i in range(length):
                words[i] = words[i].rstrip().lower()
                words[i] = words[i].split("'")[0]
        return words

def read_highscores():
        lines = open("highscores.txt").readlines()
        hs_dict = {}
        for line in lines:
                line = line.split(',')
                hs_dict[line[2].rstrip()] = [line[0], line[1]]

        hs_dict = collections.OrderedDict(sorted(hs_dict.items(), reverse = True))


        return hs_dict

def add_score(score, word):
        hs_dict = read_highscores()
        print("Here are the top 5 scores:")
        print("SCORE:\tNAME:\tWORD:")
        i = 0
        for k, v in hs_dict.items():
                if i < 5:
                        print("{}\t{}\t{}".format(k, v[0], v[1]))
                        i += 1

        q = True
        while(q):
                c = input("Would you like to add your score? [y/n]: ")
                if c.lower() == 'y':
                        name = input("Please input your initials: ")
                        f = open("highscores.txt", 'a')
                        f.write('\n{},{},{}'.format(name,word,score))
                        f.close()

                        print("Here are the updated top 5 scores:")
                        hs_dict = read_highscores()
                        i = 0
                        for k, v in hs_dict.items():
                                if i < 5:
                                        print("{}\t{}\t{}".format(k, v[0], v[1]))
                                        i += 1
                        q = False
                elif c.lower() == 'n':
                        q = False
                else:
                        print("Invalid input. Try again.")


 
def choose_word(words):
        choose = True
        while(choose):
                c = input("Would you like 1) a random word or 2) to enter your own? [1/2]: ")
                if c == '1':
                        word = random.choice(words)
                        choose = False
                elif c == '2':
                        word = input("Input your word: ")
                        choose = False
                else:
                        print("Invalid input. Try again.")
        return word


def find_subwords(word, dict):
        l = len(word)
        subwords = []
        for i in range(2,l):
                perms = [''.join(p) for p in permutations(word, i)]
                for perm in perms:
                        if perm in dict:
                                subwords.append(perm)
        return set(subwords)

def input_guesses(word):
        guess = True
        guesses = []
        while(guess):
                g = input("{} | Input word [or d for done]: ".format(word))
                if(g != 'd'):
                        guesses.append(g)
                else:
                        guess = False
        return guesses

def check_guesses(word, guesses, subwords):
        correct = []
        incorrect = []
        score = 0
        l = len(word)
        for g in guesses:
                if g in subwords:
                        correct.append(g)
                        subwords.remove(g)
                else:
                        incorrect.append(g)

        print("~~~~~~RESULTS~~~~~~")
        print("Your word was: {}".format(word))
        print("Congratulations! You got these words correct:")
        i = 0
        for c in correct:
                print(c, end = '\t')
                i += 1
                if (i%5 == 0):
                        print()
                if len(c) == l:
                        score += 3
                else:
                        score += 1
        print("\nSorry, these words were wrong:")
        i = 0
        for n in incorrect:
                print(n, end = '\t')
                i += 1
                if (i%5 == 0):
                        print()
        print("\nThese were the words you missed:")
        i = 1
        for s in subwords:
                print(s, end = '\t')
                i += 1
                if(i%5 == 0):
                        print()
        print("\nYour score was {}. Good job!".format(score))
        add_score(score, word)
        print("~~~~~~~~~~~~~~~~~~~~")



def main():
        words = read_dictionary()
        play = True
        word_choice = True
        while(play):
                print("Welcome to MomGame!")

                print("Here are the top 5 scores:")
                print("SCORE:\tNAME:\tWORD:")
                hs = read_highscores()
                i = 0
                for k, v in hs.items():
                        if i < 5:
                                print("{}\t{}\t{}".format(k, v[0], v[1]))
                                i += 1



                while(word_choice):
                        word = choose_word(words)
                        word = word.rstrip()
                        c = input("Would you like to play with {}? [y/n/q to quit]: ".format(word))
                        if(c.lower() == 'y'):
                                print("Generating subwords.")
                                print("This may take a few moments, start thinking!")
                                subwords = find_subwords(word, words)
                                guesses = input_guesses(word)
                                check_guesses(word, guesses, subwords)
                                #word_choice = False
                        elif (c.lower() == 'n'):
                                continue
                        elif(c.lower() in ['quit', 'q']):
                                word_choice = False
                                play = False
                                print("Goodbye :(")
                        else:
                                print("Invalid input. Try again.")

                play = False


if __name__ == '__main__':
        main()