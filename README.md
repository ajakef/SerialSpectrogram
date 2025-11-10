### Installation
* First, set up the conda environment with dependencies.
```
conda config --add channels conda-forge
conda create -y -n serialspectrogram python=3.10 numpy obspy matplotlib scipy pytest
```

* Next, from the right project folder, clone the github repository.
```
conda activate serialspectrogram
git clone https://github.com/ajakef/SerialSpectrogram/
```

* Then, change directory into the `SerialSpectrogram/` folder and run `./serial_spectrogram.py`. 
