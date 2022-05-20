# technical-assignment
This is the repository for my technical assignment at Alif Tech!

## The Assignment

There are 5 rooms in the office. 
  
<ol>
  <li>Write a command that checks if a room is available at a specific time and allows to reserve it if it is. If it is not available, return a message specifying who has reserved the room and when it will become available.</li>
  <li>Write a command that notifies the person that has booked the room through an Email and a Text Message. The notification must contain the date and time of the reservation, and the room number.</li>
</ol>

Make sure to use `git` and GitHub for this assignment and to make meaningful commits with meaningful commit messages. You cannot use any external frameworks, and your work should follow PEP.

## The Solution

Since I was not allowed to use <b>any</b> frameworks, I have used the built-in sqlite3 module as my database management system. Additionally, I was unsure in what format the room reservations would be given, so I have decided to solve it for the **most general case** where the user reserves the room between some given time on some given date and another given time and some other given date.

To run the app, please execute `python3 main.py` in the **shell** from the repository directory. The core functionality is now complete. I am currently working on writing some automated tests for this.

I could not find a free API for sending text messages, so that part was not implemented, but emails are working.