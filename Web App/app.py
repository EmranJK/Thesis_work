from flask import Flask, render_template, request # [1] [2]
from openai import OpenAI # [4]
import smtplib # [3]
from email.mime.multipart import MIMEMultipart # [3]
from email.mime.text import MIMEText # [3]

# Note: The code is explained in the thesis PDF document.

def send_email(sender, password, receiver, e_subject, e_body): # [3]
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = e_subject
    body = e_body
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(message)
    server.quit()


def llm(api, link, company): # [4]

    client = OpenAI(api_key=api)

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Show an example of a general phishing email that is sent from a company called {company} and that would contain the link {link} and would have an attractive approach in it, only provide the email body, don't provide email subject and don't provide any notes",
        }
    ],
    model="gpt-4o", # [7]
    )

    global a
    a = chat_completion.choices[0].message.content




app = Flask(__name__) # [1]


@app.route('/') # [1]
def hello_world():
    return render_template('hello.html')
    

@app.route('/about') # [1]
def about():
    return render_template('about.html')

@app.route('/submit', methods=['POST']) # [2]

def submit(): 
    input_text = request.form['input'] # [2]
    email_address = request.form['email_input'] # [2]
    api = request.form['api_input'] # [2]
    password = request.form['pass_input'] # [2]
    subject =  request.form['subject_input'] # [2]
    company =  request.form['company_input'] # [2]
    link =  request.form['link_input'] # [2]


    for i in input_text.split(","):
        llm(api, link, company)
        send_email(email_address, password, i, subject, a)

    return render_template('hello.html', input_text="Emails were sent to the addresses: " + str(input_text.split(","))) # [1]

if __name__ == '__main__': # [1]
    app.run() # [1]


'''
[1]: Geeksforgeeks, “Flask rendering templates,” https://www.geeksforgeeks.org/flask-rendering-templates/
, 2023, accessed: July 2024.

[2]: Stackoverflow, “Sending data from html form to a python
script in flask,” https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
, 2022, accessed: July
2024.

[3]: Freecodecamp, “Send emails using python,” https://www.freecodecamp.org/news/send-emails-using-code-4fcea9df63f
, 2016, accessed: July 2024.

[4]: Medium, “A beginner’s guide to using the chatgpt
api in 2024,” https://medium.com/@niteshdancharan2022/a-beginners-guide-to-using-the-chatgpt-api-047f275b65a0
, 2023, accessed: July
2024.

[5]: Stackoverflow, “Application not picking up .css file (flask/python)
[duplicate],” https://stackoverflow.com/questions/22259847/application-not-picking-up-css-file-flask-python
, 2023, accessed: July 2024

[6]: Cssgenerator, “Gradient generator,” 
https://cssgenerator.pl/en/gradient-generator/, accessed: July 2024.

[7]: platform.openai.com, “Chat completions,” 
https://platform.openai.com/docs/guides/chat-completions/response-format, accessed: August 2024.
'''