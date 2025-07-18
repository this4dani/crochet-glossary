/* Flashcard functionality for DANI'S Crochet Glossary */

/* Global variables */
let glossaryTerms = [];
let currentCardIndex = 0;
let isFlipped = false;
let studyMode = 'flashcards';

/* API configuration */
const apiEndpoint = 'https://raw.githubusercontent.com/this4dani/crochet-glossary-api/main/glossary.json';

/* Initialize application */
document.addEventListener('DOMContentLoaded', function() {
    loadGlossaryData();
});

/* Navigation scroll behavior */
window.addEventListener('scroll', function() {
    const nav = document.getElementById('nav');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

/* Load glossary data from API */
async function loadGlossaryData() {
    try {
        console.log('Loading glossary data from API...');
        
        const response = await fetch(apiEndpoint);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        /* Handle different data structures */
        glossaryTerms = data.data || data.terms || data || [];
        
        console.log(`Loaded ${glossaryTerms.length} terms from API`);
        
        if (!Array.isArray(glossaryTerms) || glossaryTerms.length === 0) {
            throw new Error('No valid terms found in API response');
        }
        
        /* Filter out invalid terms */
        glossaryTerms = glossaryTerms.filter(term => term && (term.name_us || term.name_uk || term.name));
        
        console.log(`Filtered to ${glossaryTerms.length} valid terms`);
        
        /* Hide loading, show interface */
        document.getElementById('loading').style.display = 'none';
        document.getElementById('flashcard-interface').style.display = 'block';
        
        /* Display first card */
        displayCard();
        updateProgress();
        
    } catch (error) {
        console.error('Error loading glossary data:', error);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
        document.getElementById('error').innerHTML = `
            Unable to load flashcards.<br>
            Error: ${error.message}<br>
            Please check your internet connection.
        `;
    }
}

/* Display current flashcard */
function displayCard() {
    if (glossaryTerms.length === 0) return;
    
    const term = glossaryTerms[currentCardIndex];
    
    /* Front of card: abbreviation and symbol */
    document.getElementById('term-name').textContent = term.id ? term.id.toUpperCase() : 'Unknown';
    document.getElementById('term-description').textContent = term.symbol || '';
    
    /* Back of card: full name and instructions */
    document.getElementById('term-abbreviation').textContent = term.name_us || term.name || 'Unknown Term';
    document.getElementById('back-notes').textContent = term.notes || term.description || term.instruction || 'Practice this technique';
    
    /* Clear translations section */
    const translationsEl = document.getElementById('term-translations');
    if (translationsEl) {
        translationsEl.innerHTML = '';
    }
    
    /* Reset flip state */
    const cardInner = document.getElementById('card-inner');
    cardInner.classList.remove('flipped');
    isFlipped = false;
}

/* Card interaction functions */
window.flipCard = function() {
    const cardInner = document.getElementById('card-inner');
    isFlipped = !isFlipped;
    cardInner.classList.toggle('flipped', isFlipped);
}

window.nextCard = function() {
    currentCardIndex = (currentCardIndex + 1) % glossaryTerms.length;
    displayCard();
    updateProgress();
}

window.previousCard = function() {
    currentCardIndex = currentCardIndex === 0 ? glossaryTerms.length - 1 : currentCardIndex - 1;
    displayCard();
    updateProgress();
}

window.shuffleCards = function() {
    /* Fisher-Yates shuffle algorithm */
    for (let i = glossaryTerms.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [glossaryTerms[i], glossaryTerms[j]] = [glossaryTerms[j], glossaryTerms[i]];
    }
    currentCardIndex = 0;
    displayCard();
    updateProgress();
}

window.markKnown = function() {
    /* Currently just moves to next card */
    nextCard();
}

/* Update progress display */
function updateProgress() {
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    
    if (progressText) {
        progressText.textContent = `Card ${currentCardIndex + 1} of ${glossaryTerms.length}`;
    }
    
    if (progressFill) {
        const percentage = ((currentCardIndex + 1) / glossaryTerms.length) * 100;
        progressFill.style.width = `${percentage}%`;
    }
}

/* Keyboard navigation */
document.addEventListener('keydown', function(e) {
    switch(e.key) {
        case 'ArrowLeft':
            previousCard();
            break;
        case 'ArrowRight':
        case ' ':
            nextCard();
            break;
        case 'ArrowUp':
        case 'ArrowDown':
            flipCard();
            break;
    }
});

/* Study mode management */
window.setStudyMode = function(mode) {
    studyMode = mode;
    
    /* Update active button */
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (mode === 'match' || mode === 'test' || mode === 'quickid') {
        /* Hide regular flashcard layout */
        document.querySelector('.flashcard-layout').style.display = 'none';
        document.querySelector('.progress-info').style.display = 'none';
        
        /* Remove any existing game containers */
        removeGameContainers();
        
        /* Create appropriate game mode */
        if (mode === 'match') {
            createMemoryMatch();
        } else if (mode === 'test') {
            createMultipleChoice();
        } else if (mode === 'quickid') {
            createSpeedRecognition();
        }
    } else {
        /* Show regular flashcard layout */
        document.querySelector('.flashcard-layout').style.display = 'grid';
        document.querySelector('.progress-info').style.display = 'block';
        
        /* Remove any game containers */
        removeGameContainers();
    }
}

/* Remove game containers helper */
function removeGameContainers() {
    const containers = ['match-game-container', 'test-game-container', 'speed-game-container'];
    containers.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.remove();
    });
}

/* Memory match game variables */
let flippedCards = [];
let matchedPairs = 0;
let isChecking = false;

/* Create memory match game */
function createMemoryMatch() {
    /* Create container for match game */
    const gameContainer = document.createElement('div');
    gameContainer.id = 'match-game-container';
    gameContainer.innerHTML = `
        <div style="text-align: center; margin-bottom: 20px; color: var(--clr-warm-white);">
            <h3>Match the stitch name with its description!</h3>
            <p>Matches: <span id="match-score">0</span> / <span id="match-total">6</span></p>
        </div>
        <div id="match-grid" style="
            display: grid;
            grid-template-columns: repeat(auto-fit, 150px);
            gap: 15px;
            justify-content: center;
            margin: 0 auto;
            max-width: 800px;
        "></div>
    `;
    
    /* Insert after study modes buttons */
    document.querySelector('.study-modes').insertAdjacentElement('afterend', gameContainer);
    
    /* Generate 6 random pairs */
    const matchGrid = document.getElementById('match-grid');
    const pairs = [];
    const selectedTerms = [...glossaryTerms].sort(() => 0.5 - Math.random()).slice(0, 6);
    
    /* Create pairs */
    selectedTerms.forEach((term, index) => {
        /* Card with name */
        pairs.push({
            id: `name-${index}`,
            pairId: index,
            content: term.name_us || term.name || 'Unknown',
            type: 'name'
        });
        
        /* Card with description */
        pairs.push({
            id: `desc-${index}`,
            pairId: index,
            content: term.description || term.notes || term.instruction || 'No description',
            type: 'description'
        });
    });
    
    /* Shuffle pairs */
    pairs.sort(() => 0.5 - Math.random());
    
    /* Create cards */
    pairs.forEach(pair => {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.dataset.pairId = pair.pairId;
        card.dataset.cardId = pair.id;
        card.innerHTML = `
            <div class="memory-card-inner" style="
                width: 150px;
                height: 150px;
                position: relative;
                transform-style: preserve-3d;
                transition: transform 0.6s;
                cursor: pointer;
            ">
                <div class="memory-card-front" style="
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    backface-visibility: hidden;
                    background: var(--clr-coral);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 3rem;
                    color: white;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                ">
                    ?
                </div>
                <div class="memory-card-back" style="
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    backface-visibility: hidden;
                    background: var(--clr-cream);
                    border-radius: 12px;
                    transform: rotateY(180deg);
                    padding: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    color: var(--clr-primary-dark);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    font-size: ${pair.type === 'name' ? '1.2rem' : '0.9rem'};
                    font-weight: ${pair.type === 'name' ? '600' : '400'};
                    line-height: 1.4;
                ">
                    ${pair.content}
                </div>
            </div>
        `;
        
        card.addEventListener('click', handleMemoryCardClick);
        matchGrid.appendChild(card);
    });
    
    /* Reset game state */
    flippedCards = [];
    matchedPairs = 0;
    isChecking = false;
}

/* Handle memory card clicks */
function handleMemoryCardClick(e) {
    if (isChecking) return;
    
    const card = e.currentTarget;
    const cardInner = card.querySelector('.memory-card-inner');
    
    /* Don't flip already matched cards */
    if (card.classList.contains('matched')) return;
    
    /* Don't flip the same card twice */
    if (flippedCards.includes(card)) return;
    
    /* Flip the card */
    cardInner.style.transform = 'rotateY(180deg)';
    flippedCards.push(card);
    
    /* Check for match when 2 cards are flipped */
    if (flippedCards.length === 2) {
        isChecking = true;
        
        const [card1, card2] = flippedCards;
        const pairId1 = card1.dataset.pairId;
        const pairId2 = card2.dataset.pairId;
        
        if (pairId1 === pairId2) {
            /* Match found */
            setTimeout(() => {
                card1.classList.add('matched');
                card2.classList.add('matched');
                card1.style.opacity = '0.6';
                card2.style.opacity = '0.6';
                matchedPairs++;
                
                document.getElementById('match-score').textContent = matchedPairs;
                
                if (matchedPairs === 6) {
                    setTimeout(() => {
                        alert('Great job! You matched all the stitches!');
                    }, 500);
                }
                
                flippedCards = [];
                isChecking = false;
            }, 1000);
        } else {
            /* No match - flip back */
            setTimeout(() => {
                card1.querySelector('.memory-card-inner').style.transform = 'rotateY(0deg)';
                card2.querySelector('.memory-card-inner').style.transform = 'rotateY(0deg)';
                flippedCards = [];
                isChecking = false;
            }, 1500);
        }
    }
}

/* Test mode variables */
let currentTestQuestion = 0;
let testScore = 0;
let currentCorrectAnswer = '';

/* Create multiple choice test */
function createMultipleChoice() {
    /* Reset test variables */
    currentTestQuestion = 0;
    testScore = 0;
    
    /* Create test container */
    const testContainer = document.createElement('div');
    testContainer.id = 'test-game-container';
    testContainer.innerHTML = `
        <div style="text-align: center; margin-bottom: 30px; color: var(--clr-warm-white);">
            <h3>Test Your Knowledge!</h3>
            <p>Score: <span id="test-score">0</span> / <span id="test-total">${glossaryTerms.length}</span></p>
            <div style="margin: 20px auto; max-width: 400px;">
                <div style="
                    width: 100%;
                    height: 8px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div id="test-progress-bar" style="
                        width: 0%;
                        height: 100%;
                        background: linear-gradient(90deg, var(--clr-coral), var(--clr-fuchsia));
                        transition: width 0.3s ease;
                    "></div>
                </div>
                <p style="margin-top: 10px; font-size: 0.9rem;">Question <span id="test-current">1</span> of ${glossaryTerms.length}</p>
            </div>
        </div>
        <div id="test-card" style="
            max-width: 600px;
            margin: 0 auto;
            background: var(--clr-cream);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        ">
            <div id="test-question" style="
                font-size: 1.3rem;
                color: var(--clr-primary-dark);
                margin-bottom: 30px;
                text-align: center;
                font-weight: 600;
            "></div>
            <div id="test-options" style="
                display: grid;
                gap: 15px;
            "></div>
        </div>
    `;
    
    /* Insert after study modes */
    document.querySelector('.study-modes').insertAdjacentElement('afterend', testContainer);
    
    /* Start test */
    generateTestQuestion();
}

/* Generate test question */
function generateTestQuestion() {
    if (currentTestQuestion >= glossaryTerms.length) {
        /* Test complete */
        document.getElementById('test-card').innerHTML = `
            <h2 style="text-align: center; color: var(--clr-coral);">Test Complete!</h2>
            <p style="text-align: center; font-size: 1.5rem;">Your score: ${testScore} / ${glossaryTerms.length}</p>
            <button onclick="setStudyMode('flashcards')" style="
                display: block;
                margin: 20px auto;
                padding: 12px 30px;
                background: var(--clr-coral);
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 1rem;
            ">Back to Flashcards</button>
        `;
        return;
    }
    
    /* Update progress */
    document.getElementById('test-current').textContent = currentTestQuestion + 1;
    const progressBar = document.getElementById('test-progress-bar');
    if (progressBar) {
        progressBar.style.width = `${((currentTestQuestion + 1) / glossaryTerms.length) * 100}%`;
    }
    
    /* Pick random term for question */
    const correctTerm = glossaryTerms[Math.floor(Math.random() * glossaryTerms.length)];
    currentCorrectAnswer = correctTerm.name_us || correctTerm.name || 'Unknown';
    
    /* Generate question */
    const questionText = correctTerm.description || correctTerm.notes || correctTerm.instruction || 'No description';
    document.getElementById('test-question').innerHTML = `
        <strong>Question ${currentTestQuestion + 1}:</strong><br>
        Which stitch is described as:<br>
        "${questionText}"
    `;
    
    /* Generate 3 wrong answers */
    const wrongAnswers = glossaryTerms
        .filter(term => term !== correctTerm)
        .sort(() => 0.5 - Math.random())
        .slice(0, 3)
        .map(term => term.name_us || term.name || 'Unknown');
    
    /* Mix correct answer with wrong ones */
    const allAnswers = [...wrongAnswers, currentCorrectAnswer].sort(() => 0.5 - Math.random());
    
    /* Create option buttons */
    const optionsContainer = document.getElementById('test-options');
    optionsContainer.innerHTML = '';
    
    allAnswers.forEach((answer, index) => {
        const button = document.createElement('button');
        button.textContent = answer;
        button.style.cssText = `
            padding: 18px 20px;
            background: transparent;
            border: 2px solid var(--clr-coral);
            color: var(--clr-primary-dark);
            border-radius: 6px;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        `;
        button.onmouseover = () => {
            button.style.background = 'var(--clr-coral)';
            button.style.color = 'white';
        };
        button.onmouseout = () => {
            button.style.background = 'transparent';
            button.style.color = 'var(--clr-primary-dark)';
        };
        button.onclick = () => checkAnswer(answer, button);
        optionsContainer.appendChild(button);
    });
}

/* Check test answer */
function checkAnswer(answer, button) {
    /* Disable all buttons */
    const allButtons = document.querySelectorAll('#test-options button');
    allButtons.forEach(btn => {
        btn.disabled = true;
        btn.style.cursor = 'default';
    });
    
    if (answer === currentCorrectAnswer) {
        /* Correct */
        button.style.background = '#4CAF50';
        button.style.borderColor = '#4CAF50';
        button.style.color = 'white';
        testScore++;
        document.getElementById('test-score').textContent = testScore;
    } else {
        /* Wrong */
        button.style.background = '#f44336';
        button.style.borderColor = '#f44336';
        button.style.color = 'white';
        
        /* Show correct answer */
        allButtons.forEach(btn => {
            if (btn.textContent === currentCorrectAnswer) {
                btn.style.background = '#4CAF50';
                btn.style.borderColor = '#4CAF50';
                btn.style.color = 'white';
            }
        });
    }
    
    /* Next question after delay */
    currentTestQuestion++;
    setTimeout(() => {
        generateTestQuestion();
    }, 2000);
}

/* Speed recognition variables */
let speedScore = 0;
let speedLives = 3;
let speedTimeLimit = 3.0;
let speedTimer = null;
let speedRound = 0;
let speedCurrentAnswer = '';

/* Create speed recognition game */
function createSpeedRecognition() {
    /* Reset speed variables */
    speedScore = 0;
    speedLives = 3;
    speedTimeLimit = 3.0;
    speedRound = 0;
    if (speedTimer) clearInterval(speedTimer);
    
    /* Create game container */
    const speedContainer = document.createElement('div');
    speedContainer.id = 'speed-game-container';
    speedContainer.innerHTML = `
        <div style="text-align: center; margin-bottom: 20px; color: var(--clr-warm-white);">
            <h3>Quick ID Challenge!</h3>
            <p>Identify stitches as fast as you can!</p>
            <p>Score: <span id="speed-score">0</span> | Lives: <span id="speed-lives">❤️❤️❤️</span></p>
            <p>Time: <span id="speed-timer">3.0</span> seconds</p>
        </div>
        <div id="speed-flash-card" style="
            max-width: 300px;
            margin: 0 auto 20px;
            background: var(--clr-cream);
            border-radius: 15px;
            padding: 30px 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            text-align: center;
        ">
            <p style="margin: 0 0 5px 0; color: var(--clr-primary-dark); font-size: 0.9rem; opacity: 0.8;">What stitch is this?</p>
            <div id="speed-symbol" style="
                font-size: 3rem;
                color: var(--clr-coral);
                font-weight: 800;
            "></div>
        </div>
        <div id="speed-options" style="
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            max-width: 500px;
            margin: 0 auto;
        "></div>
    `;
    
    /* Insert after study modes */
    document.querySelector('.study-modes').insertAdjacentElement('afterend', speedContainer);
    
    /* Start game */
    startSpeedRound();
}

/* Start a speed recognition round */
function startSpeedRound() {
    if (speedLives <= 0) {
        /* Game over */
        document.getElementById('speed-flash-card').innerHTML = `
            <h2 style="color: var(--clr-coral); margin: 0 0 15px 0;">Game Over!</h2>
            <p style="font-size: 1.3rem; margin: 0;">Final Score: ${speedScore}</p>
        `;
        document.getElementById('speed-options').innerHTML = `
            <button onclick="setStudyMode('flashcards')" style="
                grid-column: span 2;
                padding: 12px 25px;
                background: var(--clr-coral);
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 1rem;
            ">Back to Flashcards</button>
        `;
        return;
    }
    
    /* Pick random term */
    const correctTerm = glossaryTerms[Math.floor(Math.random() * glossaryTerms.length)];
    speedCurrentAnswer = correctTerm.name_us || correctTerm.name || 'Unknown';
    
    /* Show abbreviation or symbol */
    const flashContent = correctTerm.abbreviation || correctTerm.symbol || correctTerm.id || '?';
    document.getElementById('speed-symbol').textContent = flashContent.toUpperCase();
    
    /* Generate wrong answers */
    const wrongAnswers = glossaryTerms
        .filter(term => term !== correctTerm)
        .sort(() => 0.5 - Math.random())
        .slice(0, 3)
        .map(term => term.name_us || term.name || 'Unknown');
    
    /* Mix answers */
    const allAnswers = [...wrongAnswers, speedCurrentAnswer].sort(() => 0.5 - Math.random());
    
    /* Create option buttons */
    const optionsContainer = document.getElementById('speed-options');
    optionsContainer.innerHTML = '';
    
    allAnswers.forEach(answer => {
        const button = document.createElement('button');
        button.textContent = answer;
        button.style.cssText = `
            padding: 15px 20px;
            background: var(--clr-cream);
            border: 2px solid var(--clr-coral);
            color: var(--clr-primary-dark);
            border-radius: 6px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        `;
        button.onmouseover = () => {
            button.style.background = 'var(--clr-coral)';
            button.style.color = 'white';
            button.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
        };
        button.onmouseout = () => {
            button.style.background = 'var(--clr-cream)';
            button.style.color = 'var(--clr-primary-dark)';
            button.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
        };
        button.onclick = () => checkSpeedAnswer(answer);
        optionsContainer.appendChild(button);
    });
    
    /* Start timer */
    startSpeedTimer();
}

/* Start countdown timer */
function startSpeedTimer() {
    let timeLeft = speedTimeLimit;
    const timerDisplay = document.getElementById('speed-timer');
    
    /* Reset timer styling */
    timerDisplay.style.color = '';
    timerDisplay.style.fontWeight = '';
    
    /* Clear any existing timer */
    if (speedTimer) clearInterval(speedTimer);
    
    speedTimer = setInterval(() => {
        timeLeft -= 0.1;
        timerDisplay.textContent = timeLeft.toFixed(1);
        
        /* Add urgency styling when time is low */
        if (timeLeft <= 1.0) {
            timerDisplay.style.color = '#f44336';
            timerDisplay.style.fontWeight = 'bold';
        }
        
        if (timeLeft <= 0) {
            clearInterval(speedTimer);
            checkSpeedAnswer(null);
        }
    }, 100);
}

/* Check speed answer */
function checkSpeedAnswer(answer) {
    /* Stop timer */
    if (speedTimer) clearInterval(speedTimer);
    
    /* Disable buttons */
    const buttons = document.querySelectorAll('#speed-options button');
    buttons.forEach(btn => btn.disabled = true);
    
    if (answer === speedCurrentAnswer) {
        /* Correct */
        speedScore++;
        document.getElementById('speed-score').textContent = speedScore;
        
        /* Speed up for next round */
        speedTimeLimit = Math.max(0.5, speedTimeLimit - 0.1);
        
        /* Flash green */
        document.getElementById('speed-flash-card').style.background = '#c8e6c9';
    } else {
        /* Wrong or timeout */
        speedLives--;
        const livesDisplay = document.getElementById('speed-lives');
        livesDisplay.textContent = '❤️'.repeat(speedLives) + '💔'.repeat(3 - speedLives);
        
        /* Flash red */
        document.getElementById('speed-flash-card').style.background = '#ffcdd2';
        
        /* Show correct answer */
        buttons.forEach(btn => {
            if (btn.textContent === speedCurrentAnswer) {
                btn.style.background = '#4CAF50';
                btn.style.borderColor = '#4CAF50';
                btn.style.color = 'white';
            } else {
                btn.style.opacity = '0.5';
            }
        });
    }
    
    /* Next round after delay */
    speedRound++;
    setTimeout(() => {
        document.getElementById('speed-flash-card').style.background = 'var(--clr-cream)';
        startSpeedRound();
    }, 1500);
}