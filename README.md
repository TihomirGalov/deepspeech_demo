# DeepSpeech

DeepSpeech is a simple GUI implementation of the DeepSpeech library, to record your microphone and export the conversations as .txt files
## Installation

Install all the project requirements
```bash
pip3 install -r requirements.txt
```
then you must install the pre-trained model files in the project directory
```bash
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
```
## Usage
From the command line start the app using the following command:
```bash
python3 main.py
```
Then when you hit "Start" your voice activity will be recorded and after you hit "Stop" the file will be saved in the media/ directory

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
