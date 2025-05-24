import os
from groq import Groq

from amenities import parse_amenities, create_amenities_dataframe
from requirements import inform_AI

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def receive(lodge):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": inform_AI(),
            }
            ,
            {
                "role": "user",
                "content": "Does the lodge - " + lodge + " - contain the following amenities: swimming pool, waterhole, starbed, plunge pool, private terrace, landscape view, river view, fenced, not fenced, kid's club, spa, bar, beachfront, beach access, camp fire, buffet, A La Carte, Family Room, 24h Power, Inside the park"
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion

def main():

    lodges = parse_amenities()
    result = {}

    for i in range(0, len(lodges)):
        answers = receive(lodges[i][0]).choices[0].message.content

        #Since our answers variable returns a string rather than an dictionary, we have to actually build the array of Yes and No that corresponds to each amenity
        confirmed = []
        length = len(answers)
        index = 0
        
        while index < length:
            if answers[index] == '{' or answers[index] == '}' or answers[index] == ',' or answers[index] == " " or answers[index] == '"':
                index = index + 1
            elif answers[index] == 'Y' and answers[index + 1] == 'e' and answers[index + 2] == 's':
                confirmed.append("x")
                index = index + 3
            elif answers[index] == 'N' and answers[index + 1] == 'o' and answers[index + 2] == '"':
                confirmed.append(" ")
                index = index + 2
            else:
                index = index + 1

        #Add Lodge: Amenities
        result[lodges[i][0]] = confirmed

    #Create the new Dataframe
    create_amenities_dataframe(result)

if __name__ == '__main__':
    main()
