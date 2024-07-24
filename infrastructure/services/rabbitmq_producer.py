import pika
import json

def send_verification_request(user_token, response_queue, callback):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()
        channel.queue_declare(queue='verification_queue')
        channel.queue_declare(queue=response_queue)

        message = json.dumps({'token': user_token, 'response_queue': response_queue})
        print(f"Sending message to verification_queue: {message}")
        channel.basic_publish(
            exchange='',
            routing_key='verification_queue',
            body=message
        )
        print("Message sent successfully")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")

    def on_response(ch, method, properties, body):
        print(f"Received message: {body}")
        try:
            data = json.loads(body)
            callback(data) 
            channel.stop_consuming()
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    channel.basic_consume(queue=response_queue, on_message_callback=on_response, auto_ack=True)
    channel.start_consuming()
