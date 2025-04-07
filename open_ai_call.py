from openai import OpenAI
client = OpenAI()
import json

def get_response(user_content):
    h = 'Consider only the following, this COLUMBIA-SUICIDE SEVERITY RATING SCALE metrics:'
    q1 = '1) Have you wished you were dead or wished you could go to sleep and not wake up? Severity: 1'
    q2 = '2) Have you actually had any thoughts about killing yourself? Severity: 2'
    q3 = '3) Have you been thinking about how you might do this? Severity: 3'
    q4 = '4) Have you had these thoughts and had some intention of acting on them? Severity: 4'
    q5 = '5) Have you started to work out or worked out the details of how to kill yourself? Did you intend to carry out this plan? Severity: 5'
    q6 = '6) Have you done anything, started to do anything, or prepared to do anything to end your life? Severity: 6'
    questions = [h, q1, q2, q3, q4, q5, q6]
    c_card = '\n'.join(questions)
    prompt = "\n Evaluate these post question by question and assign them severity on a scale of 0-6, where 0 means the post is not related to suicide, and 1-6 depending on the metrics above where 1 is for the first question and 6 for the last. \n"
    expected_template = {
        "Q1": "Wording that fulfills this criteria else N/A",
        "Q2": "Wording that fulfills this criteria else N/A",
        "Q3": "Wording that fulfills this criteria else N/A",
        "Q4": "Wording that fulfills this criteria else N/A",
        "Q5": "Wording that fulfills this criteria else N/A",
        "Q6": "Wording that fulfills this criteria else N/A",
        "severity": "integer (0-6)",
    }

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            # {"role": "system", "content": "Provide a structured JSON response containing evaluated severity and reasoning behind it."},
            {"role": "system", "content": f"Provide a structured JSON response with the following format: {json.dumps(expected_template)}."},
            {"role": "user", "content": c_card+prompt+user_content}
        ]
    )

    return response.choices[0].message.content

# user_content = 'please help I feel like I deserve to die please help me'
# response = get_response(user_content)
# graded_result = response.choices[0].message.content
# print(json.loads(graded_result))