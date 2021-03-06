"""
Script for converting file structure to a format that is easier to upload to edge impulse.
"""
import logging
import pathlib
import shutil
import argparse

import tqdm

from wai_data_tools.setup_logging import setup_logging


def convert_file_structure_to_upload_format(src_root_dir: pathlib.Path,
                                            dst_root_dir: pathlib.Path) -> None:
    """
    Copies contents of a source file structure and stores it as a format that is easier to upload to edge impulse in
    a destination directory.

    :param src_root_dir: Source root directory to read files from.
    :param dst_root_dir: Destination root directory to store new file structure.
    """

    frame_dirs = [content for content in src_root_dir.iterdir() if content.is_dir()]

    logging.info("Creating new file structure")
    for frame_dir in tqdm.tqdm(frame_dirs):
        target_dirs = [content for content in frame_dir.iterdir() if content.is_dir()]
        for target_dir in target_dirs:
            target_name = target_dir.stem
            dst_target_dir = dst_root_dir / target_name

            dst_target_dir.mkdir(exist_ok=True, parents=True)

            for frame_filepath in target_dir.glob("*.jpeg"):
                shutil.copy(str(frame_filepath), str(dst_target_dir / frame_filepath.name))


def main():
    setup_logging()

    parser = argparse.ArgumentParser("Copies contents of a source file structure and stores it as a format that is "
                                     "easier to upload to edge impulse in a destination directory.")

    parser.add_argument('src_root_dir', type=str,
                        help='Path to the root source directory containing image files')
    parser.add_argument('dst_root_dir', type=str,
                        help='Path to the root destination root directory to save images')

    args = parser.parse_args()

    src_root_dir = pathlib.Path(args.src_root_dir)
    dst_root_dir = pathlib.Path(args.dst_root_dir)

    convert_file_structure_to_upload_format(src_root_dir=src_root_dir, dst_root_dir=dst_root_dir)


if __name__ == "__main__":
    main()
