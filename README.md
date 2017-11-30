Thingiverse Exporter
=============

Python2 script that simplifies exporting all your stuff out of Thingiverse.  
It creates a Git-compatible directory with a list and folders. Each folder contains all the files, images and description for each design. 

Also added an option to generate a "Archive Gallery" HTML file for easy viewing and searching.. 

_Disclaimer_
--------
I'm not a python programmer so some googling and stackoverflow searches help me to make script run again.. Hope it helps you! Not associated with Thingiverse, use at your own risk.

Instructions
--------
* _Optional:_ Create an empty Git repository, clone the repo locally
* Download [the python script](thingExport.py) as raw into the created empty directory
* Edit lines 17-19 for user, authorName, and authorDescription
* Install PIP (sudo apt-get install python-pip)
* Install requests (sudo pip install requests)
* Install natsort (sudo pip install natsort)
* Install lxml (sudo pip install lxml)
* Install beautifulsoup4 (sudo pip install beautifulsoup4)
* Run the script from the same directory (python export_things.py)
* _Optional:_ Commit and push the changes into your Git repository

You can **browse the generated directories offline**, by simply using the generated **"ThingList.html"** file.

**New**  

* Combined 3 different scripts into one. Now you can choose what to do.
* Generate "Things Directory" Gallery from all things you archived.

**Features**  

* Select which page to download (desings/liked) (save your liked things too!)
* Files can be downloaded OR linked from the original website to save disk space
* Customize authorship
* Customize the header for the pages
* Select if files will be re-downloaded if already present
* Select if things will be re-processed if the folder is already present (to save time when re-running for long lists)

Credit
--------
* Thanks to everyone who is re-sharing the script
* Thanks to **Derrick Oswald** for writing installation instructions
* Thanks to [**Mark Durbin (MakeALot)**](https://twitter.com/MarkDurbin104) for a bugfix
* Original Author: Carlos Garcia Saura (carlosgs)

--------
<http://fatiher.com/>  

License
--------
Creative Commons - Attribution - Share Alike license.  


