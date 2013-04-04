
from opensezame import get_real_path
from shutil import copy

import argparse
import os


def copyproject(source_path, destination_path):
    for root, dirnames, filenames in os.walk(source_path):
        for filename in filenames:
            if os.path.splitext(filename)[1] in ['.py', '.json', '.html']:
                middle = root.replace(source_path, '')
                relative_path = os.path.join(
                    middle,
                    filename
                )
                if relative_path[0] == os.sep:
                    relative_path = relative_path[1:]

                src = os.path.join(root, filename)
                dest = os.path.join(destination_path, relative_path)

                dest_dir = os.path.dirname(dest)
                if not os.path.exists(dest_dir):
                    print "New folder .. {0}".format(middle[1:])
                    os.makedirs(dest_dir)

                if os.path.exists(dest):
                    print "Overwrite ... {0}".format(relative_path)
                else:
                    print "New file .... {0}".format(relative_path)
                copy(
                    src,
                    dest
                )


def init():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'destination',
        help="Destination directory."
    )

    parser.add_argument(
        '-y', '--yes',
        action="store_true",
        help="Yes to overwrite."
    )

    args = parser.parse_args()

    source_path = os.path.join(os.path.dirname(get_real_path()), 'example')
    destination_path = os.path.abspath(args.destination)
    overwrite = None

    if args.yes or os.path.exists(destination_path):
        answer = raw_input("Destination path exists, overwrite? (y/N): ")
        if answer and 'y' == answer[0].lower():
            overwrite = True
        else:
            overwrite = False

    if overwrite is None:
        print "Creating new project ..."
    elif overwrite:
        print "Overwriting ..."
    else:  # overwrite is False
        print "Doing nothing."
        exit(0)

    try:
        copyproject(source_path, destination_path)
    except:
        raise
    else:
        print "Done: {0}".format(destination_path)
