from api import mAPI

api = mAPI()


 
"""
    If you are not going to use asynchronously, remove the 'async' prefix before the functions in 'api.py'

    
    'api.searchmusic()' returns a string with the path to the saved file
    Accepts parameters:
        # qu:str -> Search request
        # logprefix:str - > Just a string with a prefix to output the information to the console
        # skipyt:bool - > Skipping links to YouTube, only if they fall out in the search query, direct links atk same response

        
    By default, the path for audio is set to the 'AUDIO_PATH' variable in the 'api.py' file        

    The resulting path you can use according to your needs. 
        You can, as in the example, implement a bot to search for audio for TG or something else    
    
        

    p.s. There will probably be a lot of errors in my code. I'm very new to this, don't beat up.

            ^_^
            Perhaps someone else has thought about this and it might be a trigger for you
"""


def main():
    try:
        while True:
            name = input("Search query: ")
            data = api.searchmusic(name)
            print(data)

    except KeyboardInterrupt:
        print("\n\nbye")


if __name__ =="__main__":
    main()
