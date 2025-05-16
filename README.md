# cits3403-group-5-2025-S1

## Group Members
| UWA ID | Name | Github Username |
| ------ | ---- | --------------- |
| 23730148 | Archer Key | Archer-Key |
| 23744478 | Hayashi Lin | enqinghayashi |
| 23801947 | Thisal Wickramasinghe Arachchilage | wicky-t |
| 24275986 | William Walmsley | cal05s |

## Description
Our app is a music rating application where users can rate their favourite tracks, albums, and artists and then view stats about how their ratings compare to their listening history, view their friend's ratings and their friends stats.

We have designed the app to be easy to understand and easy to use. Rating music is as easy as using the search bar like Google and then entering their scores in the score box by either pressing Enter or hitting the save button, viewing your stats is as easy as navigating to the page and clicking generate, and to share with your friends all you have to do is tell them your user id and then accept their friend requeset.

We analyse a user's data by calculating a listening score for each track in a user's listening history where their most listened track is a 10 and their least listened track is a 0. We then use these scores and a user's ratings to create aggregate data for their albums, artists, track duration, and release year to use for analysis. 

Once we've collected and calculated this data for the scores in our database and the scores from Spotify we look for any common items between the two, graph them on a grid and find the correlation between the score you gave and its listening score we calculated. We also look at the graph and pick the items closest to each of the corners for the highest rated, most listened, highest rated, least listened, etc. as well as the item that is furthest away from the line of best fit through your items.

## Requirements
- Access to a Spotify Premium account.
  - A Spotify Premium account is required to make an app with the SpotifyAPI.
  - If you do not have a Spotify Premium account but do have a free account and know of someone who does have a premium account, you can ask them to create the Spotify app and add you as a user and you will still be able to use this application.
  - In the submitted copy of this application a Spotify Premium account made with a 3 month free trial is provided soley for the purpose of testing this project, please refer to login_details.md for more information.

## Setting Up The Spotify API
This project uses the Spotify API to obtain data about tracks, albums, and artists that a user searchs for as well as obtaining the user's top tracks and artists that is then used for analysis.

As this app is still in the Spotify API's 'Development Mode', users must be added manually by the owner of the Spotify API app and thus we detail the process of setting up a new app to allow anyone to try it out for personal use.

If you are using the account provided for marking purposes, this has already been done for you but is still useful to read in case you are running the flask app on a port that is not 5000 or you wish to use your own Spotify Premium account (prefereable) or add your free acount to ther users.

### Logging In To Spotify For Developers
Navigate to https://developer.spotify.com/documentation/web-api.
![Spotify for Developers welcome page.](/readme_images/appsetup0.png)

Now click the 'Log in' button in the top right and log in using your regular Spotify account details.
![Spotify login page.](/readme_images/appsetup1.png)

If you are using the provided account and are prompted with the 6-digit code select 'Log in with a password' and use the password provided.
![Spotify login page.](/readme_images/appsetup2.png)
![Spotify login page.](/readme_images/appsetup3.png)

### Creating The Spotify API App
Now that you've logged in you should see something like this:
![Spotify for Developers home page.](/readme_images/appsetup4.png)

Click the user dropdown in the top right and click 'Dashboard'. You should see something like this:
![Spotify for Developers dashboard.](/readme_images/appsetup5.png)

Click the button that says 'Create app'. You should see the following:
![Spotify for Developers create app.](/readme_images/appsetup6.png)

Now fill in the 'App name', 'App description' with anything you see fit. Under 'Redirect URIs' fill in the address 'http://127.0.0.1:5000/auth' and click the 'Add' button. This redirect uri is essential for the app to work, this is where Spotify redirects you to after you succeed or fail authorization.
![Spotify for Developers create app redirect uri.](/readme_images/appsetup7.png)

(NOTE: The port number 5000 can be changed if you are running the flask app on a different port. THE PORT NUMBER MUST BE THE SAME AS THE ONE THAT YOU ARE RUNNING THE FLASK APP ON. If you are running the app on a different port you will also have to change the `redirect_uri` in auth.py which we will detail later. YOU MAY NOT CHANGE THE '/auth' AT THE END OF THE REDIRECT URI, ONLY THE PORT IS ABLE TO BE CHANGED.)

We will also need to check the 'Web API' box and agree to the terms of use.

Once everything has been filled in it should look something like this:
![Spotify for Developers create app full details.](/readme_images/appsetup8.png)

Hit 'Save' and you should see a page that looks like this:
![Spotify for Developers app basic information.](/readme_images/appsetup9.png)

### Adding the Client ID to the Flask App
Copy the Client ID from the page you are now on and navigate to /app/auth.py.
![auth.py screenshot](/readme_images/appsetup10.png)

Inside the quotation marks of `self.client_id` place the Client ID you copied earlier and save the file.

(NOTE: If you changed the port of the redirect uri earlier you will also have to change it under `self.redirect_uri`).

The Flask App will now be linked to your Spotify API app.

### (Optional) Adding Other Users to Your Spotify API App
Return the top App information page as shown below:
![Spotify for Developers home page.](/readme_images/appsetup9.png)

Above 'Client ID' click 'User Management' and you should see something like this:
![Spotify for Developers user management page.](/readme_images/adduser0.png)

Enter the full name and email of the Spotify account that you wish to allow access to the Spotify API app and hit 'Add user'. You should see something like this:
![Spotify for Developers user management page after adding friend.](/readme_images/adduser1.png)

### (Optional) Removing Other Users from your Spotify API App
To remove a user from your Spotify API app simly return to the user management page and click the three dots to the right of the user you wish to remove, then click 'Remove user'.
![Spotify for Developers user management page remove user highlighted.](/readme_images/removeuser0.png)

## Launching The Flask App
Once you have set up the virtual python environment and linked your Spotify API app to Auth you should then be able to run `python3 project.py` and navigate to the link it provides to you, something like `http://127.0.0.1:5000`.

## Using the App
Navigate to the front page and click 'Log in' in the top right corner.
![Rankd Home Page.](/readme_images/appuse0.png)

Click 'Register here' and fill in the details for a new account.
![Rankd Login Page.](/readme_images/appuse1.png)
![Rankd Register Page.](/readme_images/appuse2.png)

Click 'Register' to create your account and login using the account details you just made.
![Rankd Login Page with details.](/readme_images/appuse3.png)

This should take you to the Spotify login page. Login to Spotify using your Spotify account details and agree to give the app permissions to some of your data.
![Spotify Login Page.](/readme_images/appuse4.png)
![Spotify Authorization Page.](/readme_images/appuse5.png)

If you linked to the wrong Spotify account you can change this by clicking Profile in the top right. Clicking 'Settings' on the dropdown and then 'Connect to Your Music' and you will be prompted to authorize with Spotify again.

You should then be redirected to the 'Scores' page. If you haven't, click 'Scores' either in the top navigation bar or bottom icons.
![Rankd Score Page empty.](/readme_images/appuse6.png)

On the Scores page, search for music that you listen by inputting your search into the search bar at the top and hitting Enter.
![Rankd Score Page search](/readme_images/appuse7.png)

Here you can give the tracks, albums, and artists that you like ratings to show how much you like them. After inputing your score either hit Enter in the box or click 'Save' on the right. A score can be deleted by hitting the red trash button.
![Rankd Score Page add score.](/readme_images/appuse8.png)
![Rankd Score Page score added.](/readme_images/appuse9.png)

Navigating to the 'Stats' page you can choose how many top items you would like our analysis to search through and then click 'Generate' to generate your analysis.
![Rankd empty Analysis Page.](/readme_images/appuse10.png)

Once your analysis is ready you should see something like this:
![Rankd Analysis Example.](/readme_images/appuse11.png)

If you want to generate a new analysis looking at more or less items you can find the generate button at the bottom of the web page.

To add friends navigate to the 'Friends' page and give your User ID to some of your friends.

You can send friend requests to your friends by putting their User ID in the middle box as seen below and clicking 'Add'.
![Rankd Friends add Friend.](/readme_images/appuse12.png)

To accept a friend request hit the 'Accept' button next to their name, or hit 'Reject' to delete the friend request. Only accepted friends can view each other's scores and stats.
![Rankd Friends accept friend request.](/readme_images/appuse13.png)

Once you have added some of your friends you should see something like this:
![Rankd Friends page with 3 friends.](/readme_images/appuse14.png)

You can now navigate to the Share page and view your scores next to your friend's as well as view their analysis.
![Rankd Share Page share scores tab.](/readme_images/appuse15.png)
![Rankd Share Page share stats page.](/readme_images/appuse16.png)
