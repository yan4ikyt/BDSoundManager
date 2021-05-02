# BDSoundManager
Program for edit, extract, list SoundBank files or fix VAG or BD files.

Perfectly works! Original code by Nistro, BDFix original code by Pips.
Tested on Parappa The Rapper 2.

All just need for Windows just run script in Command Line and here we go!
For linux, just run in terminal `python3 bdsoundmanager`

```
usage: [-h] [-bd BD] [-hd HD] [-o OUT] [-inf INPUTFOLDER] [-in INPUT] [-m MODE]

optional arguments:
  -h, --help            show this help message and exit
  -bd BD, --bd BD       .BD File
  -hd HD, --hd HD       .HD File
  -o OUT, --out OUT     Output folder (must exist)
  -inf INPUTFOLDER, --inputfolder INPUTFOLDER
                        Input folder (must exist)
  -in INPUT, --input INPUT
                        Input VAG file for export
  -m MODE, --mode MODE  'E' For extract, 'i' For import, 'F' for fix VAG file, 'l' for list audio in BD file
```  
  Example : 
  
  BD Sound Manager.exe -bd A01_gm0_00.bd -hd A01_gm0_00.hd -m i -inf "C:/P2/STAGE1/PROPS"
  ```(BD Sound Manager.exe means name of exe program
   -bd means .BD File
   -hd means .HD File
   -m means Mode 'E' For extract, 'i' For import, 'F' for fix VAG file, 'l' for list audio in BD file
   -inf means input folder where .wav files are situated
   )
   ```
   
*Subscribe to [Yan4ik Channel on YouTube](https://youtube.com/channel/UCu6l8wKI7WGlwoD1It_vcdw)!*
