import requests, googlesearch
from bs4 import BeautifulSoup
import sys, pafy, os, time
from colorama import init, Fore, Style
init(True)

AUDIO_PATH = "./audio"
ABORT_LINKS = []



class mAPI:
    def __init__(self, defb=False):
        self.debug = True
        self.startTime = 0
        self.EndTime = 0


        ## Creating a session, for the future
        self.req_session = requests.Session()


    async def download(self, link):


        ## Just checking the time it takes to parse
        if self.debug and self.startTime != 0:
            self.EndTime = time.time() - self.startTime
            print(Fore.GREEN + f"[DEBUG] Search Time: {self.EndTime}")
        try:
 

            ## Get the name of the file on the server
            local_filename = link.split('/')[-1]
            print(f"Trying to download: {local_filename}")



            ## Obtaining a file to download
            with requests.get(link, stream=True, timeout=3) as r:

                ## Just for a little progress in the console
                total_length = r.headers.get('content-length')
                dl = 0
                total_length = int(total_length)


                r.raise_for_status()
                filepath = f"{AUDIO_PATH}/{local_filename}"
                
                ## Chunk loading itself, just in case
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=4096): 
                        if chunk: 
                            dl += len(chunk)
                            f.write(chunk)
                            done = int(50 * dl / total_length)
                            sys.stdout.write(Fore.LIGHTCYAN_EX+"\r[%s%s]" % ('=' * done, ' ' * (50-done)))    
                            sys.stdout.flush()


            ## Return the path to the local file
            return filepath
        
        except Exception as err:
            print("\nERROR --> "+Fore.LIGHTRED_EX+f"{err}")
            return 

    async def dlYoutube(self, link):
        ## Just checking the time it takes to parse
        if self.debug and self.startTime != 0:
            self.EndTime = time.time() - self.startTime
            print(Fore.GREEN + f"[DEBUG] Search Time: {self.EndTime}")



        ## Using the "pafy" module to download audio from YouTube
        vid = pafy.new(link)
        ## Getting the best audio streaming options for the link
        audiostreams = vid.audiostreams



        ## I form the download path, and the path with the changed extension for ffmpeg
            ## This adds time to processing. you can also save them as they are (m4a or webm)
        dlpath = "{}/{}.{}" .format(
            AUDIO_PATH,
            audiostreams[0].title,
            audiostreams[0].extension
        )
        new_path = "{}/{}.mp3" .format(
            AUDIO_PATH,
            audiostreams[0].title,
        )

        ## Downloading audio on a specified path
        audiostreams[0].download(dlpath)

        ##Running the 'ffmpeg' command. 
            #№ The file 'ffmpeg.exe' (Win) must be located in the folder with the script
        os.system('ffmpeg -i "{}" -vn -ar 44100 -loglevel quiet -ac 2 -b:a 192k "{}"'.format(
            dlpath,
            new_path
        ))

        ## Deleting an old file with an unsuitable extension 
        os.remove(dlpath)

        ## Return the path to the local file
        return new_path

    async def searchmusic(self, qu:str, logprefix:str="-", skipyt:bool=False):
        ## Start debug...

        if self.debug:
            self.startTime = time.time()


        if await self.isyt(qu):
            ## Checking if the text is a link to YouTube
            print(f"{logprefix} 'qu' is YouTube Link. Downloading....")

            ## If the link is to YouTube, upload it and pass the resulting path to the main script
            audio = await self.dlYoutube(qu)
            return audio



        ## Getting a list of links from a search query using the 'googlesearch' module
            ## Here you can add something, for example, that the chance of getting a link would be higher
        data = googlesearch.search(f"{qu} song download mp3", num=5)
        alink = ""



        ## Cycle through each link from the results
        for x in data:
            try:

                ## This probably skips links that have already been marked as failures
                    ## If everything works correctly, you can write them to a file, and load them at startup.
                if x in ABORT_LINKS:
                    continue

                ## Again check for the YouTube link in the search results
                if await self.isyt(x) and not skipyt:
                    print(f"{logprefix} Downloading from YT: "+Fore.CYAN+f"{x}")

                    ## If the link is to YouTube, upload it and pass the resulting path to the main script
                    audio = await self.dlYoutube(x)
                    return audio
                        


                else:
                    print(f"{logprefix} Searching audios on: "+Fore.BLUE+f"{x}")


                    ## Update User Agent to random
                    self.req_session.headers.update({"User-Headers": googlesearch.get_random_user_agent()})

                    ## Getting the Page Skeleton
                    page =  self.req_session.get(x, timeout=10)

                    ## Passing skeleton to bs4 for element parsing
                    soup = BeautifulSoup(page.content, "html.parser")


                    """
                        Search on the page for all elements with <a> tag - Link
                    
                        Checking each of them for a pointing file, 
                            if .mp3 save a link to pass to the downloader
                    """
                    linkstest = soup.find_all("a")
                    for xlink in linkstest:
                        if xlink.find(".mp3") != -1:
                            alink = xlink.href



                    ## If there are no direct links
                    if not alink:

                        ## Get all elements with <audio> tag - Audio widget, 
                            ## can be seen quite often on websites

                        el = soup.find_all("audio")
                        if el:
                            for element in el:
                                try:

                                    ## Get the link the widget refers to
                                    link = element.find("source")['src']
                                except AttributeError:

                                    """
                                        I don’t remember why I left the already existing check, 

                                        P.S #1. in the end I didn’t make sure it was necessary
                                    
                                        P.S #2. I remembered that sometimes the link in the Widget 
                                            was stored in a separate tag
                                    """
                                    link = element.find("a").text

                                except TypeError:
                                    """
                                        If nothing helps, the link is skipped. 
                                        You can add here methods from non-working links I have
                                    """

                                    break


                                
                                """
                                    In my case, there were often "bitten" links, 
                                    and they could not be opened. My attempt to "cure" them, 
                                    in these cases, helped. 
                                        More precisely, there was no site protocol
                                
                                
                                    p.s I will try to describe
                                """

                                ## Splitting a Link into Components
                                ldata = link.split("/")

                                ## If the protocol is missing first in the link
                                if ldata[0].find("http") == -1:
                                    for itm in ldata:
                                        if itm == "":

                                            ## Removing empty cells that remain from '//'
                                            ldata.remove(itm)

                                        ## Probably, here I found out the location of the main domain
                                            ## Sorry, I'm really not sure what I was doing here)))
                                        if itm.find(".") != -1:

                                            ## Removing the element that was wrong in order to replace it with a good one
                                            ldata.remove(itm)

                                            """
                                                There may be a problem with some of the nonworking link options here.
                                            """

                                            ## Create the first element in the list with a protocol
                                            ldata[0] = f"https://{itm}"
                                            
                                            ## Merging into an empty link
                                            link = '/'.join(ldata)
                                            break


                                ## Checking for certain parameters passed to the site that interfere with the downloader
                                checke = link.split("?")
                                if len(checke):
                                    link = checke[0]


                                ## Passing the link to the loader
                                dl = await self.download(link)
                                if dl:
                                    return dl
                                else:
                                    print(f"{logprefix} Error on: "+Fore.LIGHTRED_EX+f"{x}"+". Next...")
                                    ABORT_LINKS.append(x)
                                    break
                    else:

                        ##
                        dl = self.download(link)
                        if dl:
                            return dl
                        else:
                            print(f"{logprefix} Error on: "+Fore.LIGHTRED_EX+f"{x}"+". Next...")
                            ABORT_LINKS.append(x)
                            break

            except requests.exceptions.ReadTimeout:
                print(f"{logprefix} Error on: "+Fore.LIGHTRED_EX+f"{x}"+". Next...")
                ABORT_LINKS.append(x)
                break

            except requests.exceptions.ConnectTimeout:
                print(f"{logprefix} Error on: "+Fore.LIGHTRED_EX+f"{x}"+". Next...")
                ABORT_LINKS.append(x)
                break


        print(f"{logprefix} Not founded.....")
        return
    


    ## The most common and simple check for a YouTube link
    async def isyt(self, text):
        if text.find("youtube.com") != -1 or \
            text.find("youtu.be") != -1:
            return True
        
        return False


