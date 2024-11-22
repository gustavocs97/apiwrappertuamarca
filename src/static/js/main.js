let apiKey; // Variável para armazenar a chave da API
// let apiKeyWrapper; // Variável para armazenar a chave da API para o wrapper
let apiKeyWrapper = 'your_second_api_key'; // Defina a chave manualmente

async function fetchConfig() {
    try {
        const response = await fetch('/api/v1/config', {
            headers: {
                'Authorization': `Bearer ${apiKeyWrapper}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP! status: ${response.status}`);
        }

        const data = await response.json();
        apiKeyWrapper = data.apiKey; // Atribui a chave da API do wrapper
        console.log('Chave da API carregada:', apiKeyWrapper);
    } catch (error) {
        console.error('Erro ao buscar configuração:', error);
    }
}

// Call the function to fetch the configuration on startup
fetchConfig();

document.getElementById('fetchVoices').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/v1/voices/all', {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data); // Verify the structure

        const voiceSelect = document.getElementById('voice');
        voiceSelect.innerHTML = ''; // Clear existing options

        if (data.voices && Array.isArray(data.voices)) {
            data.voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.name; // Voice name
                option.textContent = `${voice.name} (${voice.language} - ${voice.gender})`; // Display text
                voiceSelect.appendChild(option);
            });
        } else {
            alert('No voices found or incorrect format.');
        }
    } catch (error) {
        alert('Error fetching voices: ' + error.message);
    }
});

document.getElementById('audioForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        input: document.getElementById('input').value,
        voice: document.getElementById('voice').value,
        model: "tts-1",
        response_format: "mp3"
    };

    try {
        const response = await fetch('/api/v1/speech', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKeyWrapper}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            if (response.status === 401) {
                alert('Authentication error: Please check your API key.');
            } else {
                alert(`Error: ${response.statusText}`);
            }
            return; // Prevent further execution on error
        }

        const data = await response.json();
        
        if (data.url) {
            const resultsContainer = document.getElementById('resultsContainer');
            const audioResult = document.createElement('div');
            audioResult.classList.add('audio-result');

            const audioPlayer = document.createElement('audio');
            audioPlayer.controls = true;
            audioPlayer.src = data.url;

            const downloadLink = document.createElement('a');
            downloadLink.href = data.url;
            downloadLink.download = true;
            downloadLink.textContent = 'Download Audio';

            // Create timer
            let timeLeft = 120;
            const timerElement = document.createElement('span');
            timerElement.textContent = `Link expires in: ${timeLeft} seconds`;

            const timer = setInterval(() => {
                timeLeft--;
                timerElement.textContent = `Link expires in: ${timeLeft} seconds`;
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    audioResult.remove(); // Remove audio after expiration
                }
            }, 1000);

            // Append elements to result container
            audioResult.appendChild(audioPlayer);
            audioResult.appendChild(timerElement);
            audioResult.appendChild(downloadLink);
            resultsContainer.appendChild(audioResult);
        } else {
            alert('Audio generation failed: No URL returned.');
        }
    } catch (error) {
        alert('Error generating audio: ' + error.message);
    }
});
