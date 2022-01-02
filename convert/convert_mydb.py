"""
Author: Thi Minh Nhut <thiminhnhut@gmail.com>
Date: 2022-01-02 13:40:30
Title: convert_mydb.py
Command: python convert_mydb.py -i ../db.json -o ./provincesdb.json
"""

import argparse
import json
from time import gmtime, strftime


class Province:
    def __init__(self, idProvince, name):
        self.idProvince = idProvince
        self.name = name


class District:
    def __init__(self, idProvince, idDistrict, name):
        self.idProvince = idProvince
        self.idDistrict = idDistrict
        self.name = name


class Commune:
    def __init__(self, idDistrict, idCommune, name):
        self.idDistrict = idDistrict
        self.idCommune = idCommune
        self.name = name


def convert_mydb(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    province_json = data.get("province", None)
    district_json = data.get("district", None)
    commune_json = data.get("commune", None)

    provinces = []
    for province in province_json:
        province_obj = Province(province.get("idProvince", None),
                                province.get("name", None))
        provinces.append(province_obj)

    districts = []
    for district in district_json:
        district_obj = District(district.get("idProvince", None),
                                district.get("idDistrict", None),
                                district.get("name", None))
        districts.append(district_obj)

    communes = []
    for commune in commune_json:
        commune_obj = Commune(commune.get("idDistrict", None),
                              commune.get("idCommune", None),
                              commune.get("name", None))
        communes.append(commune_obj)

    db = dict()
    for province in provinces:
        db_district = dict()
        for district in districts:
            if district.idProvince == province.idProvince:
                db_commune = list()
                for commune in communes:
                    if commune.idDistrict == district.idDistrict:
                        db_commune.append(commune.name.title())
                db_district[district.name.title()] = db_commune
        db[province.name.title()] = db_district

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(
            dict(timestamp=strftime("%Y-%m-%d %H:%M:%S", gmtime()), provice=db),
            f, ensure_ascii=False, indent=4)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("-i", "--input", help="json db input file", required=True)
    args.add_argument("-o", "--output", help="json db output file", required=True)
    input_file = args.parse_args().input
    output_file = args.parse_args().output
    convert_mydb(input_file, output_file)


if __name__ == "__main__":
    main()
