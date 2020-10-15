# convert.py
# 2020 - Stephen Rothery

import sys, argparse, simplekml, html

__version__ =  "0.1"

if __name__ == "__main__":
    print("Starting JPLink Location Data Conversion", __version__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputfile",
                        help="The file that contains a the main HTML file containing the locator map data")
    parser.add_argument("--outputfile",
                        help="The file that will contain the KML data")
    parser.add_argument("--includeClassData",
                        help="Include points which contain this string in the any of the data attributes")
    parser.add_argument("--excludeClassData",
                        help="Ex points which contain this string in the any of the data attributes")

    args = parser.parse_args()

    if not args.inputfile:
        sys.exit("Please specify an input file...")

    try:
        kmlfile = simplekml.Kml()
        with open(args.inputfile) as jplink_data:

            # A few variables to keep track of the file as we parse it
            storeData = False
            lastLine = ""
            skipLines = 0

            # Blank varibles for a location
            pointLocation = []
            pointIcon = ""
            pointData = []
            pointDescription = ""

            # File Parser
            for line in jplink_data:
                # Clean up the input a bit
                line = line.strip()
                line = html.unescape(line)

                # Skip blank lines
                if len(line) == 0:
                    continue

                # Skip blocks of lines
                if skipLines > 0:
                    skipLines -= 1
                    continue

                # What do do when we arrive at the start of a new location
                if "<!-- store -->" in line:
                    storeData = True

                    # Check to see if this is the very first location
                    if len(pointData) > 0:
                        include = True

                        # Iterate through the data tags and record any that we want to include in the KML file
                        for itemName, itemValue in pointData:
                            if 'title' in itemName:
                                pointName = itemValue
                            else:
                                pointDescription = pointDescription + " " + itemValue + "<br>"


                        # Check to see if we are filtering based on the data tag values
                        if args.includeClassData:
                            include = False
                            for itemName, itemValue in pointData:
                                if args.includeClassData in itemValue:
                                    include = True

                        if args.excludeClassData:
                            include = True
                            for itemName, itemValue in pointData:
                                if args.excludeClassData in itemValue:
                                    include = False

                        # Include the location in the KML file if required
                        if include:
                                # MODIFY HERE TO ADD YOUR OWN DATA TAGS TO KML
                                point = kmlfile.newpoint(name = pointName,
                                                         coords = [(pointLocation_long, pointLocation_lat)],
                                                         description = pointDescription)
                                point.iconstyle.icon.href = pointIcon

                    # Clear the location data, ready fo the next location
                    pointName = ""
                    pointLocation = []
                    pointIcon = ""
                    pointData = []
                    pointDescription = ""
                    continue

                # Parse through the data
                if "</div>" in line and "</div>" in lastLine:
                    storeData = False
                    continue
                lastLine = line

                if "<!-- directions -->" in line:
                    skipLines = 7
                    continue

                if "<div" in line or "</div" in line:
                    continue

                # Processing Lines
                if storeData:

                    if "data-latitude" in line:
                        data_latitude = line.split("=")
                        pointLocation_lat = float(data_latitude[1].strip('"'))
                        continue

                    if "data-longitude=" in line:
                        data_longitude = line.split("=")
                        pointLocation_long = float(data_longitude[1].strip('">'))
                        pointLocation = tuple(pointLocation)
                        continue

                    #Items that can work with one split.
                    splitLine = line.split(" ",1)

                    try:
                        if "data-marker-icon" in splitLine[1]:
                            pointIcon = splitLine[1].split("=")[1][:-6].strip("'")
                            continue

                        if "data-type=" in splitLine[1]:
                            if "<p hidden>" in splitLine[1]:
                                splitLine = splitLine[1].split('"><p hidden>', 1)
                                dataName = splitLine[0].split('"')[1]
                                dataValue = splitLine[1].split("<")[0]
                                pointData.append((dataName, dataValue))
                                continue

                            splitLine = splitLine[1].split('">', 1)
                            dataName = splitLine[0].split('"')[1]
                            dataValue = splitLine[1].split("<")[0]
                            pointData.append((dataName, dataValue))
                            continue

                        # Items that can work with two splits.
                        splitLine = splitLine[1].split(" ",1)
                        dataName = splitLine[0].split("=")[1].strip('"')
                        dataValue = splitLine[1].split(">")[1].split('<')[0]
                        pointData.append((dataName,dataValue))
                        continue

                    except IndexError:
                        pass
                        print("Ignoring Line:", line)

        # Output the KML once everything is done
        kmlfile.save(args.outputfile)

    except IOError:
        print("File:", args.inputfile, "Not Found")