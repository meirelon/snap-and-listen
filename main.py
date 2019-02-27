import os
import requests

import telegram

from ImageIO import get_image, get_emotion, get_vision_request
from gcloud_utils import upload_blob
from spotipy import get_playlist

def snap_and_listen(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True,
                                                          silent=True,
                                                          cache=True), bot)

        if update.message.photo:
            try:
                chat_id = update.message.chat.id
                fileID = update.message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                photo_link = file_info.file_path
                get_image(photo_link)
                upload_blob(bucket_name=os.environ["GCS_BUCKET"], source_file_name="/tmp/photo.jpg", destination_blob_name="photo.jpg")

                r = get_vision_request(key=os.environ["VISION_API_KEY"], bucket_path=os.environ["GCS_BUCKET"])
                keyword = get_image_keyword(r)

                playlist = get_playlist(clientID=os.environ["SPOTIPY_CLIENT_ID"],
                                        clientSECRET=os.environ['SPOTIPY_CLIENT_SECRET'],
                                        keyword=keyword)

                full_response = "Here is your {keyword} playlist: {playlist}".format(keyword=keyword, playlist=playlist)

                bot.sendMessage(chat_id=chat_id, text=full_response)
            except Exception as e:
                bot.sendMessage(chat_id=chat_id, text=str(e))
        else:
            bot.sendMessage(chat_id=chat_id, text="Please send a picture")        
