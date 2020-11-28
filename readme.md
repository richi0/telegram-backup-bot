# Telegram backup bot

## Features
- Send files to the bot from your device
- Files are saved on the server and meta data are stored in a database
- Query files by sending query strings
- Request files and the bot will responde them back to you


## Detail description
- Protection
    - User has to send a password to get permission for his files
- Send data
    - If a user sends a image, video or audio file the file will be saved into the data folder with a unique.
    - The original name is saved in the database together with the time recived, the time created, the file type, the file size
- Query files
    - A user can search for files by sending a query string. He can filter for files containing a string
    - Are created on a specific date is older or younger than a specific date
- Request files
    - The query respones contains previews and id's for every file. You can request the original files by sending a id or a list of ids to the bot.
- Every message
    - Every message will be connectet with a user. If a message arrives the database will be checked if the sender already exist.
    - If not a new user will be created.
    - If the usere ever loggs in successfully he will be marked as logged in.
    - The user object will be send to every handler callback


- search
    - name
    - date
        - exact => 2020-03-03
        - range => 2020-03-03/2020-05-01
    - type
        - video
        - audio
        - document
        - photo
    - user
    - extension
