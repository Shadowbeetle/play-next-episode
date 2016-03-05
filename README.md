This little script will play your favorite series episode after episode using vlc media player.

**depends on pymsgbox**

# Setup

Place the script files wherever you want. Create a file named 'setup.yml' in the script's directory and make sure you have a link to the setup file in a convenient place. 

## Necessary fields

**name**: The name of the series

**path**: Absolute path where you store your series

and done. The script can find your series in most of the cases. Let's assume you have a folder in /home/your-user/series
where you have all your series by seasons. You are watching a series named "Fairytales of Phnom Penh", now it doesn't matter
if you have the first season as /home/your-user/series/wtf.fairytales.of.phnom.penh.s1.720p.HDTV or if you have each episode in a 
different folder the script will find it, and log which episodes have been played in the setup file.

You can use vlc's next button to jump to the next episode as well if each episode in a season is in the same folder.

## Other  fields

These can be omitted completely

**audio_language**: the language you wish to play the movie in

**sub_language**: if you wish to watch the movie with subtitles

both of them use the 2 letters abbreviations such as 'en', 'es', 'de' 'fr', 'hu', 'hr'. If none of them is specified, vlc's
default settings are applied. External subtitle files are not taken into account by the script!

## Controlling what to play next

**next_episode**: you can specify the number of the next episode, if you have your series organized by episodes

**exclude**: these folders will be omitted while searching for the next episode

If you have each episode in different folder, you will need to add those you have already watched to "exclude". If you have them organized by seasons, the seasons you have already watched are listed here.

# Contributions

All contributions are welcome. If you are a Windows user and would like to add a bat or cmd file to make calling the script
easier, go ahead and create a pull request!
