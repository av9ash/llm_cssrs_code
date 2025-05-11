import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def get_assessment(post):
    # Prompt to detect language and translate
    p = ("\n Evaluate this post step by step and assign them severity on a scale of 0-6, "
              "where 0 means the post is not related to suicide, "
              "and 1-6 depending on the metrics above where 1 is for the first question and 6 for the last. \n")

    q = ('COLUMBIA-SUICIDE SEVERITY RATING SCALE metrics:\n'
         '1) Have you wished you were dead or wished you could go to sleep and not wake up? Severity: 1\n'
         '2) Have you actually had any thoughts about killing yourself? Severity: 2\n'
         '3) Have you been thinking about how you might do this? Severity: 3\n'
         '4) Have you had these thoughts and had some intention of acting on them? Severity: 4\n'
         '5) Have you started to work out or worked out the details of how to kill yourself? Did you intend to carry out this plan? Severity: 5\n'
         '6) Have you done anything, started to do anything, or prepared to do anything to end your life? Severity: 6\n')

    r = ("\n\n Provide your response in JSON format, using the following template:\n\n"
         "{"
         "\n\"Q1\": Reasoning that fulfills this criteria or N/A"
         "\n\"Q2\": Reasoning that fulfills this criteria or N/A"
         "\n\"Q3\": Reasoning that fulfills this criteria or N/A"
         "\n\"Q4\": Reasoning that fulfills this criteria or N/A"
         "\n\"Q5\": Reasoning that fulfills this criteria or N/A"
         "\n\"Q6\": Reasoning that fulfills this criteria or N/A"
         "\n\"severity\": integer (0-6)\n"
         "}")

    # Create a chat completion request
    response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": p+q+r+'\n\n post: '+post,
            },
        ]
    )

    response_text = response.choices[0].message.content
    r = response_text.replace("```json", "").replace("```", "").strip()
    return r


# post = "Constant cycle of fighting my addictive demons and losing… and then hating myself for it before I just end up repeating the same over and over\n"
# print(get_assessment(post))