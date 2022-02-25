# My Random Movie Generator 

This repository gives you all you need to launch your very own Movie website, equipped with all the features for user login and registration, commenting and rating functionality as well as the ability to search endlessly through movies in the TMDB database as you go down the rabbit hole of clicking on the four `Similar Movies` provided to you at the bottom of the webpage. 

## Installation Requirements

Thanks for downloading my repo! I'm excited to help you deploy the site locally on your machine. 
Before we get started, let's make sure you have all the necessary components installed to run this code.
Run these commands in your terminal to get started:
1. `pip3 install python-dotenv`
2. `pip3 install requests`
3. `pip3 install flask`
4. `pip3 install flask_sqlalchemy`
5. `pip3 install flask_login`
6. `pip3 install psycopg2`
7. `pip3 install werkzeug`


## Sign up with TMDB to get an API key

Once you have signed up and received an API key you'll need to add a .env file to your project.
Inside this .env file create a variable called (`TMDB_KEY`) and assign it a string value of your newly aquired API Key.
The rest of my code will locate this key in your `.env` file and use it to pull the necessary info down from TMDB.
This key is meant to be super secret, but don't worry. I have included a `.gitignore` file that will keep this secret automatically. Next, 

## You're ready to Run!

Finally, all you have to do now is open up a new terminal window and type in `python main.py` and you should be given a link 
to check out your newly deployed website locally!

## Check out my own deployment of the site!

If you are interested [CLICK HERE](http://damp-castle-17150.herokuapp.com/) to view my site!


## Overview of Libraries used to create this project

For this project I utilized flask, a small and lightweight Python web framework that allowed me to build my web application. 
I also had to import and use the external python libraries: `python-dotenv`, `requests`, `flask`, `flask_sqlalchemy`, `flask_login`, and `werkzeug`, as well as several internal libraries like `os`, and `random`.

The `requests` library allowed me to make calls to the TMDB web API and get back a response with the relevant info on the movie I was querying for, which I then converted into a json and parced to find and store the relevant information on the movies I would then display on my web page. 

The `python-dotenv` library was used to retreive my TMDB API key from my `.env` file in a secure manner to then use in my main codebase when making calls to TMDB's API.

The `os` library was also used in retreival of the API key stored in my `.env` file using the method `.getenv()`.

I used five internal libraries within the `flask` library: `render_template`, `request`, `redirect`, `url_for`, and `flash`. The `render_template` was used to render the python code through flask into an html doc that then was able to display my webpage using the logic written in python. The `request`, I actually learned about from an in class demo, which basically is used to know when a POST was made by the HTML and then notify my interal logic in my python code as well as to then store the data that was posted back to that code. The `redirect` and `url_for` both basically operate the same way and are just used as ways to navigate from route to route within your code. And, finally, `flash` was an important one, because it gave me the ability to display messages on the screen for users of the webpage when they do things like enter an incorrect username or password or try to signup with a username that already exists. 

Next, I used `flask_sqlalchemy` to basically wire up my flask app to be able to create a database. `flask_sqlalchemy` allowed me to create 3 `Models` for users, comments, and ratings, each with their own unique set of attributes that I used to build my tuples in my tables as users interact with the website.

`flask_login` and its libraries were used to handle my user class and all the signup, login, and logout functionality of my app. I heavily referenced the documentation linked to us in the milestone 2 writeup to get my `flask login` working. Pretty much following the set up guide step by step and working out a few bugs along the way until it was all working correctly. The most important feature I found from this library was the `current_user` feature. This allowed me to keep track of which users commented on what as well as rated what and to then display their username alongside things like their comments. For the ratings, though they are not uniquely showed for each user, if you were to go into my database you will find records of every rating and the user that left them. But, on the front end, I chose to make a stylistic choice to only display the average rating amongst all user's ratings in an effort to keep my page clearer and free from overcluttering. 

As we know security is a big issue in today's online world. It is common practice to keep passwords secure and for that reason I employed `werkzeug` to hash my passwords as soon as they were posted back by the user so that if you were to go into my database or if my database was compromised, no hacker could make sense or decode the users' passwords saved there.

Finally, the `random` library was used to randomize the choices of movie ID's I kept within a list that I would plug into my API call to get the info on that specific movie to use and manipulate to ultimately populate my webpage with.

## Overview of API's used to create this project

For this project, I used two API's: the TMDB API to get data on a predefined list of movies as well as the wikipedia API to provide links at the bottom of my webpage for the viewer to follow and be taken to that movie's wikipedia page. 

## Reflections on my project

## Overview of what I created for Milestone 1 and then Milestone 2

For Milestone 1, I started by creating what was a duplicate of the example given by my professor in his assignment document. Given that I started early on this project, once I got the bear minimum working, I started to delve into additional features as well as styling of my web page. I used bootstrap to create the custom navigation bar at the top of my page that a user can actually interact with. The navigation bar has two choices: Recommended Movie and Wikipedia. Every time you click Recommended Movie, a movie is displayed from my pre-defined list of movies that I embedded in my `tmdb_api_call.py`. When you click on Wikipedia, you are taken to the wikipedia page for that movie, which I embedded into my website. I made this decision because I thought it was logical to stay on my website page and not be taken to another page, as well as for what I believe is a more stylistic approach. I also decided to go beyond the assignment requirements by including four similar movies at the bottom of the screen. All four of these are clickable which will then repopulate the page with the main movie displayed being the similar movie you just clicked on, as well as refreshing the similar movies displayed at the bottom to reflect those similar to the new movie displayed at the top of the screen. At the recommendation of a fellow student, I explored Google Fonts as a way to bring more style to my web page. I employed four custom Google Fonts in my project, which I believe is an improvement from what I started with, copying my professor's example. 

For Milestone 2, I was tasked with implementing user login functionality, ratings and comments. I did this by employing a postgresql database to store all of the data I derived from users' account information as well as all user comments and ratings. `Flask_login` was super helpful in implementing login functionality and took a lot of the load off my shoulders with relatively few lines of code. I'm gonna be honest. When I first looked at the Milestone 2 spec, specifically John's example of what the app should look like, I was underwhelmed and felt challenged to take on the functionality of the requirements but bring a lot more style and cleanness to them. I first tackled the ratings requirement. I was inspired from the beginning of the assignment to implement a visual 5 star rating system. I was able to find a template of html and css code online that I worked from, but I had to do a lot of backend work to get it all wired up so that it passed the rating information back to python. Once I figured out how to get the numerical value of the user's rating back into my python code from the html, I decided it would be cool if there was an average user rating displayed for each movie. So, I wrote an algorithm to get each rating on the fly and calculate the average, which I then rounded to one decimal place to give the rating a sleeker look, on par with the stylistic approach of IMDB. Next, once I got all the logic and communication from the front end to the backend and back to the front end working for the comments, it was time to style them. I utilized google fonts to do this for the text displayed as well as putting all the comments into a scrollable window which would allow for the user to still read through all of the comments, but while not having what feels like an endlessly scrolling page. This was also important because I didn't want the similar movies displayed at the bottom of the screen to get pushed further and further down after the addition of each new user comment. 

## Video Walkthrough

Here's a walk through of my website:

<img src='Milestone2.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with [LiceCap](http://www.cockos.com/licecap/).

### Known Problems with my Project

There is only one bug with my project and that is when a user hits refresh after having left a comment, the comment doesn't get removed from the cache, the page posts the old comment back and the comment gets posted again. I tried googling how to fix this within html or javascript, but I couldn't come up with any concrete fixes after implementing several. So, the only problem I would fix with my site is the double posting of comments on page refreshes. I decided to save myself further frustration when I went to John's office hours today and he assured me no points would be deducted for that bug, so I am turning in my milestone as is. Apart from that, I wish I could have found better fonts for the comments section. I ended up just going with `Courier` after trying out several custom google fonts. The google fonts were just a little too flashy for what I was looking for, and I guess you can't get classier than `Courier`. I'm sure if I spent an additional hour trying out more google fonts I could have arrived at something better, but that work is for another time. I've also noticed that Heroku is extremely slow in it's response time when navigating and using my website. This really bothers me, but since my webpage flies when I run it locally, I have also let that performance issue go.

### Project Implementation vs. Planning

I would say that my real problem and struggle with this project was my lack of a planning stage. I sort of just dove right into it starting with the login and when I got stuck on that, I stopped working for a few days. If I would have planned more, I could have said to myself, "hey, let's move on to a different aspect of the requirements for the milestone and get back to login later." But, I didn't and just got stuck on login. My time would have been so much better utilized skipping past the login implementation phase and moving on to implementing things like the comments or the rating system, which I only got to after days of wracking my head over the issues with my `flask_login`. Although I didn't have much planning before I started implementing, I will say that as I went along, I started realizing the importance of planning and after I got my `flask_login` to work, I really did turn to pen and paper and write to-do lists for myself regarding implementation of the comments and ratings. I wrote so many notes about how I might approach things from a routing and algorithmic standpoint that I later referenced while writing my code for reminders and inspiration. All in all, I would say this milestone was a great learning experience for me in the importance of planning and getting all your thoughts down on paper as they come to you for later use during implementation. 

### Technical Issues encountered during Milestone 1 & 2

#### Milestone 1

The first one is pretty dumb but took me awhile to figure out. I had written some python code to format the json I got back from the TMDB server. I mistakenly put the list I had parced from the json inside another list and kept getting errors when I tried to access the information in the nested list. I googled how to fix this and ended up writing a flatten method to take the nested list and turn it into just one list. It wasn't only until hours spent away from the code that I looked back and saw where I was putting the list into a list. It was at this point that I refactored my code, took away the additional outer list, and was finally able to parse the original list of entries as was intended. I was then also able to delete the unneeded flatten method from my code.

The second technical issue I had was when trying to display the movie poster. I kept thinking that the url I had to attatch the movie poster identifier from the json, the one ending in `.png`, was the original url I used to access the database. It was only after hours reviewing the TMDB's documentation for images that I saw an example url that was completely different from the database query url. I then copied the base of this url into my code and concatinated it with the movie poster identifier and bingo, the movie poster displayed just as it should have. 

The third technical issue was not realizing that HTML is a scripting language and not a specific coding language itself. I was under the impression that HTML was its own language like python or java and when I was googling how to write HTML code, I kept getting results that showed me javascript code. I assumed this can't be right! I had to call my dad after awhile, a seasoned software engineer and he explained to me that you can write lots of different types of coding languages embedded within an HTML document. Once I figured this out, I was able to better understand and implement logic in python within my `index.html` that displayed the movie info I needed to display, the way I wanted it displayed. 

Another huge issue for me was figuring out how to pass variables from one HTML document to another. I solved this problem through hours of Googling and was ultimately able to do it by utilizing very specific javascript code into my HTMLs. My professor even said when I asked him about this problem that it was a very unique problem that he had no idea how to solve, so I am very proud of myself for overcoming this issue. 

A smaller problem I encountered was how to approach making the similar movies clickable and for that to then post back movie Ids to my python code so the code could be recompiled and the page reloaded with the new main movie as the similar movie just clicked on. Again, I turned to Google and found my solution in utilizing a `button` in HTML in which I nested the poster images of the similar movies. 

#### Milestone 2

This milestone has really been a painful experience of hours of debugging and googling to finally get everything working the way it should. 

My first big roadblock was with getting `flask_login` to work. I spent about a dozen hours over the course of 3 days trying to get it functioning. I kept getting unknown errors, but I finally got it all to work after lots of googling. It mostly had to do with adding additional functions that were not discussed in the lengthy set up instructions that John linked us to in the spec. I was so happy when I finally got it working and am happy to say, that I imparted my deeper understanding of the bugs of `flask_login` to my fellow students, so that they could get unblocked at a much quicker pace than originally took me. Once piece of code that I was able to find online that saved me was:

`@login_manager.user_loader`
`def load_user(user_id):`
    `return User.query.get(int(user_id))`

This was not in the detailed walkthrough but proved to be neccessary for my implementation of `flask_login`.

My second technical issue was when I chose to stylistically display `no ratings yet` above my five stars on my main page. I didn't end up having to google much for this, but instead coming up with an algorithm that basically set a variable `avg_ratings` to 0 if there were no movie rating yet stored in the database and then set the same `avg_ratings` variable to the length of the queried ratings for the current movie. Then I added python logic into my html that said, `{% if avg_rating == 0 %}` then display `no ratings yet` else display the rounded average rating for that particular movie. It wasn't so much of an issue as a fun logical problem to solve. 

Next, I really struggled with making sure the page didn't load a new movie after a user left a new comment or rating. I ultimately had to do this by creating a new route called `/home_page_reload`. What this route allowed me to do was `POST` back the movie_id for the rated or commented on movie from the html, for which I employed a `form input` of `type="hidden"`. I have come to love these hidden form inputs as they have allowed me to pass back data from my html that never gets seen by the user during their experience interacting with my webpage. 

Lastly, I really struggled for several hours trying to get my app to deploy to heroku. I googled so much and got some very strange results, some of which I tried and some of which seemed to odd to even implement. It wasn't until I messaged John this morning that he was able to direct me to his pinned post on Discord where he detailed the exact issue I was having. It boiled down to `postgres://` versus `postgresql://`. So I followed his instructions and created a new variable with the `postgresql://` header in my `.env`. Then I went to the dashboard for my heroku app online and added a new `var` to my list of vars which included the correct `postgresql://` header. John said that this was a weird heroku bug where heroku is kind of incompatible with python, or so he explained to me. 

### Future Improvements

Since I've gotten the core of the code working and the webpage does exactly what it's supposed to do, in addition to fixing all the stylistic errors I was having in my code, I would say the only thing left that I would like to do as far as the requirements for milestone 2 are concerned, is improving the look and feel of my site. I tried to take inspiration from IMDB when it came to the 5 star rating system and the rating being an average of all users rating, which I am very proud to have accomplished but I am still a far cry away from building UI for a website that could compete with IMDB. I am proud of the work I have done, but I do have a long way to go as far as my knowledge and implementation of html and css to render professional-looking webpages. I also think it would be cool to implement a search bar feature that allows you to search for any movie you want, and that, even if you mistype the movie name, the search engine will still be able to figure out what you were going for with your query. 
