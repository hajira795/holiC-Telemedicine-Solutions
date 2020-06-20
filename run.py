from web import website
from web import socketio

if __name__ == '__main__':
    website.run(debug=True)


if __name__ == '__main__':
    socketio.run(website, debug=True)