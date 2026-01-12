"use client"

import { useState, useRef } from "react"
import { ArrowRight, Zap, AlertCircle } from "../components/Icons"

export default function ReactionTest({ onComplete }) {
  const [stage, setStage] = useState("ready")
  const [startTime, setStartTime] = useState(0)
  const [reactionTime, setReactionTime] = useState(0)
  const [tooEarly, setTooEarly] = useState(false)
  const timeoutRef = useRef(null)

  const startTest = () => {
    setStage("waiting")
    setTooEarly(false)
    const delay = 2000 + Math.random() * 3000
    timeoutRef.current = setTimeout(() => {
      setStartTime(Date.now())
      setStage("click")
    }, delay)
  }

  const handleClick = () => {
    if (stage === "waiting") {
      if (timeoutRef.current) clearTimeout(timeoutRef.current)
      setTooEarly(true)
      setStage("ready")
    } else if (stage === "click") {
      const time = Date.now() - startTime
      setReactionTime(time)
      setStage("result")
    }
  }

  const getReactionRating = () => {
    if (reactionTime < 200) return { text: "Incredible!", emoji: "🚀", color: "text-emerald-500" }
    if (reactionTime < 300) return { text: "Excellent!", emoji: "⚡", color: "text-green-500" }
    if (reactionTime < 400) return { text: "Good!", emoji: "👍", color: "text-blue-500" }
    if (reactionTime < 500) return { text: "Average", emoji: "👌", color: "text-amber-500" }
    return { text: "Keep Practicing", emoji: "💪", color: "text-orange-500" }
  }

  return (
    <div className="text-center">
      <div className="mb-2 flex items-center justify-center gap-2">
        <Zap className="h-6 w-6 text-primary animate-pulse-slow" />
        <h2 className="text-2xl font-bold text-foreground md:text-3xl">Reaction Time Test</h2>
      </div>
      <p className="mb-8 text-muted-foreground">Click as fast as you can when the screen turns green</p>

      <div
        onClick={handleClick}
        className={`relative min-h-[24rem] cursor-pointer overflow-hidden rounded-2xl transition-all duration-300 ${
          stage === "ready"
            ? "bg-gradient-to-br from-blue-100 to-indigo-100 hover:from-blue-200 hover:to-indigo-200"
            : stage === "waiting"
              ? "bg-gradient-to-br from-red-100 to-rose-100"
              : stage === "click"
                ? "bg-gradient-to-br from-green-400 to-emerald-500 animate-pulse-slow"
                : "bg-gradient-to-br from-slate-100 to-gray-100"
        } flex items-center justify-center`}
      >
        {stage === "ready" && (
          <div className="animate-fade-in space-y-4 p-8">
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-white/50">
              <Zap className="h-10 w-10 text-primary" />
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation()
                startTest()
              }}
              className="btn btn-primary"
            >
              Start Test
            </button>
          </div>
        )}

        {stage === "waiting" && (
          <div className="animate-scale-in space-y-4">
            <div className="relative">
              <div className="absolute inset-0 animate-ping rounded-full bg-red-400 opacity-30" />
              <AlertCircle className="relative h-16 w-16 text-red-500" />
            </div>
            <p className="text-3xl font-bold text-red-600">WAIT...</p>
            <p className="text-red-400">{"Don't click yet!"}</p>
          </div>
        )}

        {stage === "click" && (
          <div className="animate-bounce-in space-y-4">
            <div className="relative">
              <div className="absolute inset-0 animate-ping rounded-full bg-white opacity-50" />
              <Zap className="relative h-20 w-20 text-white" />
            </div>
            <p className="text-5xl font-bold text-white">CLICK!</p>
          </div>
        )}

        {stage === "result" && (
          <div className="animate-fade-in space-y-6 p-8">
            <div className="text-6xl">{getReactionRating().emoji}</div>
            <div>
              <p className="text-6xl font-bold text-primary">{reactionTime}</p>
              <p className="text-xl text-muted-foreground">milliseconds</p>
            </div>
            <p className={`text-2xl font-semibold ${getReactionRating().color}`}>{getReactionRating().text}</p>
            <button
              onClick={(e) => {
                e.stopPropagation()
                onComplete(reactionTime)
              }}
              className="btn btn-success group"
            >
              Continue
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        )}
      </div>

      {tooEarly && (
        <div className="animate-shake mt-4 rounded-xl border-l-4 border-destructive bg-destructive/10 p-4">
          <p className="font-semibold text-destructive">Too early! Wait for the green screen.</p>
        </div>
      )}
    </div>
  )
}
