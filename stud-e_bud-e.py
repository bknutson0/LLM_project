import os
from openai import OpenAI
import dotenv
import json

# get API key
config = dotenv.dotenv_values(".env")
client = OpenAI(api_key='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')

# build quiz-making function that inputs text from course material and outputs a quiz on that material
def get_quiz(text, model='gpt-3.5-turbo-1106'):
    user_input = input('Do you have a text to make a quiz from? (y/n)\n')
    if user_input == 'y':
        print('Please save text to \'text.txt\'.\n')
    else:
        text = input('Please enter a topic of interest to make a quiz from.\n')

    prompt = f"""
        Create a five question, multiple-choice quiz on the text below.
        '''{text}'''
        """
    #print(f'Prompt:\n{prompt}')
    
    # messages = [{'role':'user', 'content':prompt}]
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=messages,
    #     temperature=0, # this is the degree of randomness of the model's output
    # )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to create a multiple-choice quiz based on user input. The quiz should be formatted as a JSON containing an array of question objects. Each question object has three keys: 'question', 'choices', and 'answer'."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

# test on sample text
nihilism_text = '''Nihilism is a family of views within philosophy that rejects generally accepted or fundamental aspects of human existence, such as knowledge, morality, or meaning. The term was popularized by Ivan Turgenev and more specifically by his character Bazarov in the novel Fathers and Sons. There have been different nihilist positions, including that human values are baseless, that life is meaningless, that knowledge is impossible, or that some set of entities does not exist or is meaningless or pointless. Scholars of nihilism may regard it as merely a label that has been applied to various separate philosophies, or as a distinct historical concept arising out of nominalism, skepticism, and philosophical pessimism, as well as possibly out of Christianity itself. Contemporary understanding of the idea stems largely from the Nietzschean 'crisis of nihilism', from which derive the two central concepts: the destruction of higher values and the opposition to the affirmation of life. Earlier forms of nihilism, however, may be more selective in negating specific hegemonies of social, moral, political and aesthetic thought. The term is sometimes used in association with anomie to explain the general mood of despair at a perceived pointlessness of existence or arbitrariness of human principles and social institutions. Nihilism has also been described as conspicuous in or constitutive of certain historical periods. For example, Jean Baudrillard and others have characterized postmodernity as a nihilistic epoch or mode of thought. Likewise, some theologians and religious figures have stated that postmodernity and many aspects of modernity represent nihilism by a negation of religious principles. Nihilism has, however, been widely ascribed to both religious and irreligious viewpoints. In popular use, the term commonly refers to forms of existential nihilism, according to which life is without intrinsic value, meaning, or purpose. Other prominent positions within nihilism include the rejection of all normative and ethical views, the rejection of all social and political institutions, the stance that no knowledge can or does exist, and a number of metaphysical positions, which assert that non-abstract objects do not exist, that composite objects do not exist, or even that life itself does not exist.'''
caesar_text = '''Gaius Julius Caesar; 12 July 100 BC 15 March 44 BC) was a Roman general and statesman. A member of the First Triumvirate, Caesar led the Roman armies in the Gallic Wars before defeating his political rival Pompey in a civil war, and subsequently became dictator from 49 BC until his assassination in 44 BC. He played a critical role in the events that led to the demise of the Roman Republic and the rise of the Roman Empire. In 60 BC, Caesar, Crassus, and Pompey formed the First Triumvirate, an informal political alliance that dominated Roman politics for several years. Their attempts to amass political power were opposed by many in the Senate, among them Cato the Younger with the private support of Cicero. Caesar rose to become one of the most powerful politicians in the Roman Republic through a string of military victories in the Gallic Wars, completed by 51 BC, which greatly extended Roman territory. During this time he both invaded Britain and built a bridge across the river Rhine. These achievements and the support of his veteran army threatened to eclipse the standing of Pompey, who had realigned himself with the Senate after the death of Crassus in 53 BC. With the Gallic Wars concluded, the Senate ordered Caesar to step down from his military command and return to Rome. In 49 BC, Caesar openly defied the Senate's authority by crossing the Rubicon and marching towards Rome at the head of an army.[2] This began Caesar's civil war, which he won, leaving him in a position of near-unchallenged power and influence in 45 BC. After assuming control of government, Caesar began a programme of social and governmental reform, including the creation of the Julian calendar. He gave citizenship to many residents of far regions of the Roman Republic. He initiated land reforms to support his veterans and initiated an enormous building programme. In early 44 he was proclaimed "dictator for life" (dictator perpetuo). Fearful of his power and domination of the state, Caesar was assassinated by a group of senators led by Brutus and Cassius on the Ides of March (15 March) 44 BC. A new series of civil wars broke out and the constitutional government of the Republic was never fully restored. Caesar's great-nephew and adopted heir Octavian, later known as Augustus, rose to sole power after defeating his opponents in the last civil war of the Roman Republic. Octavian set about solidifying his power, and the era of the Roman Empire began. Caesar was an accomplished author and historian as well as a statesman; much of his life is known from his own accounts of his military campaigns. Other contemporary sources include the letters and speeches of Cicero and the historical writings of Sallust. Later biographies of Caesar by Suetonius and Plutarch are also important sources. Caesar is considered by many historians to be one of the greatest military commanders in history.[3] His cognomen was subsequently adopted as a synonym for "Emperor"; the title "Caesar" was used throughout the Roman Empire, giving rise to modern descendants such as Kaiser and Tsar. He has frequently appeared in literary and artistic works.'''

quiz = get_quiz(caesar_text)
#print(quiz)

#assert quiz['quiz']['questions'].length == quiz['quiz']['correct_answers'].length
letters = ['A', 'B', 'C', 'D']
questions = quiz['questions']
for i in range(len(questions)):
    print(questions[i]['question'])
    for j in range(len(questions[i]['choices'])):
        print(letters[j], questions[i]['choices'][j])
    user_input = input()
    user_choice = questions[i]['choices'][letters.index(user_input)]
    answer = questions[i]['answer']
    if user_choice == answer:
        print('Correct')
    else:
        print('Incorrect: correct answer is', questions[i]['answer'])

    # grade 

