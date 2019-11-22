import requests
import lxml.html as lh
import pandas as pd


url='https://www.berufsstart.de/unternehmen/stadt/frankfurt-top100-unternehmen.php'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('/html/body/div.row/div.col-md-9/div.col-md-12.bshidden/div.row/div@class="col-sm-12')

#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]