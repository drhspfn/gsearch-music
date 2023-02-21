# gsearch-music

## General information
 ### There may be some inaccuracies in the script, but the basic idea will be clear
 
 ###### The basic functionality is in `api.py`. There the principle of operation is also described
 ###### For the job you need: `googlesearch BeautifulSoup pafy` 
 ###### Average parsing time per page, ~ 0.3 sec.
 ###### If you search for the host `youtube.com` it downloads audio from YouTube. (This function can be disabled by querying `api.searchmusic(qu:str)`)
 
 ###### In `tg.py` there is a simple variant of integration with Telegram (using `aiogram`)
