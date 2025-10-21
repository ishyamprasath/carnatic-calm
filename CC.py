from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import secrets
import os
from urllib.parse import urlencode

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a strong secret key

# Mood analysis with multiple raga options per condition
def analyze_mood(stress, sleep, anxiety, energy):
    total_score = stress + anxiety + (5 - sleep) + (5 - energy)  # Max score: 20
    
    if total_score >= 15:  # High distress
        return [
            {'raga': 'Neelambari', 'description': 'Promotes sleep and calms the mind'},
            {'raga': 'Anandabhairavi', 'description': 'Relieves stress and promotes peace'},
            {'raga': 'Bhairavi', 'description': 'Reduces anxiety and brings emotional stability'}
        ]
    elif stress > 3 and anxiety > 3:  # High stress + anxiety
        return [
            {'raga': 'Bhairavi', 'description': 'Reduces anxiety and brings emotional stability'},
            {'raga': 'Shankarabharanam', 'description': 'Uplifts mood and reduces mental tension'},
            {'raga': 'Mohanam', 'description': 'Enhances focus and reduces restlessness'}
        ]
    elif sleep < 3:  # Poor sleep
        return [
            {'raga': 'Neelambari', 'description': 'Promotes sleep and calms the mind'},
            {'raga': 'Anandabhairavi', 'description': 'Relieves stress and promotes peace'}
        ]
    elif energy < 3:  # Low energy
        return [
            {'raga': 'Kalyani', 'description': 'Boosts energy and inspires positivity'},
            {'raga': 'Hamsadhwani', 'description': 'Elevates mood and brings joy'}
        ]
    elif anxiety > 3:  # High anxiety
        return [
            {'raga': 'Bhairavi', 'description': 'Reduces anxiety and brings emotional stability'},
            {'raga': 'Mohanam', 'description': 'Enhances focus and reduces restlessness'}
        ]
    elif stress > 3:  # High stress
        return [
            {'raga': 'Shankarabharanam', 'description': 'Uplifts mood and reduces mental tension'},
            {'raga': 'Anandabhairavi', 'description': 'Relieves stress and promotes peace'}
        ]
    else:  # General well-being
        return [
            {'raga': 'Hamsadhwani', 'description': 'Elevates mood and brings joy'},
            {'raga': 'Kalyani', 'description': 'Boosts energy and inspires positivity'}
        ]

# Route to serve audio files from audio/ folder
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('audio', filename)

UI_CODE = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Roboto', sans-serif;
    line-height: 1.6;
    transition: background 0.3s, color 0.3s;
    overflow-x: hidden;
    min-height: 100vh;
}

.dark-theme {
    background: linear-gradient(135deg, #1e3c72, #000000); /* Blue to black gradient */
    color: #e6e6e6;
}

.light-theme {
    background: linear-gradient(135deg, #a1c4fd, #ffffff); /* Blue to white gradient */
    color: #2c3e50;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 100px 20px 60px 20px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

header {
    position: fixed;
    top: 0;
    width: 100%;
    background: #000000;
    padding: 15px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
}

.light-theme header {
    background: #FFFFFF;
}

.logo {
    font-size: 24px;
    font-weight: 700;
    color: #3498db;
    letter-spacing: 1px;
}

.theme-toggle {
    background: #3498db;
    border: none;
    padding: 8px 20px;
    border-radius: 25px;
    color: white;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s;
    font-size: 18px;
    width: 50px;
    text-align: center;
}

.theme-toggle:hover {
    background: #2980b9;
}

.dark-theme .theme-toggle::before {
    content: '🌙';
}

.light-theme .theme-toggle::before {
    content: '☀️';
}

h1 {
    font-size: 36px;
    font-weight: 700;
    color: #3498db;
    margin-bottom: 20px;
    text-align: center;
}

h3 {
    font-size: 24px;
    font-weight: 500;
    color: #3498db;
    margin-bottom: 15px;
    text-align: center;
}

p {
    font-size: 16px;
    max-width: 600px;
    margin: 0 auto 30px;
}

.btn {
    background: #3498db;
    padding: 12px 30px;
    border: none;
    border-radius: 25px;
    color: white;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
}

.btn:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.btn-container {
    margin-top: auto;
    padding-bottom: 40px;
    text-align: center;
}

.rocket-container {
    position: fixed;
    font-size: 40px;
    animation: rocketLaunch 4s ease-out forwards;
    pointer-events: none;
    z-index: 11;
}

.rocket {
    display: inline-block;
    color: #e74c3c;
    transform: rotate(-135deg); /* Downward-left slant */
}

@keyframes rocketLaunch {
    0% { 
        left: 20px; 
        bottom: 20px; 
        opacity: 1; 
        transform: rotate(135deg) scale(1);
    }
    100% { 
        left: 90vw; 
        bottom: 80vh; 
        opacity: 0; 
        transform: rotate(135deg) scale(1.2);
    }
}

.form-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    border: 1px solid rgba(52, 152, 219, 0.2);
    transition: box-shadow 0.3s;
    text-align: center;
}

.form-box:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.question {
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 15px;
    color: inherit;
}

.star-rating {
    direction: rtl;
    display: inline-block;
}

.star-rating input {
    display: none;
}

.star-rating label {
    font-size: 28px;
    color: #bdc3c7;
    cursor: pointer;
    transition: color 0.2s;
}

.star-rating input:checked ~ label,
.star-rating label:hover,
.star-rating label:hover ~ label {
    color: #f1c40f;
}

.star-blink {
    position: fixed;
    font-size: 20px;
    color: #f1c40f;
    animation: starBlink 1.5s infinite;
}

@keyframes starBlink {
    0% { opacity: 0; transform: scale(0.5); }
    50% { opacity: 1; transform: scale(1.2); }
    100% { opacity: 0; transform: scale(0.5); }
}

.music-notes {
    position: fixed;
    font-size: 40px; /* Bigger size */
    color: #ffffff; /* White color */
    animation: musicFlow 3s ease-out forwards; /* 3s duration */
}

@keyframes musicFlow {
    0% { bottom: 50%; left: 50%; opacity: 1; }
    100% { bottom: 80%; left: 70%; opacity: 0; transform: scale(1.2); }
}

.sound-wave {
    width: 150px;
    height: 150px;
    margin: 30px auto;
    border-radius: 50%;
    background: radial-gradient(circle, #3498db 20%, #8e44ad 60%, #ffffff 100%);
    animation: pulse 2s infinite;
    box-shadow: 0 0 20px rgba(52, 152, 219, 0.5);
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.8; box-shadow: 0 0 20px rgba(52, 152, 219, 0.5); }
    50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 30px rgba(142, 68, 173, 0.7); }
    100% { transform: scale(1); opacity: 0.8; box-shadow: 0 0 20px rgba(52, 152, 219, 0.5); }
}

.media-controls {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
}

.control-btn {
    background: #34495e;
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s;
}

.light-theme .control-btn {
    background: #7f8c8d;
}

.control-btn:hover {
    background: #2c3e50;
}

@media (max-width: 768px) {
    .container {
        padding: 80px 15px 40px 15px;
    }
    
    h1 {
        font-size: 28px;
    }
    
    .form-box {
        padding: 20px;
    }
}
</style>
<script>
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    document.body.classList.toggle('light-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

window.onload = function() {
    const theme = localStorage.getItem('theme') || 'dark';
    document.body.classList.remove('dark-theme', 'light-theme');
    document.body.classList.add(theme + '-theme');
}

function launchRocket() {
    const rocketContainer = document.createElement('div');
    rocketContainer.className = 'rocket-container';
    const rocket = document.createElement('span');
    rocket.className = 'rocket';
    rocket.innerHTML = '🚀';
    rocketContainer.appendChild(rocket);
    document.body.appendChild(rocketContainer);
    setTimeout(() => rocketContainer.remove(), 4000);
}

function triggerStarBlink() {
    for (let i = 0; i < 15; i++) {
        const star = document.createElement('div');
        star.className = 'star-blink';
        star.innerHTML = '★';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDelay = Math.random() * 0.8 + 's';
        document.body.appendChild(star);
        setTimeout(() => star.remove(), 1500);
    }
}

function triggerMusicNotes() {
    for (let i = 0; i < 8; i++) {
        const note = document.createElement('div');
        note.className = 'music-notes';
        note.innerHTML = '🎶';
        note.style.left = (50 + Math.random() * 20 - 10) + '%';
        note.style.animationDelay = (i * 0.2) + 's';
        document.body.appendChild(note);
        setTimeout(() => note.remove(), 3000); /* Remove after 3s */
    }
}

function playRaga(url) {
    triggerMusicNotes(); /* Start the animation */
    setTimeout(() => {
        window.location.href = url; /* Navigate after 3s */
    }, 3000);
}
</script>
"""

# Home Page
@app.route('/')
def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Carnatic Calm</title>{UI_CODE}</head>
    <body class="dark-theme">
        <header>
            <div class="logo">Carnatic Calm</div>
            <button class="theme-toggle" onclick="toggleTheme()"></button>
        </header>
        <div class="container">
            <div>
                <h1>Welcome to Carnatic Calm</h1>
                <p>Discover a revolutionary way to reduce stress and improve sleep with AI-powered Carnatic music therapy. Let the soothing ragas guide you to peace.</p>
            </div>
            <div class="btn-container">
                <button class="btn" onclick="launchRocket(); setTimeout(() => window.location.href='/questionnaire', 2000);">Get Started</button>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# Questionnaire Page
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        stress = int(request.form['stress'])
        sleep = int(request.form['sleep'])
        anxiety = int(request.form['anxiety'])
        energy = int(request.form['energy'])
        ragas = analyze_mood(stress, sleep, anxiety, energy)
        raga_params = '&'.join([f"raga{i}={r['raga']}&desc{i}={r['description']}" for i, r in enumerate(ragas, 1)])
        return redirect(url_for('results') + '?' + raga_params)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Questionnaire - Carnatic Calm</title>{UI_CODE}</head>
    <body class="dark-theme">
        <header>
            <div class="logo">Carnatic Calm</div>
            <button class="theme-toggle" onclick="toggleTheme()"></button>
        </header>
        <div class="container">
            <div>
                <h1>Tell Us How You Feel</h1>
                <form method="POST">
                    <div class="form-box">
                        <div class="question">How stressed do you feel right now?</div>
                        <div class="star-rating" oninput="triggerStarBlink()">
                            <input type="radio" name="stress" value="5" id="s5"><label for="s5">★</label>
                            <input type="radio" name="stress" value="4" id="s4"><label for="s4">★</label>
                            <input type="radio" name="stress" value="3" id="s3"><label for="s3">★</label>
                            <input type="radio" name="stress" value="2" id="s2"><label for="s2">★</label>
                            <input type="radio" name="stress" value="1" id="s1"><label for="s1">★</label>
                        </div>
                    </div>
                    <div class="form-box">
                        <div class="question">How well did you sleep last night?</div>
                        <div class="star-rating" oninput="triggerStarBlink()">
                            <input type="radio" name="sleep" value="5" id="sl5"><label for="sl5">★</label>
                            <input type="radio" name="sleep" value="4" id="sl4"><label for="sl4">★</label>
                            <input type="radio" name="sleep" value="3" id="sl3"><label for="sl3">★</label>
                            <input type="radio" name="sleep" value="2" id="sl2"><label for="sl2">★</label>
                            <input type="radio" name="sleep" value="1" id="sl1"><label for="sl1">★</label>
                        </div>
                    </div>
                    <div class="form-box">
                        <div class="question">How anxious do you feel today?</div>
                        <div class="star-rating" oninput="triggerStarBlink()">
                            <input type="radio" name="anxiety" value="5" id="a5"><label for="a5">★</label>
                            <input type="radio" name="anxiety" value="4" id="a4"><label for="a4">★</label>
                            <input type="radio" name="anxiety" value="3" id="a3"><label for="a3">★</label>
                            <input type="radio" name="anxiety" value="2" id="a2"><label for="a2">★</label>
                            <input type="radio" name="anxiety" value="1" id="a1"><label for="a1">★</label>
                        </div>
                    </div>
                    <div class="form-box">
                        <div class="question">How would you rate your energy levels?</div>
                        <div class="star-rating" oninput="triggerStarBlink()">
                            <input type="radio" name="energy" value="5" id="e5"><label for="e5">★</label>
                            <input type="radio" name="energy" value="4" id="e4"><label for="e4">★</label>
                            <input type="radio" name="energy" value="3" id="e3"><label for="e3">★</label>
                            <input type="radio" name="energy" value="2" id="e2"><label for="e2">★</label>
                            <input type="radio" name="energy" value="1" id="e1"><label for="e1">★</label>
                        </div>
                    </div>
                    <div class="btn-container">
                        <button type="submit" class="btn">Analyze My Mood</button>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# Results Page
@app.route('/results')
def results():
    ragas = []
    for i in range(1, 4):  # Up to 3 ragas
        raga = request.args.get(f'raga{i}')
        desc = request.args.get(f'desc{i}')
        if raga and desc:
            ragas.append({'raga': raga, 'description': desc})
    
    raga_params = {f'raga{i+1}': r['raga'] for i, r in enumerate(ragas)}
    raga_params.update({f'desc{i+1}': r['description'] for i, r in enumerate(ragas)})
    
    raga_html = ''.join([f"""
        <div class="form-box">
            <h3>{raga['raga']}</h3>
            <p>{raga['description']}</p>
            <button class="btn" onclick="playRaga('{url_for('play', raga=raga['raga'], **raga_params)}')">Play Now</button>
        </div>
    """ for raga in ragas])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Results - Carnatic Calm</title>{UI_CODE}</head>
    <body class="dark-theme">
        <header>
            <div class="logo">Carnatic Calm</div>
            <button class="theme-toggle" onclick="toggleTheme()"></button>
        </header>
        <div class="container">
            <div>
                <h1>Your Recommended Ragas</h1>
                {raga_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html

# Music Player Page
@app.route('/play/<raga>')
def play(raga):
    ragas = []
    for i in range(1, 4):  # Up to 3 ragas
        raga_name = request.args.get(f'raga{i}')
        desc = request.args.get(f'desc{i}')
        if raga_name and desc:
            ragas.append({'raga': raga_name, 'description': desc})
    
    current_index = next((i for i, r in enumerate(ragas) if r['raga'] == raga), 0)
    audio_file = f"/audio/{raga}.mp3"
    raga_params = '&'.join([f"raga{i+1}={r['raga']}&desc{i+1}={r['description']}" for i, r in enumerate(ragas)])
    
    prev_index = (current_index - 1) % len(ragas) if ragas else 0
    next_index = (current_index + 1) % len(ragas) if ragas else 0
    prev_url = f"/play/{ragas[prev_index]['raga']}?{raga_params}"
    next_url = f"/play/{ragas[next_index]['raga']}?{raga_params}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Playing {raga} - Carnatic Calm</title>{UI_CODE}</head>
    <body class="dark-theme">
        <header>
            <div class="logo">Carnatic Calm</div>
            <button class="theme-toggle" onclick="toggleTheme()"></button>
        </header>
        <div class="container">
            <div>
                <h1>Now Playing: {raga}</h1>
                <div class="form-box">
                    <audio id="audioPlayer" controls autoplay>
                        <source src="{audio_file}" type="audio/mp3">
                        Your browser does not support the audio element.
                    </audio>
                    <div class="media-controls">
                        <button class="control-btn" onclick="window.location.href='{prev_url}'">Previous</button>
                        <button class="control-btn" onclick="document.getElementById('audioPlayer').play()">Play</button>
                        <button class="control-btn" onclick="document.getElementById('audioPlayer').pause()">Pause</button>
                        <button class="control-btn" onclick="window.location.href='{next_url}'">Next</button>
                    </div>
                </div>
                <div class="sound-wave"></div>
            </div>
            <div class="btn-container">
                <button class="btn" onclick="window.location.href='/'">Back to Home</button>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    if not os.path.exists('audio'):
        os.makedirs('audio')
    app.run(debug=True)