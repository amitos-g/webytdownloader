from flask import Flask, render_template, request
from flask.views import MethodView
from pytube import YouTube
from pytube.exceptions import *
import flask

from io import BytesIO

def validate(url : str, mp4: bool):
    try:
        youtube_object = YouTube(url)
        if mp4:
            return youtube_object.streams.get_highest_resolution()
        else:
            return youtube_object.streams.get_audio_only()
    except PytubeError or Exception:
        raise Exception



app = Flask(__name__)
app.secret_key = "abc"





class HomePage(MethodView):
    def get(self):

        return render_template('index.html')

    def post(self):

        try:
            link = request.form.get("link")
            select = request.form.get("select")
            try:
                if select == 'audio': # if audio is clicked


                    yt = validate(link, False)
                    title = yt.title
                    yt.stream_to_buffer(buffer:=BytesIO())
                    buffer.seek(0)
                    return flask.send_file(buffer, as_attachment=True, download_name=f'{title}.mp3')



                if select == 'video': # if audio is clicked
                    yt = validate(link, True)
                    title = yt.title
                    yt.stream_to_buffer(buffer:=BytesIO())
                    buffer.seek(0)

                    return flask.send_file(buffer, as_attachment=True, download_name=f'{title}.mp4')


                else:
                    return render_template('index_error.html', error='Please Select Audio/Video!')
            except Exception:
                return render_template('index_error.html', error='Invalid Link!')
        except Exception:
            return render_template('index_error.html',  error='Error! Try Again.')



app.add_url_rule('/', view_func=HomePage.as_view('home'))

app.run(debug=True)