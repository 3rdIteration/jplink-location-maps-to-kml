# jplink-location-maps-to-kml
 A simple script to filter & convert JPList based location maps (eg: for stores) in to KML that you can use with other mapping tools.
 
 It currently parses all data tags, icons, etc, and maps these to the corresponding KML. (Everything else is currently added to the description, but this is easy to change.)
 
 ## Usage
 Straight Conversion
 
` python convert.py --inputfile "JPList Page.html" --outputfile "Output File.kml"
`

 Only Including items with a specific data tag
 
`python convert.py --inputfile "JPList Page.html" --includeClassData "Tag Data Value to Include" --outputfile "Output File.kml"
` 

 Excluding items with a specific data tag
 
`python convert.py --inputfile "JPList Page.html" --excludeClassData "Tag Data Value to Exclude" --outputfile "Output File.kml"
` 

 ## Requirements:
 SimpleKML library. (Easily installed via PIP)
