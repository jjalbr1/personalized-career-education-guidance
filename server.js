// server.js

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
require('./tracing');  

const app = express();
const PORT = process.env.PORT || 3000;

// Multer storage configuration
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// POST endpoint for file upload
app.post('/upload', upload.single('resume'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No files were uploaded.');
    }
    res.send('File uploaded successfully.');
});

app.get('/', (req, res) => {
    res.send('Hello World!');
    })

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
