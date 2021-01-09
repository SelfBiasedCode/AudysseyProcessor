# AudysseyProcessor

## Summary
AudysseyProcessor is a python script to be used in conjunction with the Audyssey MultEQ app for Android (and possibly other OSes). It allows to set EQ correction curves based on precise frequency and gain information rather than forcing the user to draw it by hand on a touchscreen. This allows for better comparison of different speakers, placements and EQ curves.

The following data can be edited automatically:
* Custom EQ curve as a list of points. Each point has a Frequency in Hz and a level in dB.
* Crossover frequency in Hz. If one is given, the speaker will automatically be set to "Small".
* Midrange Compensation Yes/No
* Speaker level in dB
* Correction range in Hz: This feature is implemented correctly with respect to the JSON file, but requires at least version 1.6.0 of Audyssey MultEQ to work. The last confirmed previous version 1.5.2 uses it during neither im- nor export. 

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