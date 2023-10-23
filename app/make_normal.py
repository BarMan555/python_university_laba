import logging
import os
from dataset_interface import DataAbstract
from get_way import get_path_normal

class MakeNormalCsv(DataAbstract):
    def write_in_file(name_csv : str, img_classes : list, directory : str) -> None:
        """
        Pick over objects

        Pick over objects
        Parameters
        ----------
        name_csv : str
            Name of csv file
        img_classes : list
            List if objects
        directory : str
            Directory where is our img
        """
        try:
            DataAbstract.create_csv(name_csv)
            for img_class in img_classes:
                number_of_img = len(os.listdir(os.path.join(directory, img_class)))
                for img in range(number_of_img):
                    DataAbstract.write_in_csv(name_csv, img_class, get_path_normal(img_class, img))
        except Exception as ex:
            logging.error(f"Error of add to csv file : {img} | {ex}")
