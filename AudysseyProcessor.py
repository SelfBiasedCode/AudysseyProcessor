"""AudysseyProcessor

Usage:
  AudysseyProcessor.py --input_file=<inputPath> --output_file=<outputPath> [--rewrite_only] [--remove_noncustom]

Options:
  --input_file=<inputPath>   The path to the input file to be processed. Will not be modified.
  --output_File=<outputPath> The path to the processed output file. Path will be created if necessary.
  --rewrite_only  Read, add whitespaces for readability and write, but do not change any values.
  --remove_noncustom  Remove all channels that are not explicitly listed in this script.
  -h --help     Show this screen.
  --version     Show version.

"""

import json
from datetime import datetime
from os import path, makedirs

from docopt import docopt


class AudysseyProcessor:
    class ChannelInfo:
        def __init__(self, crossover_hz: int = None, level_db: float = None,
                     corrections_list=None,
                     midrange_comp: bool = None, correction_limit_hz: int = None):
            self.crossover_hz = crossover_hz
            self.level_db = level_db
            self.corrections_list = corrections_list
            self.midrange_comp = midrange_comp
            self.correction_limit_hz = correction_limit_hz

    @staticmethod
    def create_channel_data():
        channels = {}

        # insert channel data here
        corrections_front = ["{20.0, 10.0}", "{50.0, 8.0}", "{100.0, 3.0}",  # low end
                             "{250.0, 2.0}",  # warmth
                             "{450.0, 0.0}", "{600.0, 1.0}", "{800.0, 0.0}",  # mids
                             "{2000.0, -3.0}", "{5000.0, 0.0}",  # sharpness
                             "{18000.0, -2.0}"  # high end
                             ]

        corrections_center = ["{20.0, 0.0}", "{100.0, 0.0}", "{170.0, -0.5}", "{570.0, -2.0}", "{1500.0, 0.0}",
                              "{3565.00, -3.0}", "{6000.00, -1.0}", "{18000.0, -2.0}"]

        corrections_rear = ["{20.0, 10.0}", "{50.0, 7.0}", "{100.0, 5.0}",  # low end
                            "{170.0, 5}", "{250.0, 5}", "{315.0, 2}",  # warmth
                            "{450.0, -4.0}", "{600.0, -5.0}",  # mids
                            "{1000.0, -7.0}", "{2500.0, -7.0}",  # radio
                            "{5000.0, -1.5}",  # sharpness
                            "{18000.0, -2.0}"  # high end
                            ]

        # channel assembly
        channels["FL"] = AudysseyProcessor.ChannelInfo(crossover_hz=80, midrange_comp=False,
                                                       corrections_list=corrections_front, correction_limit_hz=2000)
        channels["FR"] = AudysseyProcessor.ChannelInfo(crossover_hz=80, midrange_comp=False,
                                                       corrections_list=corrections_front, correction_limit_hz=2000)
        channels["C"] = AudysseyProcessor.ChannelInfo(crossover_hz=80,
                                                      corrections_list=corrections_center, correction_limit_hz=20000)
        channels["SRA"] = AudysseyProcessor.ChannelInfo(crossover_hz=90, midrange_comp=False,
                                                        corrections_list=corrections_rear, correction_limit_hz=20000)
        channels["SLA"] = AudysseyProcessor.ChannelInfo(crossover_hz=90, midrange_comp=False,
                                                        corrections_list=corrections_rear, correction_limit_hz=20000)
        # channels["SW1"] = AudysseyProcessor.ChannelInfo(level_db=2.5)

        return channels

    def run(self, input_file_path: str, output_file_path: str, rewrite_only: bool, remove_noncustom: bool):
        start_time = datetime.now()

        # extract input filename for printing
        input_file_name = path.splitext(path.basename(input_file_path))[0]

        # extract output filename and path
        output_file_name = path.splitext(path.basename(output_file_path))[0]
        output_dir_path = path.dirname(output_file_path)

        # recursively create output path if required
        makedirs(output_dir_path, exist_ok=True)

        # inform user
        print(f"Replacing values from {input_file_name} and writing a formatted version to {output_file_name}...")

        mod_channels = self.create_channel_data()

        # read
        with open(input_file_path) as infile:
            data = json.load(infile)

        # process
        if not rewrite_only:
            data["title"] = output_file_name
            # filter list if required
            if remove_noncustom:
                data["detectedChannels"][:] = [channel for channel in data["detectedChannels"]
                                               if channel["commandId"] in mod_channels]
            for input_channel in data["detectedChannels"]:
                channel_id = input_channel["commandId"]
                if channel_id in mod_channels:
                    mod_data = mod_channels[channel_id]

                    if mod_data.corrections_list is not None:
                        input_channel["customTargetCurvePoints"] = mod_data.corrections_list

                    if mod_data.level_db is not None:
                        input_channel["customLevel"] = str(mod_data.level_db)

                    if mod_data.crossover_hz is not None:
                        input_channel["customCrossover"] = str(mod_data.crossover_hz)
                        input_channel["customSpeakerType"] = 'S'

                    if mod_data.midrange_comp is not None:
                        input_channel["midrangeCompensation"] = str(mod_data.midrange_comp)

                    if mod_data.correction_limit_hz is not None:
                        input_channel["frequencyRangeRolloff"] = "%.1f" % mod_data.correction_limit_hz
        # write
        with open(output_file_path, "w+") as output:
            json.dump(obj=data, fp=output, indent='\t')

        # inform user
        end_time = datetime.now()
        print("Finished processing in {0:.2f} s.".format((end_time - start_time).total_seconds()))


def get_args():
    arguments = docopt(__doc__)
    input_file = arguments["--input_file"]
    output_file = arguments["--output_file"]
    rewrite_only = arguments["--rewrite_only"]
    remove_noncustom = arguments["--remove_noncustom"]
    return input_file, output_file, rewrite_only, remove_noncustom


if __name__ == '__main__':
    instance = AudysseyProcessor()
    input_file, output_file, rewrite_only, remove_noncustom = get_args()
    instance.run(input_file_path=input_file, output_file_path=output_file, rewrite_only=rewrite_only,
                 remove_noncustom=remove_noncustom)
