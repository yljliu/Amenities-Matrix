import os
import time
import ast
import random
from groq import Groq, RateLimitError
from amenities import get_lodge_names, create_amenities_dataframe
from requirements import get_prompt

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def receive(lodge):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": get_prompt(),
            }
            ,
            {
                "role": "user",
                "content": "Does the lodge - " + lodge + " - contain the following amenities: swimming pool, waterhole, starbed, plunge pool, private terrace, landscape view, river view, fenced, not fenced, kid's club, spa, bar, beachfront, beach access, camp fire, buffet, A La Carte, Family Room, 24h Power, Inside the park"
            }
        ],
        model="llama-3.1-8b-instant",
    )

    return chat_completion

def main():
    
    lodges = get_lodge_names()
    print(lodges)
    result = {}

    '''Find confirmed amenities of every lodge'''
    for i in range(0, len(lodges)):
        
        '''Variables to retry API if API calls fail'''
        current_tries = 0
        MAX_RETRIES = 6
        DELAY = 1
        error = False

        while True:

            confirmed = {}   

            #'''Convert the response into a dictionary. Should the conversion of string to dictionary result in SyntaxError, we will go to the except block'''
            try:
                #'''Ask the AI for a response & convert to dictionary'''
                confirmed_amenities = receive(lodges[i][0]).choices[0].message.content
                confirmed = ast.literal_eval(confirmed_amenities)
                print("done")
                break
            
            #If we hit our rate limit, stop because our free tier has ended (for 24 hours)
            except RateLimitError as e:
                error = True
                break

            #'''If conversion from string to dictionary fails, retry until the syntax is right or we've retried up to 11 times'''
            except SyntaxError:
                current_tries = current_tries + 1

                if current_tries > MAX_RETRIES:
                    error = True
                    break
                time.sleep(DELAY * (2 ** current_tries) * random.uniform(0, 0.5))

        if error: 
            print("Resource Exhausted")
            break

        '''Add Lodge: Amenities'''
        result[lodges[i][0]] = confirmed
        if i == 30:
            break

    '''Create the new Dataframe from our results'''
    print(result)
    create_amenities_dataframe(result)

if __name__ == '__main__':
    main()
