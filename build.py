#!/bin/env python
"""
MeSH ID -> names

Parses MeSH XML file from https://www.nlm.nih.gov/databases/download/mesh.html and
generates a mapping from MeSH identifiers to descriptive names.
"""
import os
import gzip
import pandas as pd
import yaml
import xml.etree.ElementTree as ET
from uuid import uuid1
from frictionless import describe

# load recipe conifg & metadata
with open("recipe.yml") as fp:
    mdat = yaml.load(fp, Loader=yaml.FullLoader)

# lists to store values to use in output
ids = []
names = []

# 1. descriptors
with gzip.open(mdat["data"]["input"]["desc"], "rb") as fp:
    tree = ET.parse(fp)
    root = tree.getroot()

ids = [elem.text for elem in root.findall(".//DescriptorRecord/DescriptorUI")]
names = [elem.text for elem in root.findall(".//DescriptorRecord/DescriptorName/String")]

#
# 2. supplemental concept records
#
with gzip.open(mdat["data"]["input"]["supp"], "rb") as fp:
    tree = ET.parse(fp)
    root = tree.getroot()

ids = ids + [elem.text for elem in root.findall(".//SupplementalRecord/SupplementalRecordUI")]
names = names + [elem.text for elem in root.findall(".//SupplementalRecord/SupplementalRecordName/String")]

#
# 3. package
#
out_dir = os.path.dirname(mdat["data"]["output"]["mapping"])

# save table
if not os.path.exists(out_dir):
    os.makedirs(out_dir, mode=0o755)

df = pd.DataFrame({"mesh_id": ids, "name": names})
df.to_feather(mdat["data"]["output"]["mapping"])

# create pkg
pkg = describe(mdat["data"]["output"]["mapping"], type="package", stats=True)
pkg_dict = pkg.to_dict()

pkg_dict.update(mdat["metadata"])

pkg_dict["id"] = str(uuid1())

resource_updates = {
    "name": "mesh-id-mapping",
    "path": "mapping.feather",
    "fields": 2,
    "rows": df.shape[0],
    "schema": {
        "fields": [
            {"name": "mesh_id", "type": "string"},
            {"name": "name", "type": "string"},
        ]
    }
}
pkg_dict["resources"][0].update(resource_updates)

with open(os.path.join(out_dir, "datapackage.yml"), "w") as fp:
    yaml.dump(pkg_dict, fp)
