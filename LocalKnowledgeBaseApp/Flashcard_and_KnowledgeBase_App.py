# use flashcard_app() or knowledge_base_app() to run the app locally
# flashcard data is saved to a shelve database in the cwd, knowledge base data is saved to a shelve database in the cwd
# concatenate with folder app, potentially into a single repo or single app
import shelve, random, pyinputplus as pyip
from dataclasses import dataclass
from collections import defaultdict
# FLASHCARD APP
@dataclass
class Card:
    question: str
    answer: str
    hint: str
    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}"

class Quiz:
    def __init__(self, db):        # name of the shelve db (allows for multiple quizzes)
        self.db = db

    def __str__(self):
        return f"Quiz: {self.db}"
    
    def add(self, card):
        with shelve.open(f"{self.db}") as db:
            db[card.question] = [card.answer, card.hint]
    
    def remove(self, card):
        with shelve.open(f"{self.db}") as db:
            del db[card.question]
    
    def list_questions(self):
        with shelve.open(f"{self.db}") as db:
            res = list(db.keys())
            for question in res:
                print(f"{question}\n")
    
    def quiz(self):
        with shelve.open(f"{self.db}") as db:
            questions = list(db.keys())
            random_question = random.choice(questions)
            return random_question, db[random_question][0]  

    def hint(self, question):
        with shelve.open(f"{self.db}") as db:
            return db[question][1]

def flashcard_app():
    count_correct = 0
    count_incorrect = 0
    hint_count = 0
    hint_limit = 3
    counter = defaultdict(lambda: [0, 0])

    first = input("Welcome to the quiz! What would you like to name your quiz?")
    quiz = Quiz(first)
    while True:
        choice = pyip.inputMenu(['add', 'remove', 'list', 'quiz', 'quit'])
        if choice == 'quit':
            print(f"You got {count_correct} correct and {count_incorrect} incorrect")
            prompt2 = pyip.inputMenu(['view_counter', 'quit'])
            if prompt2 == 'view_counter':
                for question, count in counter.items():
                    print(f"{question}: {count[0]} correct, {count[1]} incorrect")
            else:
                break
            break

        elif choice == 'add':
            question = pyip.inputStr("Enter the question: ")
            answer = pyip.inputStr("Enter the answer: ")
            hint = pyip.inputStr("Enter the hint: ")
            quiz.add(Card(question, answer, hint))  

        elif choice == 'remove':
            question = pyip.inputStr("Enter the question: ")
            if question not in quiz.list_questions():
                print("Question not found")
            quiz.remove(question)

        elif choice == 'list':
            quiz.list_questions()

        elif choice == 'quiz':
            print(f"You have {hint_limit - hint_count} hints left")
            random_question, correct_answer = quiz.quiz() 
            print(f"Question: {random_question}")
            answer = pyip.inputStr("Enter the answer: ")
            if answer.lower().strip() == correct_answer.lower().strip():
                print("Correct!")
                count_correct += 1
                counter.setdefault(random_question, [0, 0])
                counter[random_question][0] += 1
            elif answer.lower().strip() == 'hint':
                hint = quiz.hint(random_question)
                print(f"Hint: {hint}")
                hint_count += 1
                if hint_count == hint_limit:
                    print("No hints left")
                    break

            else:
                print(f"Incorrect! the correct answer is {correct_answer}")
                print(f"if you want a hint, type 'hint' to give yourself one \n or type 'get_hint' to get a hint from the database")
                count_incorrect += 1
                counter.setdefault(random_question, [0, 0])
                counter[random_question][1] += 1

        else:
            print("Invalid choice")
        
# KNOWLEDGE BASE APP

class Card2:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def __str__(self):
        return f"{self.title}: {self.content}"
    
class KnowledgeBase:
    def __init__(self, name):
        self.name = name
    
    def add_card(self, card):
        with shelve.open(self.name) as db:
            db[card.title] = [card.content]
    
    def get_card(self, title):
        with shelve.open(self.name) as db:
            return db[title]
    
    def delete_card(self, title):
        with shelve.open(self.name) as db:
            if title in db:
                del db[title]
                print(f"Deleted: {title}")
            else:
                print(f"Card '{title}' not found in database")
    
    def list_cards(self):
        with shelve.open(self.name) as db:
            for title, content in db.items():
                print(f'{title}: {content}')

def knowledge_base_app():
    kb = KnowledgeBase('myknowledge')
    while True:
        first = input('add, get, delete, list or quit')
        if first == 'quit':
            break
        elif first == 'add':
            title = input('title: ')
            content = input('content: ')
            card = Card2(title, content)
            kb.add_card(card)
        elif first == 'get':
            title = input('title: ')
            print(kb.get_card(title))
        elif first == 'delete':
            title = input('title: ')
            kb.delete_card(title)
        elif first == 'list':
            kb.list_cards()
        else:
            print('invalid input')

# print flashcard_app() for flashcard app
# print knowledge_base_app() for knowledge base app
