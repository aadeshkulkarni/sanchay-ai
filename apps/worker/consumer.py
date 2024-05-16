#!/usr/bin/env python
import os
import json
import pika
from pymongo import MongoClient
from utils import perform_magic, download_video, update_data, log_error_to_db
import socket
socket.gethostbyname("")

MONGO_DB=os.getenv("MONGO_DB")
AMQP_URL=os.getenv("AMQP_URL")
client = MongoClient(MONGO_DB)
db = client['test']
collection = db["videos"]

# Testing | see all collections within the connected db
# for coll in db.list_collection_names():
#     print(coll)

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('localhost', credentials=credentials)
connection = pika.BlockingConnection(parameters)
# connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq",port=5672,credentials=credentials,virtual_host="/"))
channel = connection.channel()
channel.queue_declare(queue="task_queue")
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    try:
        print(" [x] Recieved new message")
        data = json.loads(body.decode())
        print(" [x] ", data["_doc"])
        video_url = data["_doc"]["videoUrl"]
        video_id = data["_doc"]["_id"]
        filename = os.path.basename(video_url)
        download_video(video_url, filename)
        output = perform_magic(filename)
        update_data(collection, video_id, output)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(" [x] Error: ",str(e))
        print(e)
        log_error_to_db(collection,video_id,str(e))
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()
