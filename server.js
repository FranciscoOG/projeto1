const http = require('http');
const fs = require('fs');
const path = require('path');
//let socket = new WebSocket('wss://example.com/socket');
const port = 3000;

http.createServer((req, res) => {
    const filePath = path.join(__dirname, 'indexv2.html');
    fs.readFile(filePath, (err, content) => {
        if (err) {
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('Error loading file');
        } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content);
        }
    });
}).listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});