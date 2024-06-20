from pathlib import Path

url_basemap = 'https://sgx.geodatenzentrum.de/gdz_basemapde_vektor/tiles/v1/bm_web_de_3857/13/4297/2667.pbf'
p = Path(*Path(url_basemap).parts[-4:])
print(p)