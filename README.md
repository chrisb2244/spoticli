Original README (github.com/cgbystrom/spotify-local-http-api):
A simple Python client that describes how to interact with the local, built-in HTTP server inside the Spotify player.

For more information, see my [blog post](http://cgbystrom.com/articles/deconstructing-spotifys-builtin-http-server/) describing more details.

Updated README (github.com/richraid21/spoticli):
To see what needed to be updated, check out my [blog post](http://blog.richdillon.me/how-spotify-changed-their-local-api/) explaining what happened. 

Python (or I) seems to have problems understanding SSL and the certicates. In order to make the project work, I had to disable certificate verification.

While not the end of the world, it results in constant error messages. 

Additional fork (github.com/chrisb2244/spoticli):
Have added command line parsing.

Call with '$ python spoticli.py --pause|--unpause|--skip_forward|--skip_back|--play=<spotify uri>'
The 'skip_forward' and 'skip_back' functions are not yet implemented.

Offlein added a --playpause toggle feature which has been merged
