# pi_assistant
Speech recognition assistant based on deepspeech. The little program is derived from the example speech2text code published on the Tradokk web site. I've added a logic to cut of the sound buffer if there is no new text recognized after 2 seconds. This is tested mainly with the German language model created by Aashish Agarwal, but it should work with any other model in the same way. Currently it's only the continous speech recognition is implmented. Any logik to compute the input is totally lacking.

I want to thank the Deepspeech project, Aashish Agarwal and the Tradokk team for providing all the parts. Making it so easy to setup a speech recognition in the meanwhile.

## Links & References

**Deepspeech Project:** https://github.com/mozilla/DeepSpeech

**German Deepspeech Model by Aashish Agarwal:** https://github.com/AASHISHAG/deepspeech-german

**Tradokk Example Code:** https://tradokk.com/echtzeit-spracherkennung-mit-deepspeech/

