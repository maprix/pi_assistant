# pi_assistant
Speech recognition assistant based on mozilla DeepSpeech. The little program is derived from the example speech2text code published on the Tradokk web site. It is developed on a Raspberry Pi 4. I've added a logic to cut of the sound buffer if there is no new text recognized after 2 seconds. This is tested mainly with the German language model created by Aashish Agarwal, but it should work with any other model in the same way. Currently only the continuous speech recognition is implemented. Any logik to compute the input and to transform it in any useful action is totally lacking.

For the sound recording the usage of a PS3 Eye camera is hard coded.

For the german deepspeech language model the fixed tflite file created by **koh-osug** is needed: https://github.com/AASHISHAG/deepspeech-german/issues/29#issuecomment-744798408

## Links & References

**Deepspeech Project:** https://github.com/mozilla/DeepSpeech

**German Deepspeech Model by Aashish Agarwal:** https://github.com/AASHISHAG/deepspeech-german

**Tradokk Example Code:** https://tradokk.com/echtzeit-spracherkennung-mit-deepspeech/

**Using the PS3 Eye Camera:** https://www.cnx-software.com/2019/08/30/using-sony-ps3-eye-camera-as-an-inexpensive-microphone-array/

## Installation Pico TTS

On Respbery PI OS Buster the Pico TTS packages are not available. They can be installed from the Debian Buster repository. 
```console
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
sudo apt-get install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb
```

## Acknowledgements

I want to thank the [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) project, [AASHISHAG](https://github.com/AASHISHAG) and the [Tradokk team](https://tradokk.com) for providing all the parts. Making it so easy to setup a speech recognition in the meanwhile.