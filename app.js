const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { PythonShell } = require('python-shell');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Define the desktop and temp directory paths
const desktopPath = path.join(os.homedir(), 'Desktop');
const tempDir = path.join(desktopPath, 'temp');

// Create the temp directory if it doesn't exist
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir);
}

// Set up storage for uploaded files
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, tempDir);
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage: storage });

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the public directory
app.use(express.static('public'));

// Serve static files from the temp directory
app.use('/temp', express.static(tempDir));

// Set view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Route for file upload and processing
app.post('/upload', upload.single('audiofile'), (req, res) => {
    console.log('Received upload request');
    const file = req.file;
    const cutoff = req.body.cutoff;

    if (!file) {
        console.error('No file uploaded.');
        return res.status(400).send('No file uploaded.');
    }

    const uploadPath = path.join(tempDir, file.filename);
    console.log('File uploaded to:', uploadPath);

    const options = {
        args: [uploadPath, cutoff],
        pythonOptions: ['-u'], // Unbuffered output
        scriptPath: path.join(__dirname), // Ensure the correct path
    };

    PythonShell.run('process_audio.py', options, (err, results) => {
        console.log("Inside PythonShell run callback");

        if (err) {
            console.error('Python script error:', err);
            return res.status(500).send('Error processing file');
        }

        console.log('Python script finished processing');
        
    });
    // Prepare paths for output files
    const outputFiles = {
        filteredAudio: `/temp/filtered_${file.filename}`,
        originalPlot: `/temp/original_signal.png`,
        fftMagnitudePlot: `/temp/fft_magnitude.png`,
        filteredFFTPlot: `/temp/filtered_fft_magnitude.png`,
        filteredSignalPlot: `/temp/filtered_signal.png`
    };

    // Add a delay before rendering the results page
    const delay = 5000; // 5 seconds delay
    setTimeout(() => {
        // Render results page after delay
        res.render('results', { outputFiles });
    }, delay);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
