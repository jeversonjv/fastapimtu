import pika


class RabbitMQClient:
    def __init__(self):
        self.host = "rabbitmq"
        self.port = 5672
        self.username = "guest"
        self.password = "guest"
        self.exchange_name = "fastapi_mail"
        self.queue_name = "fastapi_mail"
        self.routing_key = "fastapi_mail"

        credentials = pika.PlainCredentials(self.username, self.password)

        parameters = pika.ConnectionParameters(
            self.host, self.port, '/', credentials)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type='direct')
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(
            queue=self.queue_name, exchange=self.exchange_name, routing_key=self.routing_key)

    def publish_message(self, message):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message
        )

    def consume_messages(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
