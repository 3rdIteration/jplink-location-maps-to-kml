# jplink-location-maps-to-kml
 A simple script to filter & convert JPList based location maps (eg: for stores) in to KML that you can use with other mapping tools.
 
 It currently parses all data tags, icons, etc, but is only using the name and location in terms of output to KML. (Though it is trivial to add additional data to the KML )
 
 ## Usage
 Straight Conversion
 
` python convert.py --inputfile "JPList Page.html" --outputfile "Output File.kml"
`

 Only Including items with a specific data tag
 
`python convert.py --inputfile "JPList Page.html" --includeClassData "Tag Data Value to Include" --outputfile "Output File.kml"
` 
 ## Requirements:
 SimpleKML library. (Easily installed via PIP)
