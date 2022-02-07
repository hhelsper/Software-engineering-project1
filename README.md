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


## Overview of utilities used to create this project

For this project I utilized flask, a small and lightweight Python web framework that allowed me to build my web application. 
I also had to import and use the external python libraries: `python-dotenv`, `requests`, and `flask` itself, as well as several internal libraries like `os`, and `random`.
The `requests` library allowed me to make calls to the TMDB web API and get back a response with the relevant info on the movie I was querying for, which I then converted into a json and parced to find and store the relevant information on the movies I would display. 