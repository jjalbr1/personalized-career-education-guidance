const express = require('express');
const multer = require('multer');
const path = require('path');
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

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

app.post('/upload', upload.single('resume'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ success: false, message: 'No files were uploaded.' });
    }
    res.json({ success: true, resumePath: req.file.path });
});

app.post('/process', (req, res) => {
    const { resumePath } = req.body;
    console.log('Received request with resumePath:', resumePath);

    if (!resumePath) {
        return res.status(400).json({ success: false, message: 'Resume path is required.' });
    }

    const normalizedPath = path.resolve(resumePath);
    console.log('Normalized path:', normalizedPath);

    const command = `python resume_advice.py "${normalizedPath}"`;
    console.log('Executing command:', command);

    exec(command, (error, stdout, stderr) => {
        console.log(`stdout: ${stdout}`);
        console.log(`stderr: ${stderr}`);
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ success: false, message: 'Error processing resume.', error: error.message, stderr: stderr });
        }

        res.json({ success: true, advice: stdout });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
