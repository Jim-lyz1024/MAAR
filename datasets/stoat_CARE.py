import glob
import re

import os.path as osp

import json

import os

from .bases import BaseImageDataset
from collections import defaultdict
import pickle


class STOAT(BaseImageDataset):
    """
    New Zealand (Waiheke Island and South Island) Stoat Dataset
    
    Dataset statistics:
    # train - South Island, gallery - Waiheke Island, query - Waiheke Island
    # identities: 56 (train) + 5 (gallery) + 5 (query)
    # images: 183 (train) + 13 (gallery) + 13 (query)
    """
    dataset_dir = "Stoat"

    def __init__(self, root='', verbose=True, pid_begin=0, data_p='data/stoat.json', **kwargs):
        super(STOAT, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'gallery')

        with open(data_p, 'rb') as f:
            data = json.load(f)

        infos = {}
        for d in data['images']:
            infos[d['img_path'].split('\\')[-1]] = d['metadata']

        self.infos = infos

        self._check_before_run()
        self.pid_begin = pid_begin
        train = self._process_dir(self.train_dir, relabel=True)
        query = self._process_dir(self.query_dir, relabel=False)
        gallery = self._process_dir(self.gallery_dir, relabel=False)

        if verbose:
            print("=> Stoat loaded")
            self.print_dataset_statistics(train, query, gallery)

        self.train = train
        self.query = query
        self.gallery = gallery

        self.num_train_pids, self.num_train_imgs, self.num_train_cams, self.num_train_vids = self.get_imagedata_info(
            self.train)
        self.num_query_pids, self.num_query_imgs, self.num_query_cams, self.num_query_vids = self.get_imagedata_info(
            self.query)
        self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams, self.num_gallery_vids = self.get_imagedata_info(
            self.gallery)

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError("'{}' is not available".format(self.train_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError("'{}' is not available".format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError("'{}' is not available".format(self.gallery_dir))

    def _process_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))

        special_cameras = {"CREK": 1000, "FC01": 1001, "FC11": 1002, "GC34": 1003, "P164": 1004}
        pattern = re.compile(r'\d+_[0-9a-zA-Z]+_\d+')

        pid_container = set()
        camid_container = set()

        for img_path in sorted(img_paths):
            pid, camid, _ = pattern.search(img_path).group().split("_")
            pid = int(pid)
            if camid in special_cameras:
                camid = special_cameras[camid]
            camid = int(camid)
            pid_container.add(pid)
            camid_container.add(camid)

        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []
        for img_path in sorted(img_paths):
            pid, camid, _ = pattern.search(img_path).group().split("_")
            pid = int(pid)
            if camid in special_cameras:
                camid = special_cameras[camid]
            camid = int(camid)

            assert 0 <= pid <= 55

            if relabel:
                pid = pid2label[pid]
            name = os.path.basename(img_path)
            dataset_info = self.infos[name]

            metalabel = self.get_metalabel(dataset_info)

            # camid = -1
            dataset.append((img_path, self.pid_begin + pid, camid, 0,*metalabel))

        return dataset

    def get_metalabel(self, dataset_info):

        temperature = dataset_info['temperature']
        humidity = dataset_info['humidity']
        rain = dataset_info['rain']
        angle = dataset_info['angle']

        temperature = float(temperature)
        humidity = float(humidity)
        angle = float(angle)
        rain = float(rain)

        if temperature < 17:
            temperature_label = 'cold'
        elif temperature >= 17 and temperature < 20:
            temperature_label = 'mild'
        elif temperature >= 20:
            temperature_label = 'hot'

        if humidity < 75:
            humidity_label = 'dry'
        elif humidity >= 75 and humidity < 85:
            humidity_label = 'moderate'
        elif humidity >= 85:
            humidity_label = 'humid'

        if rain == 0:
            rain_label = 'no rain'
        elif rain > 0 and rain <= 10:
            rain_label = 'light'
        elif rain > 10 and rain <= 50:
            rain_label = 'moderate'
        elif rain >= 50:
            rain_label = 'heavy'

        if angle==0:
            angle_label='front'
        elif angle==1:
            angle_label='back'
        elif angle==2:
            angle_label='left'
        elif angle==3:
            angle_label='right'

        print(temperature_label, humidity_label, rain_label, angle_label)
        return temperature_label, humidity_label, rain_label, angle_label
