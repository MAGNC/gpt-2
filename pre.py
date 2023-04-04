import gpt_2_simple as gpt2
import socketio
from flask import Flask, render_template, request
from model import Sess
import json
import subprocess
from flask_socketio import SocketIO, emit
import asyncio
app = Flask(__name__)
eve_json_path = "eve.json"
socketio = SocketIO(app)
sess = Sess()

async def read_json():#子进程读取json文件，这样可以不用阻塞
    tail_process = await asyncio.create_subprocess_exec("tail", "-f", eve_json_path, stdout=subprocess.PIPE)
    while True:
        line = await tail_process.stdout.readline()
        data = json.loads(line)
        text = data["text"]
        generated_text = gpt2.generate(sess.sess,
                                       length=10,
                                       temperature=0.7,
                                       prefix=text,
                                       nsamples=1,
                                       batch_size=1,
                                       top_k=40)
        # 将生成的文本发送到前端
        await socketio.emit('generated_text', {'generated_text': generated_text})

asyncio.ensure_future(read_json())#也就是readjson读到之后
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    socketio.run(app)
