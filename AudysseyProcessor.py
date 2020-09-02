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
from docopt import docopt

from os import path


class AudysseyProcessor:
    class ChannelInfo:
        def __init__(self, crossover=None, level=None, corrections=None, midrangeComp=None):
            self.crossover = crossover
            self.level = level
            self.corrections = corrections
            self.midrangeComp = midrangeComp

    def createChannelData(self):
        channels = {}

        # insert channel data here
        correctionsFront = ["{20.0, 9.5}", "{150.0, -1.0}", "{500.0, 0.0}", "{2500.0, -5.0}", "{3600.0, -2.0}",
                            "{6200.0, -3.0}", "{11000.0, 0.0}", "{15000.0, -2.0}"]

        correctionsCenter = ["{20.0, 0.0}", "{100.0, 0.0}", "{170.0, -0.5}", "{295.0, 1.5}",
                             "{570.0, -4.0}", "{2040.0, -4.0}", "{3565.00, -3.5}", "{6725.0, -7.0}",
                             "{10850.0, 0.0}", "{15485.0, -3.5}"]

        correctionsRear = ["{20.0, 0.0}", "{100.0, 5.0}", "{200.0, 2.0}", "{400.0, 0.0}", "{650.0, 0.5}",
                           "{1500.0, -0.5}", "{4000.0, 0.0}", "{7000.0, -4.0}", "{12000.0, -0.5}", "{20000.0, 0.0}"]

        correctionsSL = ["{20.0, 0.0}", "{100.0, 5.0}", "{250.0, -2.5}", "{650.0, -2.0}",
                         "{1000.0, -3.0}", "{4000.0, 0.0}", "{7000.0, -4.0}", "{12000.0, -0.5}", "{20000.0, 0.0}"]

        # channel assembly
        channels["FL"] = AudysseyProcessor.ChannelInfo(crossover=80, midrangeComp=False, corrections=correctionsFront)
        channels["FR"] = AudysseyProcessor.ChannelInfo(crossover=80, midrangeComp=False, corrections=correctionsFront)
        channels["C"] = AudysseyProcessor.ChannelInfo(crossover=80, corrections=correctionsCenter)
        channels["SRA"] = AudysseyProcessor.ChannelInfo(crossover=80, corrections=correctionsRear)
        channels["SLA"] = AudysseyProcessor.ChannelInfo(crossover=80, corrections=correctionsRear)
        channels["SW1"] = AudysseyProcessor.ChannelInfo(level=3.0)

        return channels

    def run(self, inputFile, outputFileName):
        inputPath = path.dirname(inputFile)
        outputFile = path.join(inputPath, outputFileName + ".ady")

        modChannels = self.createChannelData()

        # read
        with open(inputFile) as input:
            data = json.load(input)

        # process
        data["title"] = outputFileName
        for inputChannel in data["detectedChannels"]:
            channelId = inputChannel["commandId"]
            if channelId in modChannels:
                modData = modChannels[channelId]

                if modData.corrections is not None:
                    inputChannel["customTargetCurvePoints"] = modData.corrections

                if modData.level is not None:
                    inputChannel["customLevel"] = str(modData.level)

                if modData.crossover is not None:
                    inputChannel["customCrossover"] = str(modData.crossover)
                    inputChannel["customSpeakerType"] = 'S'

                if modData.midrangeComp is not None:
                    inputChannel["midrangeCompensation"] = str(modData.midrangeComp)

        # write
        with open(outputFile, "w+") as output:
            json.dump(obj=data, fp=output, indent='\t')


def get_args():
    arguments = docopt(__doc__)
    input_file = arguments["inputPath"]
    output_file = arguments["outputPath"]
    return (input_file, output_file)


if __name__ == '__main__':
    instance = AudysseyProcessor()
    args = get_args()
    instance.run(inputFile=args[0], outputFileName=args[1])
