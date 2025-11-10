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

* Then, change directory into the `SerialSpectrogram/` folder and run `./serial_spectrogram.py`. It will probably have to restart a few times before it begins plotting. You may have to create a CONFIG.TXT file on the microSD card telling it to run all 4 channels. 
