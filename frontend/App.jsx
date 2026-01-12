import { useState } from 'react';

// ==================== STYLES ====================
const styles = `
  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  }

  .app-container {
    min-height: 100vh;
    background: linear-gradient(to bottom right, #eff6ff, #e0e7ff);
  }

  .flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 1rem;
  }

  .home-card {
    max-width: 42rem;
    width: 100%;
    background: white;
    border-radius: 1rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    padding: 2rem;
    text-align: center;
  }

  .emoji-large {
    font-size: 3.75rem;
    margin-bottom: 1.5rem;
  }

  .title-large {
    font-size: 2.25rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 1rem;
  }

  .text-body {
    font-size: 1.125rem;
    color: #4b5563;
    margin-bottom: 2rem;
  }

  .info-box {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 1rem;
    margin-bottom: 2rem;
    text-align: left;
  }

  .info-box p {
    font-size: 0.875rem;
    color: #1e3a8a;
    margin: 0;
  }

  .btn-primary {
    background: #4f46e5;
    color: white;
    font-weight: bold;
    padding: 1rem 2rem;
    border-radius: 0.5rem;
    font-size: 1.25rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }

  .btn-primary:hover {
    background: #4338ca;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  }

  .btn-secondary {
    background: #4b5563;
    color: white;
    font-weight: bold;
    padding: 0.75rem 2rem;
    border-radius: 0.5rem;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-secondary:hover {
    background: #374151;
  }

  .btn-success {
    background: #16a34a;
    color: white;
    font-weight: bold;
    padding: 0.75rem 2rem;
    border-radius: 0.5rem;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-success:hover {
    background: #15803d;
  }

  .btn-disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }

  .assessment-container {
    min-height: 100vh;
    padding: 1rem;
    padding-top: 2rem;
    padding-bottom: 2rem;
  }

  .assessment-content {
    max-width: 48rem;
    margin: 0 auto;
  }

  .progress-card {
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    margin-bottom: 1.5rem;
  }

  .progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .progress-text {
    font-size: 0.875rem;
    font-weight: 600;
    color: #4b5563;
  }

  .progress-current {
    font-size: 0.875rem;
    font-weight: 600;
    color: #4f46e5;
  }

  .progress-bar-bg {
    width: 100%;
    background: #e5e7eb;
    border-radius: 9999px;
    height: 0.5rem;
  }

  .progress-bar-fill {
    background: #4f46e5;
    height: 0.5rem;
    border-radius: 9999px;
    transition: width 0.3s;
  }

  .test-card {
    background: white;
    border-radius: 1rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    padding: 2rem;
  }

  .test-title {
    font-size: 1.875rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 1rem;
    text-align: center;
  }

  .test-description {
    color: #4b5563;
    margin-bottom: 2rem;
    text-align: center;
  }

  .jumbled-container {
    background: #eef2ff;
    border-radius: 0.75rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .jumbled-label {
    font-size: 0.875rem;
    color: #4b5563;
    margin-bottom: 0.5rem;
  }

  .jumbled-word {
    font-size: 3rem;
    font-weight: bold;
    color: #4f46e5;
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
  }

  .input-large {
    width: 100%;
    max-width: 28rem;
    padding: 1rem 1.5rem;
    font-size: 1.5rem;
    text-align: center;
    border: 2px solid #a5b4fc;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
  }

  .input-large:focus {
    outline: none;
    border-color: #4f46e5;
  }

  .result-container {
    text-align: center;
  }

  .emoji-result {
    font-size: 3.75rem;
    margin-bottom: 1rem;
  }

  .result-text {
    font-size: 1.25rem;
    color: #374151;
    margin-bottom: 1rem;
  }

  .score-large {
    font-size: 1.875rem;
    font-weight: bold;
    color: #4f46e5;
  }

  .instructions-box {
    background: #eff6ff;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .instructions-title {
    font-size: 1.125rem;
    color: #374151;
    margin-bottom: 1rem;
  }

  .instructions-list {
    text-align: left;
    max-width: 28rem;
    margin: 0 auto;
    list-style: none;
    padding: 0;
  }

  .instructions-list li {
    color: #374151;
    margin-bottom: 0.5rem;
  }

  .level-display {
    font-size: 1.5rem;
    font-weight: bold;
    color: #4f46e5;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .status-text {
    font-size: 1.125rem;
    color: #4b5563;
    margin-top: 0.5rem;
    text-align: center;
  }

  .memory-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    max-width: 28rem;
    margin: 0 auto 1.5rem;
  }

  .memory-box {
    aspect-ratio: 1;
    border-radius: 0.75rem;
    font-size: 1.875rem;
    font-weight: bold;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    background: #c7d2fe;
  }

  .memory-box:hover:not(:disabled) {
    background: #a5b4fc;
  }

  .memory-box.active {
    background: #fbbf24;
    transform: scale(1.1);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }

  .memory-box:disabled {
    cursor: not-allowed;
  }

  .complete-box {
    background: #ecfdf5;
    padding: 1.5rem;
    border-radius: 0.75rem;
    text-align: center;
  }

  .complete-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 0.5rem;
  }

  .reaction-area {
    min-height: 24rem;
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s;
  }

  .reaction-ready {
    background: #dbeafe;
  }

  .reaction-ready:hover {
    background: #bfdbfe;
  }

  .reaction-waiting {
    background: #fee2e2;
  }

  .reaction-click {
    background: #4ade80;
  }

  .reaction-result {
    background: #f3f4f6;
  }

  .reaction-prompt {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1f2937;
  }

  .reaction-wait {
    font-size: 1.875rem;
    font-weight: bold;
    color: #dc2626;
  }

  .reaction-now {
    font-size: 3.75rem;
    font-weight: bold;
    color: white;
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  .reaction-time {
    font-size: 3rem;
    font-weight: bold;
    color: #4f46e5;
  }

  .button-group {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .audio-container {
    background: #f9fafb;
    border-radius: 0.75rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .file-input {
    display: none;
  }

  .file-label {
    background: #4f46e5;
    color: white;
    font-weight: bold;
    padding: 0.75rem 2rem;
    border-radius: 0.5rem;
    cursor: pointer;
    display: inline-block;
    transition: background 0.2s;
  }

  .file-label:hover {
    background: #4338ca;
  }

  .file-selected {
    background: #ecfdf5;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
  }

  .file-selected p {
    color: #065f46;
    margin: 0;
  }

  .file-info {
    font-size: 0.875rem;
    color: #4b5563;
    margin-top: 0.25rem;
  }

  .error-box {
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    padding: 1rem;
    margin-bottom: 1.5rem;
    border-radius: 0.25rem;
  }

  .error-text {
    color: #991b1b;
    margin: 0;
  }

  .warning-box {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    padding: 1rem;
    margin-top: 1.5rem;
    border-radius: 0.25rem;
  }

  .warning-text {
    color: #78350f;
    font-size: 0.875rem;
    font-weight: 600;
    margin: 0;
  }

  .results-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }

  .results-card {
    max-width: 48rem;
    width: 100%;
    background: white;
    border-radius: 1rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    padding: 2rem;
  }

  .results-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .results-title {
    font-size: 2.25rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 0.5rem;
  }

  .results-subtitle {
    color: #4b5563;
  }

  .risk-container {
    background: linear-gradient(to bottom right, #eef2ff, #faf5ff);
    border-radius: 0.75rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
  }

  .risk-score-section {
    text-align: center;
    margin-bottom: 1.5rem;
  }

  .risk-label {
    font-size: 1.125rem;
    color: #4b5563;
    margin-bottom: 0.5rem;
  }

  .risk-score {
    font-size: 4.5rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 1rem;
  }

  .risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 2rem;
    border-radius: 9999px;
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
  }

  .breakdown-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    margin-top: 2rem;
  }

  @media (min-width: 768px) {
    .breakdown-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .breakdown-item {
    background: white;
    border-radius: 0.5rem;
    padding: 1rem;
    text-align: center;
  }

  .breakdown-label {
    font-size: 0.875rem;
    color: #4b5563;
    margin-bottom: 0.5rem;
  }

  .breakdown-value {
    font-size: 1.875rem;
    font-weight: bold;
    color: #4f46e5;
  }

  .disclaimer-box {
    background: #fefce8;
    border-left: 4px solid #facc15;
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .disclaimer-text {
    font-size: 0.875rem;
    color: #713f12;
    line-height: 1.6;
    margin: 0;
  }

  .space-y-4 > * + * {
    margin-top: 1rem;
  }

  .space-y-6 > * + * {
    margin-top: 1.5rem;
  }
`;

// ==================== MAIN APP ====================
export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [assessmentData, setAssessmentData] = useState({
    wordScore: 0,
    memoryScore: 0,
    reactionTime: 0,
    audioFile: null
  });
  const [apiResult, setApiResult] = useState(null);

  const updateAssessmentData = (key, value) => {
    setAssessmentData(prev => ({ ...prev, [key]: value }));
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onStart={() => setCurrentPage('assessment')} />;
      case 'assessment':
        return (
          <AssessmentPage
            assessmentData={assessmentData}
            updateAssessmentData={updateAssessmentData}
            onComplete={(result) => {
              setApiResult(result);
              setCurrentPage('results');
            }}
          />
        );
      case 'results':
        return (
          <ResultsPage
            result={apiResult}
            onRestart={() => {
              setCurrentPage('home');
              setAssessmentData({
                wordScore: 0,
                memoryScore: 0,
                reactionTime: 0,
                audioFile: null
              });
              setApiResult(null);
            }}
          />
        );
      default:
        return <HomePage onStart={() => setCurrentPage('assessment')} />;
    }
  };

  return (
    <>
      <style>{styles}</style>
      <div className="app-container">{renderPage()}</div>
    </>
  );
}

// ==================== HOME PAGE ====================
function HomePage({ onStart }) {
  return (
    <div className="flex-center">
      <div className="home-card">
        <div className="emoji-large">🧠</div>
        <h1 className="title-large">AI Dementia Screening</h1>
        <p className="text-body">
          Complete a series of cognitive assessments to evaluate your cognitive health.
          This screening includes memory tests, reaction time measurements, and pattern recognition tasks.
        </p>
        <div className="info-box">
          <p>
            <strong>Important:</strong> This is a screening tool only and not a medical diagnosis.
            Results should be discussed with a healthcare professional.
          </p>
        </div>
        <button onClick={onStart} className="btn-primary">
          Start Assessment
        </button>
      </div>
    </div>
  );
}

// ==================== ASSESSMENT PAGE ====================
function AssessmentPage({ assessmentData, updateAssessmentData, onComplete }) {
  const [currentTest, setCurrentTest] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const tests = ['jumbled', 'memory', 'reaction', 'audio'];

  const handleTestComplete = (key, value) => {
    updateAssessmentData(key, value);
    if (currentTest < tests.length - 1) {
      setCurrentTest(currentTest + 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('word_score', assessmentData.wordScore);
      formData.append('memory_score', assessmentData.memoryScore);
      formData.append('reaction_time', assessmentData.reactionTime);
      
      if (assessmentData.audioFile) {
        formData.append('audio_file', assessmentData.audioFile);
      }

      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      onComplete(data);
    } catch (err) {
      setError(err.message || 'Failed to submit assessment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderTest = () => {
    switch (tests[currentTest]) {
      case 'jumbled':
        return <JumbledWordTest onComplete={(score) => handleTestComplete('wordScore', score)} />;
      case 'memory':
        return <MemoryTest onComplete={(score) => handleTestComplete('memoryScore', score)} />;
      case 'reaction':
        return <ReactionTest onComplete={(time) => handleTestComplete('reactionTime', time)} />;
      case 'audio':
        return (
          <AudioUpload
            onComplete={(file) => {
              updateAssessmentData('audioFile', file);
            }}
            onSubmit={handleSubmit}
            loading={loading}
            error={error}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="assessment-container">
      <div className="assessment-content">
        <div className="progress-card">
          <div className="progress-header">
            <span className="progress-text">Assessment Progress</span>
            <span className="progress-current">
              Step {currentTest + 1} of {tests.length}
            </span>
          </div>
          <div className="progress-bar-bg">
            <div
              className="progress-bar-fill"
              style={{ width: `${((currentTest + 1) / tests.length) * 100}%` }}
            ></div>
          </div>
        </div>

        <div className="test-card">{renderTest()}</div>
      </div>
    </div>
  );
}

// ==================== JUMBLED WORD TEST ====================
function JumbledWordTest({ onComplete }) {
  const words = ['COGNITIVE', 'MEMORY', 'REACTION', 'PATTERN', 'HEALTH'];
  const [originalWord] = useState(words[Math.floor(Math.random() * words.length)]);
  const [jumbledWord] = useState(
    originalWord
      .split('')
      .sort(() => Math.random() - 0.5)
      .join('')
  );
  const [userInput, setUserInput] = useState('');
  const [completed, setCompleted] = useState(false);
  const [score, setScore] = useState(0);

  const calculateSimilarity = (str1, str2) => {
    const longer = str1.length > str2.length ? str1 : str2;
    const shorter = str1.length > str2.length ? str2 : str1;
    if (longer.length === 0) return 100;
    
    const editDistance = levenshteinDistance(longer.toLowerCase(), shorter.toLowerCase());
    return Math.round(((longer.length - editDistance) / longer.length) * 100);
  };

  const levenshteinDistance = (str1, str2) => {
    const matrix = [];
    for (let i = 0; i <= str2.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= str1.length; j++) {
      matrix[0][j] = j;
    }
    for (let i = 1; i <= str2.length; i++) {
      for (let j = 1; j <= str1.length; j++) {
        if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    return matrix[str2.length][str1.length];
  };

  const handleSubmit = () => {
    const similarity = calculateSimilarity(originalWord, userInput);
    setScore(similarity);
    setCompleted(true);
  };

  const handleNext = () => {
    onComplete(score);
  };

  return (
    <div>
      <h2 className="test-title">Word Unscrambling Test</h2>
      <p className="test-description">Unscramble the letters to form a valid word</p>

      <div className="jumbled-container">
        <p className="jumbled-label">Scrambled Word:</p>
        <p className="jumbled-word">{jumbledWord}</p>

        {!completed ? (
          <>
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value.toUpperCase())}
              placeholder="Type your answer"
              className="input-large"
              autoFocus
            />
            <button
              onClick={handleSubmit}
              disabled={!userInput}
              className={`btn-primary ${!userInput ? 'btn-disabled' : ''}`}
            >
              Submit Answer
            </button>
          </>
        ) : (
          <div className="space-y-4">
            <div className="emoji-result">{score >= 70 ? '✅' : score >= 40 ? '⚠️' : '❌'}</div>
            <p className="result-text">
              Your answer: <strong>{userInput}</strong>
            </p>
            <p className="result-text">
              Correct word: <strong>{originalWord}</strong>
            </p>
            <p className="score-large">Score: {score}/100</p>
            <button onClick={handleNext} className="btn-success" style={{ marginTop: '1rem' }}>
              Continue to Next Test
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// ==================== MEMORY TEST ====================
function MemoryTest({ onComplete }) {
  const [sequence, setSequence] = useState([]);
  const [userSequence, setUserSequence] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeBox, setActiveBox] = useState(null);
  const [level, setLevel] = useState(1);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [maxLevel, setMaxLevel] = useState(0);

  const gridSize = 9;

  const startGame = () => {
    setGameStarted(true);
    setLevel(1);
    setMaxLevel(0);
    setGameOver(false);
    startNewRound(1);
  };

  const startNewRound = (currentLevel) => {
    const newSequence = Array.from({ length: currentLevel }, () =>
      Math.floor(Math.random() * gridSize)
    );
    setSequence(newSequence);
    setUserSequence([]);
    playSequence(newSequence);
  };

  const playSequence = async (seq) => {
    setIsPlaying(true);
    for (let i = 0; i < seq.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      setActiveBox(seq[i]);
      await new Promise((resolve) => setTimeout(resolve, 600));
      setActiveBox(null);
    }
    setIsPlaying(false);
  };

  const handleBoxClick = (index) => {
    if (isPlaying || gameOver) return;

    const newUserSequence = [...userSequence, index];
    setUserSequence(newUserSequence);

    setActiveBox(index);
    setTimeout(() => setActiveBox(null), 300);

    if (newUserSequence[newUserSequence.length - 1] !== sequence[newUserSequence.length - 1]) {
      setGameOver(true);
      setMaxLevel(level - 1);
      return;
    }

    if (newUserSequence.length === sequence.length) {
      const nextLevel = level + 1;
      if (nextLevel > 9) {
        setGameOver(true);
        setMaxLevel(9);
      } else {
        setLevel(nextLevel);
        setTimeout(() => startNewRound(nextLevel), 1000);
      }
    }
  };

  const handleFinish = () => {
    onComplete(Math.min(maxLevel, 9));
  };

  return (
    <div>
      <h2 className="test-title">Memory Pattern Test</h2>
      <p className="test-description">Watch the sequence and repeat it by clicking the boxes</p>

      {!gameStarted ? (
        <div className="space-y-6">
          <div className="instructions-box">
            <p className="instructions-title">
              <strong>Instructions:</strong>
            </p>
            <ul className="instructions-list">
              <li>• Watch the boxes light up in sequence</li>
              <li>• Repeat the sequence by clicking the boxes</li>
              <li>• Each level adds one more box to remember</li>
              <li>• The test ends when you make a mistake</li>
            </ul>
          </div>
          <div style={{ textAlign: 'center' }}>
            <button onClick={startGame} className="btn-primary">
              Start Test
            </button>
          </div>
        </div>
      ) : (
        <>
          <div style={{ marginBottom: '1.5rem' }}>
            <p className="level-display">Level: {level}</p>
            {isPlaying && <p className="status-text">Watch carefully...</p>}
            {!isPlaying && !gameOver && (
              <p className="status-text">Your turn! ({userSequence.length}/{sequence.length})</p>
            )}
          </div>

          <div className="memory-grid">
            {Array.from({ length: gridSize }).map((_, index) => (
              <button
                key={index}
                onClick={() => handleBoxClick(index)}
                disabled={isPlaying || gameOver}
                className={`memory-box ${activeBox === index ? 'active' : ''}`}
              >
                {index + 1}
              </button>
            ))}
          </div>

          {gameOver && (
            <div className="complete-box">
              <div className="emoji-result">🎯</div>
              <p className="complete-title">Test Complete!</p>
              <p className="result-text">
                Maximum Level Reached: <strong>{maxLevel}</strong>
              </p>
              <p className="score-large">Memory Score: {Math.min(maxLevel, 9)}/9</p>
              <button onClick={handleFinish} className="btn-success">
                Continue to Next Test
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
function ReactionTest({ onComplete }) {
  const [stage, setStage] = useState('ready');
  const [startTime, setStartTime] = useState(0);
  const [reactionTime, setReactionTime] = useState(0);
  const [tooEarly, setTooEarly] = useState(false);

  const startTest = () => {
    setStage('waiting');
    setTooEarly(false);
    const delay = 2000 + Math.random() * 3000;
    setTimeout(() => {
      setStartTime(Date.now());
      setStage('click');
    }, delay);
  };

  const handleClick = () => {
    if (stage === 'waiting') {
      setTooEarly(true);
      setStage('ready');
    } else if (stage === 'click') {
      const time = Date.now() - startTime;
      setReactionTime(time);
      setStage('result');
    }
  };

  return (
    <div>
      <h2 className="test-title">Reaction Time Test</h2>
      <p className="test-description">Click as fast as you can when prompted</p>

      <div
        onClick={handleClick}
        className={`reaction-area ${
          stage === 'ready'
            ? 'reaction-ready'
            : stage === 'waiting'
            ? 'reaction-waiting'
            : stage === 'click'
            ? 'reaction-click'
            : 'reaction-result'
        }`}
      >
        {stage === 'ready' && (
          <button onClick={startTest} className="btn-primary">
            Start Test
          </button>
        )}

        {stage === 'waiting' && <p className="reaction-wait">WAIT...</p>}

        {stage === 'click' && <p className="reaction-now">CLICK NOW</p>}

        {stage === 'result' && (
          <div className="result-container">
            <p className="reaction-time">{reactionTime} ms</p>
            <div className="button-group">
              <button onClick={() => onComplete(reactionTime)} className="btn-success">
                Continue
              </button>
            </div>
          </div>
        )}
      </div>

      {tooEarly && (
        <div className="error-box">
          <p className="error-text">Too early! Wait for the signal.</p>
        </div>
      )}
    </div>
  );
}
function AudioUpload({ onComplete, onSubmit, loading, error }) {
  const [file, setFile] = useState(null);

  const handleChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.name.endsWith('.wav')) {
      setFile(selected);
      onComplete(selected);
    } else {
      alert('Please upload a WAV file only');
    }
  };

  return (
    <div>
      <h2 className="test-title">Speech Sample (Optional)</h2>
      <p className="test-description">Upload a WAV audio file</p>

      <div className="audio-container">
        <input type="file" accept=".wav" onChange={handleChange} className="file-input" id="audio" />
        <label htmlFor="audio" className="file-label">
          Choose WAV File
        </label>

        {file && (
          <div className="file-selected">
            <p>Selected: {file.name}</p>
            <p className="file-info">{(file.size / 1024).toFixed(2)} KB</p>
          </div>
        )}
      </div>

      {error && (
        <div className="error-box">
          <p className="error-text">{error}</p>
        </div>
      )}

      <div className="button-group">
        <button onClick={onSubmit} disabled={loading} className="btn-success">
          {loading ? 'Submitting...' : 'Submit Assessment'}
        </button>
      </div>
    </div>
  );
}
function ResultsPage({ result, onRestart }) {
  const color =
    result.risk_category === 'Low Risk'
      ? '#16a34a'
      : result.risk_category === 'Moderate Risk'
      ? '#f59e0b'
      : '#dc2626';

  return (
    <div className="results-container">
      <div className="results-card">
        <div className="results-header">
          <h1 className="results-title">Assessment Results</h1>
          <p className="results-subtitle">Screening Summary</p>
        </div>

        <div className="risk-container">
          <div className="risk-score-section">
            <p className="risk-label">Overall Risk Score</p>
            <p className="risk-score">{result.risk_score}%</p>
            <div className="risk-badge" style={{ backgroundColor: color }}>
              {result.risk_category}
            </div>
          </div>

          <div className="breakdown-grid">
            <div className="breakdown-item">
              <p className="breakdown-label">Cognitive Risk</p>
              <p className="breakdown-value">{result.cognitive_risk}%</p>
            </div>
            <div className="breakdown-item">
              <p className="breakdown-label">Speech Analysis</p>
              <p className="breakdown-value">
                {result.speech_analyzed ? 'Included' : 'Not Provided'}
              </p>
            </div>
          </div>
        </div>

        <div className="disclaimer-box">
          <p className="disclaimer-text">
            This tool is for screening purposes only and does not provide a medical diagnosis.
            Please consult a healthcare professional for clinical evaluation.
          </p>
        </div>

        <div className="button-group">
          <button onClick={onRestart} className="btn-primary">
            Restart Assessment
          </button>
        </div>
      </div>
    </div>
  );
}