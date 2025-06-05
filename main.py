import os
import sys
import time
import ast
import random
import re
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
        model="compound-beta",
    )

    return chat_completion

def main():

    lodges = get_lodge_names()
    result = {}

    '''Find confirmed amenities of every lodge'''
    for i in range(0, len(lodges)):
        
        '''Variables to retry API if API calls fail'''
        current_tries = 1
        MAX_RETRIES = 10
        DELAY = 1
        error = False

        while current_tries < MAX_RETRIES:

            confirmed = {}   

            #'''Convert the response into a dictionary. Should the conversion of string to dictionary result in SyntaxError, we will go to the except block'''
            try:

                #'''Ask the AI for a response & convert to dictionary'''
                confirmed_amenities = receive(lodges[i][0]).choices[0].message.content
                confirmed = ast.literal_eval(confirmed_amenities)
                print("done")
                break
            
            except RateLimitError as e:
                error = True
                break
                # msg = (str(e))
                # print(msg)
                # match = re.search(r'try again in (\d+)m(\d+(?:\.\d+)?)s', msg)
                # if match:
                #     min = int(match.group(1))
                #     sec = float(match.group(2))
                #     total_sleep_time = (min * 60) + sec + 60
                #     time.sleep(total_sleep_time)
                # continue

            #'''If conversion from string to dictionary fails, retry until the syntax is right or we've retried up to 11 times'''
            except SyntaxError:
                no_syntax_error = True
                stop = False
                current_tries = current_tries + 1

                while no_syntax_error and current_tries < MAX_RETRIES:
                    time.sleep(DELAY * (2 ** current_tries) * random.uniform(0, 0.5))
                    print("Overwhelmed")
                    try:
                        c = receive(lodges[i][0]).choices[0].message.content
                        confirmed = ast.literal_eval(c)
                        no_syntax_error = False
                        stop = True
                    except SyntaxError:
                        current_tries = current_tries + 1
                        continue

                '''If the API call was successful, break out of the while loop'''
                if stop:
                    break

        if error: 
            print("error")
            break

        '''Add Lodge: Amenities'''
        result[lodges[i][0]] = confirmed
        time.sleep(DELAY * (2 ** current_tries) * random.uniform(0, 0.5))
   

    '''Create the new Dataframe from our results'''
    create_amenities_dataframe(result)

if __name__ == '__main__':
    main()
