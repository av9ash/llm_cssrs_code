import os
import google.generativeai as genai
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def get_response(post):
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    p = ("\n Evaluate these post step by step and assign them severity on a scale of 0-6, "
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
         # "\n\"Q1\": Wording that fulfills this criteria or N/A"
         # "\n\"Q2\": Wording that fulfills this criteria or N/A"
         # "\n\"Q3\": Wording that fulfills this criteria or N/A"
         # "\n\"Q4\": Wording that fulfills this criteria or N/A"
         # "\n\"Q5\": Wording that fulfills this criteria or N/A"
         # "\n\"Q6\": Wording that fulfills this criteria or N/A"
         "\n\"severity\": integer (0-6)\n"
         "}")

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"{p} \n {q} \n {r}",
                ],
            }
        ]
    )

    response = chat_session.send_message(post)
    r = response.text.replace("json", "")
    r = r.replace("```", "")
    return r

# post = "Constant cycle of fighting my addictive demons and losing… and then hating myself for it before I just end up repeating the same over and over\n"
# print(get_response(post))