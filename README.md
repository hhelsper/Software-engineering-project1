# My Random Movie Generator 

This repository gives you all you need to launch your very own random movie generator from a predefined list of movies

## Installation Requirements

Thanks for downloading my repo! I'm excited to help you deploy the site locally on your machine. 
Before we get started, let's make sure you have all the necessary components installed to run this code.
Run these commands in your terminal to get started:
1. `pip install python-dotenv`
2. `pip install requests`
3. `pip3 install flask`

## Sign up with TMDB to get an API key

Once you have signed up and received an API key you'll need to add a .env file to your project.
Inside this .env file create a variable called (`TMDB_KEY`) and assign it a string value of your newly aquired API Key.
The rest of my code will locate this key in your `.env` file and use it to pull the necessary info down from TMDB.
This key is meant to be super secret, but don't worry. I have included a `.gitignore` file that will keep this secret automatically. 

## You're ready to Run!

Finally, all you have to do now is open up a new terminal window and type in `python main.py` and you should be given a link 
to check out your newly deployed website locally!

## Check out my own deployment of the site!

If you are interested [CLICK HERE](https://mysterious-thicket-40093.herokuapp.com) to view my site!


## Overview of Libraries used to create this project

For this project I utilized flask, a small and lightweight Python web framework that allowed me to build my web application. 
I also had to import and use the external python libraries: `python-dotenv`, `requests`, and `flask` itself, as well as several internal libraries like `os`, and `random`.

The `requests` library allowed me to make calls to the TMDB web API and get back a response with the relevant info on the movie I was querying for, which I then converted into a json and parced to find and store the relevant information on the movies I would then display on my web page. 

The `python-dotenv` library was used to retreive my TMDB API key from my `.env` file in a secure manner to then use in my main codebase when making calls to TMDB's API.

The `os` library was also used in retreival of the API key stored in my `.env` file using the method `.getenv()`.

I used two internal libraries within the `flask` library: `render_template` and `request`. The `render_template` was used to render the python code through flask into an html doc that then was able to display my webpage using the logic written in python. The `request`, I actually learned about last week from an in class demo, which basically is used to know when a POST was made by the HTML and then notify my interal logic in my python code as well as to then store the data that was posted back to that code.

Finally, the `random` library was used to randomize the choices of movie ID's I kept within a list that I would plug into my API call to get the info on that specific movie to use and manipulate to ultimately populate my webpage with.

## Overview of API's used to create this project

For this project, I used two API's: the TMDB API to get data on a predefined list of movies as well as the wikipedia API to provide links at the bottom of my webpage for the viewer to follow and be taken to that movie's wikipedia page. 

## Reflections on my project

## Overview of what I created

For this project, I started by creating what was a duplicate of the example given by my professor in his assignment document. Given that I started early on this project, once I got the bear minimum working, I started to delve into additional features as well as styling of my web page. I used bootstrap to create the custom navigation bar at the top of my page that a user can actually interact with. The navigation bar has two choices: Recommended Movie and Wikipedia. Every time you click Recommended Movie, a movie is displayed from my pre-defined list of movies that I embedded in my `tmdb_api_call.py`. When you click on Wikipedia, you are taken to the wikipedia page for that movie, which I embedded into my website. I made this decision because I thought it was logical to stay on my website page and not be taken to another page, as well as for what I believe is a more stylistic approach. I also decided to go beyond the assignment requirements by including four similar movies at the bottom of the screen. All four of these are clickable which will then repopulate the page with the main movie displayed being the similar movie you just clicked on, as well as refreshing the similar movies displayed at the bottom to reflect those similar to the new movie displayed at the top of the screen. At the recommendation of a fellow student, I explored Google Fonts as a way to bring more style to my web page. I employed four custom Google Fonts in my project, which I believe is an improvement from what I started with, copying my professor's example. 

## Video Walkthrough

Here's a walk through of my website:

<img src='MoviePage.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with [LiceCap](http://www.cockos.com/licecap/).

### Known Problems with my Project

I've painstakingly made sure there are no problems with my project. The final thing to fix was the stylistic errors. I had a ton of trailing whitespace issues that I had to solve, but I have now gotten my Pylint errors down to 0. Other than that, there are no bugs in my code, I have ensured that each wikipedia link takes you to the correct page for the movie and not another page and that all the titles, one line descriptions, genres, and movie posters are all correct and display as specified, as well as to make sure the four displayed similar movies are the top four queried from the TMDB server.

### Technical Issues encountered during project

The first one is pretty dumb but took me awhile to figure out. I had written some python code to format the json I got back from the TMDB server. I mistakenly put the list I had parced from the json inside another list and kept getting errors when I tried to access the information in the nested list. I googled how to fix this and ended up writing a flatten method to take the nested list and turn it into just one list. It wasn't only until hours spent away from the code that I looked back and saw where I was putting the list into a list. It was at this point that I refactored my code, took away the additional outer list, and was finally able to parse the original list of entries as was intended. I was then also able to delete the unneeded flatten method from my code.

The second technical issue I had was when trying to display the movie poster. I kept thinking that the url I had to attatch the movie poster identifier from the json, the one ending in `.png`, was the original url I used to access the database. It was only after hours reviewing the TMDB's documentation for images that I saw an example url that was completely different from the database query url. I then copied the base of this url into my code and concatinated it with the movie poster identifier and bingo, the movie poster displayed just as it should have. 

The third technical issue was not realizing that HTML is a scripting language and not a specific coding language itself. I was under the impression that HTML was its own language like python or java and when I was googling how to write HTML code, I kept getting results that showed me javascript code. I assumed this can't be right! I had to call my dad after awhile, a seasoned software engineer and he explained to me that you can write lots of different types of coding languages embedded within an HTML document. Once I figured this out, I was able to better understand and implement logic in python within my `index.html` that displayed the movie info I needed to display, the way I wanted it displayed. 

Another huge issue for me was figuring out how to pass variables from one HTML document to another. I solved this problem through hours of Googling and was ultimately able to do it by utilizing very specific javascript code into my HTMLs. My professor even said when I asked him about this problem that it was a very unique problem that he had no idea how to solve, so I am very proud of myself for overcoming this issue. 

A smaller problem I encountered was how to approach making the similar movies clickable and for that to then post back movie Ids to my python code so the code could be recompiled and the page reloaded with the new main movie as the similar movie just clicked on. Again, I turned to Google and found my solution in utilizing a `button` in HTML in which I nested the poster images of the similar movies. 

### Future Improvements

Since I've gotten the core of the code working and the webpage does exactly what it's supposed to do, in addition to fixing all the stylistic errors I was having in my code, I would say the only thing left that I would like to do as far as the requirements for milestone 1 are concerned, is improving the look and feel of my site. I would mainly like to style my site to make it look a bit more modern and sleek. I would like to spend some time watching some tutorials on youtube for writing stylish html and css code and encorporating that style into my web page. 
