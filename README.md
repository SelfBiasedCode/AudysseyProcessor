# AudysseyProcessor

## Summary
AudysseyProcessor is a python script to be used in conjunction with the Audyssey MultEQ app for Android (and possibly other OSes). It allows to set EQ correction curves based on precise frequency and gain information rather than forcing the user to draw it by hand on a touchscreen. This allows for better comparison of different speakers, placements and EQ curves.

## Technical Details
MultEQ stores its data in a JSON file. The script reads this file, changes the content based on a list of replacements to make, then stores it back into a new JSON file with a new preset name. It also adds tabs for readability.

## Usage
AudysseyProcessor[]().py --inputFile=<inputPath> --outputFile=<outputPath>

* inputPath: The full absolute or relative path to the input file. It will not be modified.
* outputPath: The full absolute or relative path to the output file. If the path does not exist, it will be created.

## Known Issues
No error checking is performed.

## TODO
* optional argument: disable tabs
* add correction cutoff frequency