import os
import subprocess
from natsort import natsorted
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('reference')
    parser.add_argument('incorrect')
    parser.add_argument('output')

    args = parser.parse_args()
    reference_path = args.reference
    incorrect_path = args.incorrect
    output_path = args.output

    reference_subtitles = natsorted(os.listdir(reference_path))
    incorrect_subtitles = natsorted(os.listdir(incorrect_path))
    for i in range(len(reference_subtitles)):
        reference_filepath = os.path.join(reference_path, reference_subtitles[i])
        incorrect_filepath = os.path.join(incorrect_path, incorrect_subtitles[i])
        output_filepath = os.path.join(output_path, incorrect_subtitles[i])

        subprocess.run([
            'alass',
            reference_filepath,
            incorrect_filepath,
            output_filepath
        ], shell=True)


if __name__ == '__main__':
    main()
