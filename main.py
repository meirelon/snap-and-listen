import os
import requests
import uuid

import telegram

from deps.images import get_image, get_vision_request, get_emotion, get_image_keyword
from deps.gcloud import upload_blob
from deps.playlists import get_playlist

def snap_and_listen(request):
    token = os.environ["TELEGRAM_TOKEN"]
    bucket = os.environ["GCS_BUCKET"]
    key = os.environ["VISION_API_KEY"]
    spotify_client_id = os.environ["SPOTIPY_CLIENT_ID"]
    spotify_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    
    photo_id = str(uuid.uuid4())

    # Initialize Telegram Bot
    bot = telegram.Bot(token=token)

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)
        chat_id = update.message.chat.id

        if update.message.photo:
            try:
                fileID = update.message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                photo_link = file_info.file_path

                # Process the image and store in GCS bucket
                get_image(photo_link)
                upload_blob(bucket_name=bucket,
                            source_file_name="/tmp/photo-{}.jpg".format(photo_id),
                            destination_blob_name="photo-{}.jpg".format(photo_id))

                # Make the image recognition request to api
                r = get_vision_request(key=key,
                                       bucket_path=bucket)

                # Get the keyword from the request above
                keyword = get_image_keyword(r)

                # Keyword search the Public Spotify Playlist repository
                playlist = get_playlist(clientID=spotify_client_id,
                                        clientSECRET=spotify_secret,
                                        keyword=keyword)

                full_response = "Here is your {keyword} playlist: {playlist}".format(keyword=keyword, playlist=playlist)

                bot.sendMessage(chat_id=chat_id, text=full_response)
            except Exception as e:
                bot.sendMessage(chat_id=chat_id, text=str(e))
        else:
            bot.sendMessage(chat_id=chat_id, text="Please send a picture")
