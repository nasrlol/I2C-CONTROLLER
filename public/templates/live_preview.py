from livereload import Server

server = Server()
# Watch HTML file
server.watch('index.html')
# Watch CSS files
server.watch('static/styles.css')
# Watch JavaScript files
server.watch('static/main.mjs')
# Watch other files if needed
server.watch('page/*')  # Watch everything in the page folder

# Serve the current directory
server.serve(root='.')
