"""
Script for preprocessing images in dataset by applying transforms such as resizing, color scale conversions etc.
"""

import pathlib
import logging

import tqdm
import click

from wai_data_tools.setup_logging import setup_logging
from wai_data_tools import preprocessing
from wai_data_tools import config
from wai_data_tools import io


def preprocess_images(config_filepath: pathlib.Path,
                      src_root_dir: pathlib.Path,
                      dst_root_dir: pathlib.Path) -> None:
    """
    Preprocess by applying transformations given in config to images in source directory and store results in
    destination directory.

    :param config_filepath: Path to config file
    :param src_root_dir: Source root directory to read images from.
    :param dst_root_dir: Destination root directory to store images.
    """
    config_dict = config.load_config(config_filepath=config_filepath)
    preprocess_config = config_dict["preprocessing"]

    logging.info("Composing transforms")
    composed_transforms = preprocessing.compose_transforms(transforms_config=preprocess_config["transformations"])

    logging.info("Preprocessing images")
    frame_dirs = [dir_path for dir_path in src_root_dir.iterdir() if dir_path.is_dir()]
    for frame_dir in tqdm.tqdm(frame_dirs):
        frames_dict = io.load_frames(frame_dir)

        for frame_index, frame_dict in frames_dict.items():
            logging.debug("Applying transforms to frame %s for video %s", frame_index, frame_dir.name)
            frame_dict["img"] = composed_transforms(frame_dict["img"])

        io.save_frames(video_name=frame_dir.stem,
                       dst_root_dir=dst_root_dir,
                       frames_dict=frames_dict)


@click.command()
@click.option("--config_filepath", type=pathlib.Path, help="Path to config file")
@click.option("--src_root_dir", type=pathlib.Path, help="Source root directory to read images from.")
@click.option("--dst_root_dir", type=pathlib.Path, help="Destination root directory to store images.")
def main(config_filepath: pathlib.Path,
         src_root_dir: pathlib.Path,
         dst_root_dir: pathlib.Path) -> None:
    setup_logging()
    preprocess_images(config_filepath=config_filepath,
                      src_root_dir=src_root_dir,
                      dst_root_dir=dst_root_dir)


if __name__ == "__main__":
    main()