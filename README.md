# AudysseyProcessor

## Summary
AudysseyProcessor is a python script to be used in conjunction with the Audyssey MultEQ app for Android (and possibly other OSes). It allows to set EQ correction curves based on precise frequency and gain information rather than forcing the user to draw it by hand on a touchscreen. This allows for better comparison of different speakers, placements and EQ curves.

The following data can be edited automatically:
* Custom EQ curve as a list of points. Each point has a Frequency in Hz and a level in dB.
* Crossover frequency in Hz. If one is given, the speaker will automatically be set to "Small".
* Midrange Compensation Yes/No
* Speaker level in dB
* Correction range in Hz: This feature is implemented correctly with respect to the JSON file, but requires at least version 1.6.0 of Audyssey MultEQ to work. The last confirmed previous version 1.5.2 uses it during neither im- nor export. 
* Trim Adjustment: This defines the intensity of the correction. 0 is the default value, it is unknown yet what this does.

## Technical Details
MultEQ stores its data in a JSON file. The script reads this file, changes the content based on a list of replacements to make, then stores it back into a new JSON file with a new preset name. It also adds tabs for readability.

## Usage
AudysseyProcessor().py --input_file=<inputPath> --output_file=<outputPath> \[--rewrite_only\] \[--remove_noncustom\]

* inputPath: The full absolute or relative path to the input file. It will not be modified.
* outputPath: The full absolute or relative path to the output file. If the path does not exist, it will be created.
* rewrite_only: Read, add whitespaces for readability and write, but do not change any values. Useful for debugging or just to gain insight.
* remove_noncustom: Removes all channels that are not explicitly defined in the script. Useful to quickly disable speakers while retaining the configuration.

## Known Issues
No error checking is performed.

## TODO
* optional argument: disable tabs