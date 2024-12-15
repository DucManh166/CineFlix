from website import create_webview
# webview creation
webview = create_webview()

if __name__ == '__main__':
    webview.run(debug=True, port=5000)