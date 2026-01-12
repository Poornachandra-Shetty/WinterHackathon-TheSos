"use client"

import { useState } from "react"
import { ArrowRight, Play, Eye, Hand } from "../components/Icons"

export default function MemoryTest({ onComplete }) {
  const [sequence, setSequence] = useState([])
  const [userSequence, setUserSequence] = useState([])
  const [isPlaying, setIsPlaying] = useState(false)
  const [activeBox, setActiveBox] = useState(null)
  const [level, setLevel] = useState(1)
  const [gameStarted, setGameStarted] = useState(false)
  const [gameOver, setGameOver] = useState(false)
  const [maxLevel, setMaxLevel] = useState(0)
  const [clickedBox, setClickedBox] = useState(null)

  const gridSize = 9

  const startGame = () => {
    setGameStarted(true)
    setLevel(1)
    setMaxLevel(0)
    setGameOver(false)
    startNewRound(1)
  }

  const startNewRound = (currentLevel) => {
    const newSequence = Array.from({ length: currentLevel }, () => Math.floor(Math.random() * gridSize))
    setSequence(newSequence)
    setUserSequence([])
    playSequence(newSequence)
  }

  const playSequence = async (seq) => {
    setIsPlaying(true)
    for (let i = 0; i < seq.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 500))
      setActiveBox(seq[i])
      await new Promise((resolve) => setTimeout(resolve, 600))
      setActiveBox(null)
    }
    setIsPlaying(false)
  }

  const handleBoxClick = (index) => {
    if (isPlaying || gameOver) return

    const newUserSequence = [...userSequence, index]
    setUserSequence(newUserSequence)

    setClickedBox(index)
    setActiveBox(index)
    setTimeout(() => {
      setActiveBox(null)
      setClickedBox(null)
    }, 200)

    if (newUserSequence[newUserSequence.length - 1] !== sequence[newUserSequence.length - 1]) {
      setGameOver(true)
      setMaxLevel(level - 1)
      return
    }

    if (newUserSequence.length === sequence.length) {
      const nextLevel = level + 1
      if (nextLevel > 9) {
        setGameOver(true)
        setMaxLevel(9)
      } else {
        setLevel(nextLevel)
        setTimeout(() => startNewRound(nextLevel), 1000)
      }
    }
  }

  const instructions = [
    { icon: Eye, text: "Watch the boxes light up in sequence" },
    { icon: Hand, text: "Repeat the sequence by clicking boxes" },
    { icon: ArrowRight, text: "Each level adds one more box" },
  ]

  return (
    <div className="text-center">
      <h2 className="mb-2 text-2xl font-bold text-foreground md:text-3xl">Memory Pattern Test</h2>
      <p className="mb-8 text-muted-foreground">Watch the sequence and repeat it</p>

      {!gameStarted ? (
        <div className="space-y-6">
          <div className="animate-fade-in rounded-2xl bg-gradient-to-br from-indigo-50 to-purple-50 p-6">
            <p className="mb-4 font-semibold text-foreground">Instructions:</p>
            <ul className="mx-auto max-w-sm space-y-3 text-left text-muted-foreground">
              {instructions.map((item, index) => (
                <li
                  key={index}
                  className={`animate-slide-in-left stagger-${index + 1} opacity-0 flex items-center gap-3`}
                >
                  <item.icon className="h-5 w-5 text-primary" />
                  <span>{item.text}</span>
                </li>
              ))}
            </ul>
          </div>

          <button onClick={startGame} className="btn btn-primary animate-scale-in stagger-4 opacity-0 group">
            <Play className="h-5 w-5" />
            Start Test
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Level Display */}
          <div className="animate-bounce-in">
            <span className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-6 py-2">
              <span className="text-muted-foreground">Level</span>
              <span className="text-3xl font-bold text-primary">{level}</span>
            </span>
          </div>

          {/* Status */}
          <p
            className={`text-lg font-medium transition-all duration-300 ${isPlaying ? "text-warning animate-pulse-slow" : "text-success"}`}
          >
            {isPlaying ? "Watch carefully..." : `Your turn! (${userSequence.length}/${sequence.length})`}
          </p>

          {/* Grid */}
          <div className="mx-auto grid max-w-xs grid-cols-3 gap-3">
            {Array.from({ length: gridSize }).map((_, index) => (
              <button
                key={index}
                onClick={() => handleBoxClick(index)}
                disabled={isPlaying || gameOver}
                className={`aspect-square rounded-xl text-2xl font-bold transition-all duration-200 ${
                  activeBox === index
                    ? "scale-110 bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-lg shadow-amber-500/50 animate-pulse-slow"
                    : clickedBox === index
                      ? "scale-95 bg-indigo-400"
                      : "bg-gradient-to-br from-indigo-200 to-purple-200 hover:from-indigo-300 hover:to-purple-300 hover:scale-105"
                } disabled:cursor-not-allowed`}
              >
                {index + 1}
              </button>
            ))}
          </div>

          {/* Game Over */}
          {gameOver && (
            <div className="animate-scale-in space-y-4 rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 p-6">
              <div className="text-5xl">🎯</div>
              <p className="text-xl font-bold text-foreground">Test Complete!</p>
              <p className="text-muted-foreground">
                Maximum Level: <span className="font-bold text-primary">{maxLevel}</span>
              </p>
              <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-6 py-3">
                <span className="text-muted-foreground">Memory Score:</span>
                <span className="text-2xl font-bold text-primary">{Math.min(maxLevel, 9)}/9</span>
              </div>

              <div>
                <button onClick={() => onComplete(Math.min(maxLevel, 9))} className="btn btn-success group">
                  Continue to Next Test
                  <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
