import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

class NotificationManager:
    
    def __init__(self):
        self.myemail=os.getenv("MYEMAIL")
        self.toemail=os.getenv("TOEMAIL")
        self.apppas=os.getenv("APPPAS")
        
        
        
    def send_notification(self,price,origin,destination,from_date,to_date):
        try:
            with smtplib.SMTP("smtp.gmail.com",587) as connection:
                connection.starttls()
                connection.login(user=self.myemail, password=self.apppas)
                message = (
                    f"Subject:Low Price Alert!\n\n"
                    f"Only {price} USD to fly from {origin} to {destination} "
                    f"from {from_date} to {to_date}."
                )
                connection.sendmail(to_addrs=self.toemail, from_addr=self.myemail,msg=message)
                print(f"Email sent successfully to {self.toemail}")
        except Exception as e:
            print(f"An error occurred while sending email: {e}")