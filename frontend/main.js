const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const downloadLink = document.getElementById('downloadLink');
const resultDiv = document.getElementById('result');
let intervalId;
let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob);

        // Create a URL for the audio blob and set it as the href for the download link
        const audioUrl = URL.createObjectURL(audioBlob);
        downloadLink.href = audioUrl;
        downloadLink.download = 'recorded_sample.webm';
        downloadLink.style.display = 'inline-block';

        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        resultDiv.innerHTML = `<p><strong>Text:</strong> ${result.text}</p><p><strong>Sentiment:</strong> ${result.sentiment.label} (Score: ${result.sentiment.score})</p>`;
        audioChunks = []; // Clear audio chunks for the next recording
    };

    mediaRecorder.start();

    setTimeout(() => {
        mediaRecorder.stop();
    }, 5000); // Record for 5 seconds
}

startButton.addEventListener('click', () => {
    startButton.style.display = 'none';
    stopButton.style.display = 'inline-block';
    downloadLink.style.display = 'none';
    intervalId = setInterval(startRecording, 10000); // Record every 10 seconds
    startRecording(); // Start immediately
});

stopButton.addEventListener('click', () => {
    clearInterval(intervalId);
    startButton.style.display = 'inline-block';
    stopButton.style.display = 'none';
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop(); // Stop any ongoing recording
    }
});
