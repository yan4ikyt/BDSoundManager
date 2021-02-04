# BDSoundManager
Program for edit, extract, list SoundBank files or fix VAG or BD files.
Perfectly works! Original code by Nistro, BDFix original code by Pips.
Tested on Parappa The Rapper 2. 
All just need for Windows just run script in Command Line and here we go!
For linux, just run in terminal `python3 bdsoundmanager`

Usage : [-h] [-bd BD] [-hd HD] [-o OUT] [-in INPUT] [-m MODE] [-i INDEX]

  -h, --help            show help message and exit
  -bd BD, --bd BD       .BD File
  -hd HD, --hd HD       .HD File
  -o OUT, --out OUT     Output folder (must exist)
  -in INPUT, --input INPUT Input VAG file for export
  -m MODE, --mode MODE  'E' For extract, 'i' For import, 'F' for fix VAG file, 'l' for list audio in BD file
  -i IND, --ind IND     Index of VAG (need for import)
  
  Example : 
  
  ```BD Sound Manager.exe  -bd A01_gm0_00.bd -hd A01_gm0_00.hd -m i -in "A01_gm0_00_00.VAG" -i 00
  (BD Sound Manager.exe means name of exe program
   -bd means .BD File
   -hd means .HD File
   -m means Mode 'E' For extract, 'i' For import, 'F' for fix VAG file, 'l' for list audio in BD file
   -in means input VAG audio file (for import in Parappa The Rapper 2 must be soundrate 24,000 Hz and 1 mono channel)
   -i means Index of replace (example : if you wanna replace A01_gm0_00_04.VAG in A01_gm0_00.bd file, you must take number from VAG file example 04, then you must enter in index 04)
   )```
   
*Subscribe to [Yan4ik Channel on YouTube](https://youtube.com/channel/UCu6l8wKI7WGlwoD1It_vcdw)!*
