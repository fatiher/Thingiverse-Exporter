_FORK Disclaimer_ : Just fixed the original script written by Carlos Garcia Saura (carlosgs) to work with BeautifulSoup4 and done some minor changes. I'm not a python programmer so some googling and stackoverflow searches help me to make script run again..

Know bugs : When script reaches to the end page it does not stop. Just leaching same last page over and over.

Thingiverse Exporter
=============

Script that simplifies exporting all your stuff out of Thingiverse  
It creates a Git-compatible directory with a list and folders. Each folder contains all the files, images and description for each design.  


Example of the result: <https://github.com/carlosgs/carlosgs-designs>  


Disclaimer
--------
Not associated with Thingiverse, use at your own risk  

Instructions
--------
* _Optional:_ Create an empty Git repository, clone the repo locally
* Download [the python script](export_things.py) as raw into the created empty directory
* Edit lines 17-19 for user, authorName, and authorDescription
* Install PIP (sudo apt-get install python-pip)
* Install requests (sudo pip install requests)
* Install lxml (sudo pip install lxml)
* Install beautifulsoup4 (sudo pip install beautifulsoup4)
* Run the script from the same directory (python export_things.py)
* _Optional:_ Commit and push the changes into your Git repository

You can also **browse the generated directories offline**, by simply using a **Markdown viewer** (i.e. [MarkdownPreview](https://chrome.google.com/webstore/detail/markdown-preview/jmchmkecamhbiokiopfpnfgbidieafmd?hl=en) for Chrome)  

**New**  
* Added [another script](export_one_thing.py) that allows fetching a single design. Run as:
<pre>export_one_thing.py thingID</pre>
* It will create a directory with the title of the design and all the necessary files.

**Features**  
* Select which page to download (save your liked things too!)
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


