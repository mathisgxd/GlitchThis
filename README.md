# GlitchThis

![GlitchThis Logo](logo.png)

A Telegram RAT to control a PC remotely  
  
## How authorizations work  
The first ever user to interact with the bot becomes its owner and has ADVANCED level  
  
Both chats and users have a LEVEL (or tier) and each command has a minimum required level for it to be executed.  
The levels are:  
- UNAUTHORIZED: Set to new chats and users and only permits chat authorization requests  
- BASIC: Enables most of the commands (except advanced ones)  
- ADVANCED: Enables advanced commands  
  
The minimum required level of a command gets confronted to the max between the requester chat level and the requester user level so that a BASIC (or higher) user can even trigger BASIC commands in UNAUTHORIZED chats while an UNAUTHORIZED user can only trigger BASIC commands in BASIC (or higher) chats.  
  
## Available commands 
Windows commands:   
- hide_windows (BASIC): Minimize all windows  
- show_windows (BASIC): Show all hidden windows
- close_window (BASIC): Close the top window
   
Locker commands:  
- lock_mouse (BASIC): Lock the mouse cursor in place
- lock_keyboard (BASIC): Lock the keyboard
  
Shutdown commands:  
- shutdown (BASIC): Shutdown the pc
- reboot (BASIC): Reboot the pc
- logoff (BASIC): Logoff the pc
- hibernate (BASIC): Hibernate the pc
- crash (BASIC): Crash the pc (BSOD)
  
Program commands:  
- notepad (BASIC): Open notepad (with optional text)
- cmd (BASIC): Execute a cmd command
- site (BASIC): Open a url or search in the browser
  
Image commands:  
- screenshot (BASIC): Take a screenshot
- picture (BASIC): Take a picture
  
Other:  
- wifi (BASIC): Get saved wifi profiles
- gte (BASIC): Stands for GlitchThis Executer and can be used to create and save custom scripts that trigger a series of commands (check out GTE for more)
  
## Media handling
When a media is sent to the bot (photo, video, voice or audio) it gets saved locally and its info is stored in the database as a Medium.  
- photo (BASIC)
  - open: Open the image
  - close: Close the image
  - wallpaper: Set as wallpaper
- audio (BASIC)
  - play: Play the audio
  - stop: Stop the audio (if playing)
- voice (BASIC)
  - play: Play the audio
  - stop: Stop the audio (if playing)
- video (BASIC)
  - open: Open the video
  - close: Close the video  

You can also give a name to a medium by writing it as its caption so that you can use it as reference, for example, I can send a photo with the caption "img" and then send the following command: "/photo img, wallpaper" to set it as the wallpaper (don't forget the comma)  
  
## GTE
GTE stands for GlitchThis Executer and can be used to create and save custom scripts that trigger a series of commands. The easiest way to understand it is with an example:  
  
let's say that I send a photo to the bot with the caption "img"  
and an audio with the caption "sound"  
  
then I can create a GTE file called "test" by sending this to the bot:  
```text
/gte test  
wait 3  
photo img, wallpaper  
audio sound, play  
hide_windows  
```  
This, when executed, will:  
- wait for 3 seconds
- set the previously sent "img" photo as the wallpaper
- play the previously sent "sound" audio
- and minimize all windows  
  
  
(More commands and updates coming soon)
