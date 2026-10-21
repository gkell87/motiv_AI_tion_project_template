from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
import smtplib, ssl, base64, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

users = [{'name' : '',
'email' : ''}]

line1 = 'A motivational poster in a slightly cartoonish style with the person in the reference pictures doing something amazing.'
line2 = 'Randomly pick something like climbing a mountain, running a marathon, boxing, baking a big cake, cooking an amazing meal'
line3 = 'being an action hero, being a super hero, discovering a long lost treasure, traveling to an interesting place,'
line4 = 'being a celebrity on the red carpet or being an astronaut! Be creative and fun about it. Also provide a famouse motivational or '
line5 = 'inspirational quote with the name of the person who said the quote.'

prompt = line1 + line2 + line3 + line4 + line5
aspect_ratio = "5:4" # "1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"
resolution = "2K" # "1K", "2K", "4K"

for user in users:
    client = genai.Client(api_key = '')
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[
            prompt,
            Image.open(f"assets/{user['name']}/{user['name']}1.jpg"),
            Image.open(f"assets/{user['name']}/{user['name']}2.jpg"),
            Image.open(f"assets/{user['name']}/{user['name']}3.jpg")
        ],
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution
            ),
        )
    )
    
    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif image:= part.as_image():
            encoded_image = base64.b64encode(image.image_bytes).decode('utf-8')
            data_uri = f'data:image/png;base64,{encoded_image}'

    sender_email = ""
    receiver_email = user['email']
    password = "fdjw cqqb osou xwci"
    
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    html = f"""\
    <html>
      <body>
        <h3> Greetings, Here is your Monday Motivation!!!</h3>
        <img src= {data_uri} height=500px widht=500px> 
      </body>
    </html>
    """
    
    message.attach(MIMEText(html, "html"))
    
    # Send the email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: # Define the Gmail SMTP server and port for SSL
            server.login(sender_email, 'fdjw cqqb osou xwci') # Set your email perameters
            server.send_message(message)
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication error. Check your email or app password.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    server.close()
