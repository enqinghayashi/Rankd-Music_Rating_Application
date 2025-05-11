# cits3403-group-5-2025-S1

## Description
Describe the purpose of this app/website.

## Requirements
- Access to a Spotify Premium account.
  - A Spotify Premium account is required to make an app with the SpotifyAPI.
  - If you do not have a Spotify Premium account but do have a free account and know of someone who does have a premium account, you can ask them to create the Spotify app and add you as a user and you will still be able to use this application.
  - In the submitted copy of this application a Spotify Premium account made with a 3 month free trial is provided soley for the purpose of testing this project, please refer to login_details.md for more information.

## Installing Packages
...

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
![Spotify for Developers home page.](/readme_images/appsetup5.png)

Click the button that says 'Create app'. You should see the following:
![Spotify for Developers home page.](/readme_images/appsetup6.png)

Now fill in the 'App name', 'App description' with anything you see fit. Under 'Redirect URIs' fill in the address 'http://127.0.0.1:5000/auth' and click the 'Add' button. This redirect uri is essential for the app to work, this is where Spotify redirects you to after you succeed or fail authorization.
![Spotify for Developers home page.](/readme_images/appsetup7.png)

(NOTE: The port number 5000 can be changed if you are running the flask app on a different port. THE PORT NUMBER MUST BE THE SAME AS THE ONE THAT YOU ARE RUNNING THE FLASK APP ON. If you are running the app on a different port you will also have to change the `redirect_uri` in auth.py which we will detail later. YOU MAY NOT CHANGE THE '/auth' AT THE END OF THE REDIRECT URI, ONLY THE PORT IS ABLE TO BE CHANGED.)

We will also need to check the 'Web API' box and agree to the terms of use.

Once everything has been filled in it should look something like this:
![Spotify for Developers home page.](/readme_images/appsetup8.png)

Hit 'Save' and you should see a page that looks like this:
![Spotify for Developers home page.](/readme_images/appsetup9.png)

### Adding the Client ID to the Flask App
Copy the Client ID from the page you are now on and navigate to /app/auth.py.
![Spotify for Developers home page.](/readme_images/appsetup10.png)

Inside the quotation marks of `self.client_id` place the Client ID you copied earlier and save the file.

(NOTE: If you changed the port of the redirect uri earlier you will also have to change it under `self.redirect_uri`).

The Flask App will now be linked to your Spotify API app.

### (Optional) Adding Other Users to Your Spotify API App
Return the top App information page as shown below:
![Spotify for Developers home page.](/readme_images/appsetup9.png)

Above 'Client ID' click 'User Management' and you should see something like this:
![Spotify for Developers home page.](/readme_images/adduser0.png)

Enter the full name and email of the Spotify account that you wish to allow access to the Spotify API app and hit 'Add user'. You should see something like this:
![Spotify for Developers home page.](/readme_images/adduser1.png)

### (Optional) Removing Other Users from your Spotify API App
To remove a user from your Spotify API app simly return to the user management page and click the three dots to the right of the user you wish to remove, then click 'Remove user'.
![Spotify for Developers home page.](/readme_images/removeuser0.png)

## Using the Flask App
...