# SQLalchemy-Challenge

Here is my attemp at creating an API after analyzing an SQL file that contants weather data from stations in Hawai'i! This challenge was definitely tough, but after some research everything came togehter smoothly.

For the first step in the challenge, I analyzed some SQL data in python using SQLalchemy. This was intuitive enough, just learning the syntax for alchemy was the biggest challenge in this part that I had. However, combining this with good ol' pandas and matplotlib made it easy for me to sparse everything out cleanly. 

The biggest challenge by far was creating the API routes using Flask. I had to do a lot of research and review a lot of notes to make it work, but in the end it came out nicely in my humble opinion. Getting everything started with flask and the variables was simple enough, but the real challenge came with creating the routes. Creating the routes themselves was challenging enough, but trying to get it to return as JSON data was another thing. I just defaulted to appening a list with a dictionary for each of my routes because I was mainly getting data type errors. One thing that stumped me for a while was in the station route, as it returns a list of touples rather than a normal list. I had to scour the internet unitl I came across this code:

# station_list = list(np.ravel(active_stations))
 
Thank the lord for Stack Overflow.

The last major challenge I had was with the date ranges, but this came down to me figuring out how routes with data worked. I was oirignally putting the date needed as the route instead of creating a variable to hold a date. After a lot of troubleshooting, I believe my API came out pretty solid. 

