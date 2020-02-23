# heatmap_mockup
A quick & visual representation of the heatmap idea. 

To run this on your local computer:

1. Clone or download the repository.

2. To guarantee reproducibility make a clone of the python environment in which this was developed. We recommend the Anaconda or Miniconda python environment mangaer. See [here](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/macos.html). The baya-data-science repository under the [documentation](https://github.com/baya-network/baya-data-science/tree/master/documentation) folder has guidelines on installing Anaconda/Miniconda and managing python environments.
  
  However, the only necessary packages are geopandas v.0.4.0, pandas v.0.23.4, and bokeh v.1.0.4, and python v.>=3.6, in case you want to skip Miniconda installation. If so, proceed to step 5.

3. Within the repository, type ```conda env create -f heatmap_mockup_env.yml```. See _environment usage_ from [documentation](https://github.com/baya-network/baya-data-science/tree/master/documentation).

4. Accept any prompts and when the environemnts finishes installing type ``` conda activate heatmap_mockup_env``` to access it.

5. Now type ```bokeh serve --show heatmap_mockup.py```. A browser window will open and display the mockup.


