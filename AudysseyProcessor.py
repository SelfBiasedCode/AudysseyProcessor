"""AudysseyProcessor

Usage:
  AudysseyProcessor.py --inputFile=<inputPath> --outputFile=<outputPath>

Options:
  --inputFile=<inputPath>   The path to the input file to be processed. Will not be modified.
  --outputFile=<outputPath> The path to the processed output file. Path will be created if necessary.
  -h --help     Show this screen.
  --version     Show version.

"""

import json
from datetime import datetime
from os import path, makedirs

from docopt import docopt


class AudysseyProcessor:
    class ChannelInfo:
        def __init__(self, crossover=None, level=None, corrections=None, midrange_comp=None, correction_limit=None):
            self.crossover = crossover
            self.level = level
            self.corrections = corrections
            self.midrange_comp = midrange_comp
            self.correction_limit = correction_limit

    @staticmethod
    def create_channel_data():
        channels = {}

        # insert channel data here
        corrections_front = ["{20.0, 9.5}", "{150.0, -1.0}", "{500.0, 0.0}", "{2500.0, -5.0}", "{3600.0, -2.0}",
                             "{6200.0, -3.0}", "{11000.0, 0.0}", "{15000.0, -2.0}"]

        corrections_center = ["{20.0, 0.0}", "{100.0, 0.0}", "{170.0, -0.5}", "{295.0, 1.5}",
                              "{570.0, -4.0}", "{2040.0, -4.0}", "{3565.00, -3.5}", "{6725.0, -7.0}",
                              "{10850.0, 0.0}", "{15485.0, -3.5}"]

        corrections_rear = ["{20.0, 0.0}", "{100.0, 5.0}", "{200.0, 2.0}", "{400.0, 0.0}", "{650.0, 0.5}",
                            "{1500.0, -0.5}", "{4000.0, 0.0}", "{7000.0, -4.0}", "{12000.0, -0.5}", "{20000.0, 0.0}"]

        # channel assembly
        channels["FL"] = AudysseyProcessor.ChannelInfo(crossover=80, midrange_comp=False,
                                                       corrections=corrections_front, correction_limit=1000)
        channels["FR"] = AudysseyProcessor.ChannelInfo(crossover=80, midrange_comp=False,
                                                       corrections=corrections_front, correction_limit=1000)
        channels["C"] = AudysseyProcessor.ChannelInfo(crossover=80,
                                                      corrections=corrections_center, correction_limit=1000)
        channels["SRA"] = AudysseyProcessor.ChannelInfo(crossover=80,
                                                        corrections=corrections_rear, correction_limit=20000)
        channels["SLA"] = AudysseyProcessor.ChannelInfo(crossover=80,
                                                        corrections=corrections_rear, correction_limit=20000)
        channels["SW1"] = AudysseyProcessor.ChannelInfo(level=3.0)

        return channels

    def run(self, input_file_path, output_file_path):
        start_time = datetime.now()

        # extract input filename for printing
        input_file_name = path.splitext(path.basename(input_file_path))[0]

        # extract output filename and path
        output_file_name = path.splitext(path.basename(output_file_path))[0]
        output_dir_path = path.dirname(output_file_path)

        # recursively create output path if required
        makedirs(output_dir_path, exist_ok=True)

        # inform user
        print("Replacing values from {0} and writing a formatted version to {1}...".format(input_file_name,
                                                                                           output_file_name))

        mod_channels = self.create_channel_data()

        # read
        with open(input_file_path) as infile:
            data = json.load(infile)

        # process
        data["title"] = output_file_name
        for input_channel in data["detectedChannels"]:
            channel_id = input_channel["commandId"]
            if channel_id in mod_channels:
                mod_data = mod_channels[channel_id]

                if mod_data.corrections is not None:
                    input_channel["customTargetCurvePoints"] = mod_data.corrections

                if mod_data.level is not None:
                    input_channel["customLevel"] = str(mod_data.level)

                if mod_data.crossover is not None:
                    input_channel["customCrossover"] = str(mod_data.crossover)
                    input_channel["customSpeakerType"] = 'S'

                if mod_data.midrange_comp is not None:
                    input_channel["midrangeCompensation"] = str(mod_data.midrange_comp)

                if mod_data.correction_limit is not None:
                    input_channel["frequencyRangeRolloff"] = "%.1f" % mod_data.correction_limit
        # write
        with open(output_file_path, "w+") as output:
            json.dump(obj=data, fp=output, indent='\t')

        # inform user
        end_time = datetime.now()
        print("Finished processing in {0:.2f} s.".format((end_time - start_time).total_seconds()))


def get_args():
    arguments = docopt(__doc__)
    input_file = arguments["--inputFile"]
    output_file = arguments["--outputFile"]
    return input_file, output_file


if __name__ == '__main__':
    instance = AudysseyProcessor()
    args = get_args()
    instance.run(input_file_path=args[0], output_file_path=args[1])
