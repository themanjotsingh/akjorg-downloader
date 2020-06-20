import os.path
from tqdm import tqdm
import urllib.request
from urllib.request import urlopen
import requests
import easygui as g
from bs4 import BeautifulSoup
import sys
import webbrowser  



print ("Please follow the on screen prompts.")

buttonbox_choices = ["continue", "go to akj.org kirtan site", "check out this project on github.com"]

buttonbox = g.buttonbox(msg="Vaheguru Jee Kaa Khalsa Vaheguru Jee Kee Fateh \n" "This downloader will download Kirtan from AKJ.org website in bunk for offline listening. \n" "To use, go to the Kirtan section of AKJ.org, filter and search by country, location, year, month, kirtani as needed. Hit search. Copy the url from the url addres bar. \n"  "This downloader will present to you all the tracks from the url and you can choose which to download.", title="Kirtan Downloader", choices=buttonbox_choices, default_choice="continue")

if buttonbox == "go to akj.org kirtan site":
    webbrowser.open("https://www.akj.org/keertan.php", new=2, autoraise=True)
    
elif buttonbox == "check out this project on github.com":
        webbrowser.open("https://github.com/themanjotsingh/akjorg-downloader", new=2, autoraise=True)


akj_link = g.enterbox("Please copy and paste the url as specified in the instructions:", "Kirtan Downloader")


if "akj.org/keertan.php" not in akj_link:
    g.msgbox ("You have entered an invalid url. Please try again.")
    akj_link = g.enterbox("Please copy and paste the url as specified in the instructions:", "Kirtan Downloader")
    if "akj.org/keertan.php" not in akj_link:
        g.msgbox ("Too many bad attempts. Script will now close.")
        sys.exit()
              
#    elif "akj.org/keertan.php" in akj_link:
#        continue

#elif "akj.org/keertan.php" in akj_link:
#    continue





parser = 'html.parser'
resp = urllib.request.urlopen(akj_link)
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
ext = "mp3"


g.msgbox ("Please select the folder into which you would like the files to be saved to.", "Kirtan Downloader")

chosen_dir = g.diropenbox()

subfolder_name = chosen_dir

list_to_choose = []

for link in soup.find_all('a', href=True):
    links_list = link['href']
    if ext in links_list:
        list_to_choose.append(links_list)    

playlist_length = (len(chooser_chosen))

if playlist_length > 1:
    file_plur = "files"
if playlist_length == 1:
    file_plur = "file" 

chooser_msg = "Please choose the tracks that you would like to download. Click on individual tracks to select/deselect."
chooser_title = "Kirtan Downloader"
chooser_choices = list_to_choose
chooser_chosen = g.multchoicebox(chooser_msg, chooser_title, chooser_choices)




print(" ")    
print("Now downloading " , playlist_length ,  file_plur)

for url in chooser_chosen:
    site = urlopen(url)
    meta = site.info()

    print(" ")
        
    file_size = int(site.getheader('Content-Length'))
    total_size = file_size
    block_size = 1024
    chunk_size = block_size
        
    file_name = url.split('/')[-1]
    name =  subfolder_name + "/" + file_name
    
    if (os.path.isfile(name)):
        already_size = os.path.getsize(name)

        if already_size == total_size:
            print("The file " + file_name + " already exists. Continueing with next file...")
            continue
        
        elif already_size != total_size:
            print("Wrong fize size detected for " + file_name + ". This is possibly from a previous download attempt and could be a corrupted file. Redownloading...")
            # Streaming, so we can iterate over the response.
            r = requests.get(url, stream=True)
            # Total size in bytes.
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            t=tqdm(total=total_size, unit='iB', unit_scale=True)
            with open (name, mode = 'wb') as f:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            print ("File downloaded: " + file_name)



            
            

        
        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")
                
            
    

    elif not (os.path.exists(name)):
        print("Downloading " + file_name)
        # Streaming, so we can iterate over the response.
        r = requests.get(url, stream=True)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        with open (name, mode = 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()

        print ("File downloaded: " + file_name)

        
        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")
                
                
            
print(" ")
print("Downloading finished.")
        
        
    
g.msgbox (("Downloads complete. Downloader will now close.") , "Kirtan Downloader")


exit()



