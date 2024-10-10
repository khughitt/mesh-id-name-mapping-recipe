# Recipe: Medical Subject Headings (MeSH) ID/Name Mapping

Parses [MeSH XML file](https://www.nlm.nih.gov/databases/download/mesh.html) and creates a data
package containing a simple two-column table mapping from MeSH IDs to descriptive names.

Example of output structure:

```
df.head()

   mesh_id                    name
0  D000001              Calcimycin
1  D000002                 Temefos
2  D000003               Abattoirs
3  D000004  Abbreviations as Topic
4  D000005                 Abdomen
```

# Usage

1. Download MeSH XML "desc" and "supp" files:

```
mkdir -p /data/raw/mesh/
cd /data/raw/mesh/

wget https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2024.gz
wget https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2024.gz
```

2. Edit `recipe.yml` and make sure the directories and are configured as desired.

3. Create a virtual environment with the needed deps and run the build script:

```
mkdir -p ~/venv

python -m ~/venv/mesh-recipe
source ~/venv/mesh-recipe/bin/activate

pip install --file requirements.txt
python build.py
```
