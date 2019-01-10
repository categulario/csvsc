#!/usr/bin/env python3
import os
import csv
import re
import json
import unicodedata
from operator import add


def parts(name):
    return re.match(r'.*axTP([0-9]+)([A-Z]{2})8539\.csv$', name).groups()


def remove_accents(input_str):
    # https://stackoverflow.com/questions/517923
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def parse(string):
    if string == '' or string is None:
        return None

    try:
        return float(string)
    except ValueError:
        return 0.0


class Organizer:

    def __init__(self, scandir, outdir):
        self.scandir = scandir
        self.outdir = outdir
        self.writers = dict()
        self.data = dict()

    def __call__(self):
        for file in os.scandir(self.scandir):
            if not file.path.endswith('.csv'):
                continue

            self.process_single(file)

        # finished all the files, now we have all the info
        for uuid, info in self.data.items():
            with open(os.path.join(self.outdir, uuid+'.json'), 'w') as jfile:
                json.dump(info, jfile, indent=2)

    def make_uid(self, data, model):
        return remove_accents("{}_{}_{}".format(
            data['Nombre_de'],
            data['Nombre_RHA'],
            model,
        )).lower().replace(" ", '_')

    def get_writer(self, uid, fieldnames):
        if uid not in self.writers:
            writer = csv.DictWriter(
                open(os.path.join(self.outdir, uid + '.csv'), 'w'),
                fieldnames=fieldnames,
            )
            writer.writeheader()

            self.writers[uid] = writer

        return self.writers[uid]

    def output_data(self, data, **kwargs):
        data = data.copy()

        for key, value in kwargs.items():
            data[key] = value

        omited = [
            'Clasif',
            'ESTADOS',
            'Nombre_RHA',
            'Nombre_de',
            'iden',
            'supkm2',
            'xymean',
            'xymedian',
            'xymode',
            'xyrange',
            'xystd',
            'xyunique',
            'xyvar',
        ]

        for key in omited:
            del data[key]

        return data

    def process_single(self, file):
        ''' processes the given file '''
        month, model = parts(file.path)

        with open(file, encoding='iso-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)

            # by ranges
            cur_output_uuid = None
            rows = []

            for line in reader:
                cur_line_uuid = self.make_uid(line, model)

                if cur_line_uuid != cur_output_uuid:
                    if cur_output_uuid is not None:
                        self.process_group(cur_output_uuid, month, model, rows.copy())
                        rows = []
                    cur_output_uuid = cur_line_uuid

                rows.append(line)

    def process_group(self, uuid, month, model, lines):
        ''' `lines` represents lines belonging to the same graphic '''
        if uuid not in self.data:
            self.data[uuid] = {
                f'r{i}': [] for i in range(1, 5)
            }

        height_tmp = {
            f'r{i}': {
                'max': -float('inf'),
                'min': float('inf'),
                'sum': 0,
                'count': 0,
            } for i in range(1,5)
        }

        for line in lines:
            height = line['rangosalt']

            if line['xysum']:
                height_tmp[f'r{height}']['sum'] += float(line['xysum'])
            if line['xycount']:
                height_tmp[f'r{height}']['count'] += float(line['xycount'])

            if line['xymax']:
                pmax = float(line['xymax'])
                if pmax > height_tmp[f'r{height}']['max']:
                    height_tmp[f'r{height}']['max'] = pmax

            if line['xymin']:
                pmin = float(line['xymin'])
                if pmin < height_tmp[f'r{height}']['min']:
                    height_tmp[f'r{height}']['min'] = pmin

        for height, data in height_tmp.items():
            self.data[uuid][height].append({
                'max': data['max'] if data['max'] > -float('inf') else 0,
                'min': data['min'] if data['min'] < float('inf') else 0,
                'avg': data['sum']/data['count'] if data['count'] != 0 else 0,
            })


def update_min(prev, attempt):
    try:
        return min(prev, float(attempt))
    except ValueError:
        return prev


def update_max(prev, attempt):
    try:
        return max(prev, float(attempt))
    except ValueError:
        return prev


def update_sum(prev, attempt):
    try:
        return add(prev, float(attempt))
    except ValueError:
        return prev


if __name__ == '__main__':
    assert update_min(3, '2') == 2
    assert update_min(3, '4') == 3
    assert update_min(3, '') == 3

    assert update_max(3, '2') == 3
    assert update_max(3, '4') == 4
    assert update_max(3, '') == 3

    assert update_sum(3, '2') == 5
    assert update_sum(3, '4') == 7
    assert update_sum(3, '') == 3
