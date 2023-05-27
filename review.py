from afinn import Afinn
import streamlit as st
import smtplib

sia = Afinn()
def analyze_sentiment(text):
    score = sia.score(text)
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'


def write_review_to_file(review, text):
    with open('reviews.txt', 'a+') as file:
        file.write(review)
    with open('sentence_reviews.txt', "a+") as file:
        file.writelines(text)


# ----- main page ------- #
st.title("Sentiment Analysis")
text = st.text_area("Enter the text:")
if st.button("click"):
    sentiment = analyze_sentiment(text)
    st.write("Reponse Recorded")
    st.write("PLEASE CLEAR THE TEXT BOX TO ENTER A NEW REVIEW OR SUGGESTION")

    # Write review to file
    text = " ".join(text.rstrip('\n').split("\n"))
    # text = text.rstrip('\n')
    if sentiment == "Positive":
        write_review_to_file("1", f"({text}, positive)\n")
    elif sentiment == "Negative":
        write_review_to_file("2", f"({text}, negative)\n")
    else:
        write_review_to_file("3", f"({text}, neutral)\n")


def overall_score():
    with open("reviews.txt", "r") as review:
        review_score = review.read()

    return {"Positive": review_score.count("1"),
            "Negative": review_score.count("2"),
            "Neutral": review_score.count("3"),
            }


score_dict = overall_score()


# Definition : Send mails to hod 
def sendMail(score_dict):
    sender="pavancs325@gmail.com"
    login_pass="ndpyfheoexnpxusy"
    server=smtplib.SMTP("smtp.gmail.com",587)
    
    server.starttls()
    server.login(sender,login_pass)

    subject = "Overall analysis of the reviews"
    message = f"subject : {subject}\nPostive Suggestions = {score_dict['Positive']}\nNegative Suggestions = {score_dict['Negative']}\nNeutral Suggestions = {score_dict['Neutral']}\n"

    server.sendmail(sender,'prathik3110@gmail.com',message)
    server.quit()
    print("Message sent Successfully")  # debug



# Send reviews
with open("sentence_reviews.txt", "r") as review:
    reviews = review.read()

# print("Reviews : ", reviews)

def sendMail1(review):
    sender="pavancs325@gmail.com"
    login_pass="ndpyfheoexnpxusy"
    server=smtplib.SMTP("smtp.gmail.com",587)
    
    server.starttls()
    server.login(sender,login_pass)

    subject = "Reviews"
    message = f"subject : {subject}\n{review}"

    server.sendmail(sender,'prathik3110@gmail.com',message)
    server.quit()
    print("Message sent Successfully")  # debug


# Call : Sends mail
if sum(score_dict.values()) == 3:
    sendMail(score_dict)
    sendMail1(reviews)





