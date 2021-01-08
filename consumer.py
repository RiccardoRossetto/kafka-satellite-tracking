from flask import Flask, render_template, Response
from kafka import KafkaConsumer

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<topic>')
def get_messages(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=False,
    )

    def events():
        for msg in consumer:
            yield 'data:{0}\n\n'.format(msg.value.decode())
    return Response(events(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

