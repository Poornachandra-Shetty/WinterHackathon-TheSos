"use client"

import { useState, useEffect } from "react"
import { CheckCircle, XCircle, AlertTriangle, ArrowRight, Sparkles } from "../components/Icons"

const words = ["COGNITIVE", "MEMORY", "REACTION", "PATTERN", "HEALTH"]

export default function JumbledWordTest({ onComplete }) {
  const [originalWord] = useState(() => words[Math.floor(Math.random() * words.length)])
  const [jumbledWord] = useState(() =>
    originalWord
      .split("")
      .sort(() => Math.random() - 0.5)
      .join(""),
  )
  const [userInput, setUserInput] = useState("")
  const [completed, setCompleted] = useState(false)
  const [score, setScore] = useState(0)
  const [showLetters, setShowLetters] = useState(false)

  useEffect(() => {
    setTimeout(() => setShowLetters(true), 100)
  }, [])

  const calculateSimilarity = (str1, str2) => {
    const longer = str1.length > str2.length ? str1 : str2
    const shorter = str1.length > str2.length ? str2 : str1
    if (longer.length === 0) return 100

    const editDistance = levenshteinDistance(longer.toLowerCase(), shorter.toLowerCase())
    return Math.round(((longer.length - editDistance) / longer.length) * 100)
  }

  const levenshteinDistance = (str1, str2) => {
    const matrix = []
    for (let i = 0; i <= str2.length; i++) {
      matrix[i] = [i]
    }
    for (let j = 0; j <= str1.length; j++) {
      matrix[0][j] = j
    }
    for (let i = 1; i <= str2.length; i++) {
      for (let j = 1; j <= str1.length; j++) {
        if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1]
        } else {
          matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
        }
      }
    }
    return matrix[str2.length][str1.length]
  }

  const handleSubmit = () => {
    const similarity = calculateSimilarity(originalWord, userInput)
    setScore(similarity)
    setCompleted(true)
  }

  const getResultIcon = () => {
    if (score >= 70) return <CheckCircle className="h-16 w-16 text-success animate-bounce-in" />
    if (score >= 40) return <AlertTriangle className="h-16 w-16 text-warning animate-bounce-in" />
    return <XCircle className="h-16 w-16 text-destructive animate-shake" />
  }

  return (
    <div className="text-center">
      <div className="mb-2 flex items-center justify-center gap-2">
        <Sparkles className="h-6 w-6 text-primary animate-pulse-slow" />
        <h2 className="text-2xl font-bold text-foreground md:text-3xl">Word Unscrambling Test</h2>
      </div>
      <p className="mb-8 text-muted-foreground">Unscramble the letters to form a valid word</p>

      <div className="mb-8 rounded-2xl bg-gradient-to-br from-indigo-50 to-purple-50 p-8">
        <p className="mb-4 text-sm font-medium text-muted-foreground">Scrambled Word:</p>

        {/* Animated Letters */}
        <div className="mb-8 flex flex-wrap justify-center gap-2">
          {jumbledWord.split("").map((letter, index) => (
            <span
              key={index}
              className={`animate-letter-pop stagger-${index + 1} opacity-0 inline-flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-2xl font-bold text-white shadow-lg transition-transform duration-200 hover:scale-110 hover:-rotate-6 md:h-16 md:w-16 md:text-3xl ${showLetters ? "" : "invisible"}`}
            >
              {letter}
            </span>
          ))}
        </div>

        {!completed ? (
          <div className="space-y-4">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value.toUpperCase())}
              placeholder="Type your answer..."
              className="input mx-auto max-w-sm"
              autoFocus
              onKeyDown={(e) => e.key === "Enter" && userInput && handleSubmit()}
            />
            <div>
              <button onClick={handleSubmit} disabled={!userInput} className="btn btn-primary">
                Submit Answer
              </button>
            </div>
          </div>
        ) : (
          <div className="animate-fade-in space-y-6">
            <div className="flex justify-center">{getResultIcon()}</div>

            <div className="space-y-2">
              <p className="text-lg text-muted-foreground">
                Your answer:{" "}
                <span
                  className={`font-bold ${score >= 70 ? "text-success" : score >= 40 ? "text-warning" : "text-destructive"}`}
                >
                  {userInput}
                </span>
              </p>
              <p className="text-lg text-muted-foreground">
                Correct word: <span className="font-bold text-foreground">{originalWord}</span>
              </p>
            </div>

            <div className="animate-scale-in">
              <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-6 py-3">
                <span className="text-lg text-muted-foreground">Score:</span>
                <span className="text-3xl font-bold text-primary">{score}/100</span>
              </div>
            </div>

            <button onClick={() => onComplete(score)} className="btn btn-success group">
              Continue to Next Test
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
