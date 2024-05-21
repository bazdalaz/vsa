const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
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
    intervalId = setInterval(startRecording, 30000); // Record every 30 seconds
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
