# Snap and Listen

Snap a selfie or a landscape and let image recognition do the rest. Then Spotify will recommend you a corresponding playlist.

## Getting Started

Project front end is a Telegram chat bot and the back end is GCP cloud functions in a python37 runtime. Unfortunately, you will need your own GCP project and API keys to run this on your own.

## Prerequisites

* [Telegram chat bot](https://core.telegram.org/bots) - Front end used
* [Google Cloud Platform](https://cloud.google.com/) - Back end
* [Cloud Functions API Enabled](https://cloud.google.com/functions/) - Webhook
* [Cloud Vison API Enabled](https://cloud.google.com/vision/) - Image Recognition
* [Spotify Developer Application](https://developer.spotify.com/) - Spotify Search API
* env.yaml file that includes all of your API key information


## Deploy webhook
Example env.yaml file:
```
TELEGRAM_TOKEN: uvwxyz
GCS_BUCKET: example-bucket
VISION_API_KEY: abcdef
SPOTIPY_CLIENT_ID: ghijkl
SPOTIPY_CLIENT_SECRET: mnopqr
```

Then run the following in your terminal
```
$ git clone https://github.com/meirelon/snap-and-listen.git
$ cd ./snap-and-listen
$ gcloud beta functions deploy snap_and_listen --env-vars-file env.yaml --runtime python37 --trigger-http
```

## Examples
### Facial Recognition

![alt text](https://raw.githubusercontent.com/meirelon/snap-and-listen/master/readme_images/roger_federer.jpg)

### Landscape Detection

![alt text](https://raw.githubusercontent.com/meirelon/snap-and-listen/master/readme_images/grand_canyon.jpg)

## Contributing

Please reach out via email or send me a pull request.

## Authors

* **Michael Nestel**
