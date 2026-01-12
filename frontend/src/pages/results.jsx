"use client"

import { useEffect, useState } from "react"
import { RefreshCw, AlertTriangle, CheckCircle, AlertCircle } from "lucide-react"

export default function Results({ result, onRestart }) {
  const [animatedScore, setAnimatedScore] = useState(0)

  useEffect(() => {
    const duration = 2000
    const steps = 60
    const increment = result.risk_score / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= result.risk_score) {
        setAnimatedScore(result.risk_score)
        clearInterval(timer)
      } else {
        setAnimatedScore(Math.round(current))
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [result.risk_score])

  const getRiskInfo = () => {
    switch (result.risk_category) {
      case "Low Risk":
        return {
          color: "from-emerald-500 to-teal-500",
          bgColor: "bg-emerald-500",
          textColor: "text-emerald-600",
          Icon: CheckCircle,
          message: "Your cognitive assessment shows healthy indicators.",
        }
      case "Moderate Risk":
        return {
          color: "from-amber-500 to-orange-500",
          bgColor: "bg-amber-500",
          textColor: "text-amber-600",
          Icon: AlertCircle,
          message: "Some indicators suggest further evaluation may be helpful.",
        }
      default:
        return {
          color: "from-red-500 to-rose-500",
          bgColor: "bg-red-500",
          textColor: "text-red-600",
          Icon: AlertTriangle,
          message: "We recommend consulting with a healthcare professional.",
        }
    }
  }

  const riskInfo = getRiskInfo()
  const RiskIcon = riskInfo.Icon

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="animate-scale-in w-full max-w-2xl">
        <div className="overflow-hidden rounded-3xl bg-card shadow-2xl">
          {/* Header */}
          <div className="animate-fade-in bg-gradient-to-r from-indigo-600 to-purple-600 p-8 text-center text-white">
            <h1 className="mb-2 text-3xl font-bold">Assessment Results</h1>
            <p className="text-indigo-100">Your cognitive screening summary</p>
          </div>

          <div className="p-8">
            {/* Score Circle */}
            <div className="animate-bounce-in mb-8 flex justify-center">
              <div className="relative">
                <svg className="h-48 w-48 -rotate-90 transform">
                  <circle cx="96" cy="96" r="88" stroke="#e5e5e5" strokeWidth="12" fill="none" />
                  <circle
                    cx="96"
                    cy="96"
                    r="88"
                    stroke="url(#gradient)"
                    strokeWidth="12"
                    fill="none"
                    strokeLinecap="round"
                    strokeDasharray={553}
                    strokeDashoffset={553 - (553 * animatedScore) / 100}
                    className="transition-all duration-100"
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#4f46e5" />
                      <stop offset="100%" stopColor="#7c3aed" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-5xl font-bold text-foreground">{animatedScore}%</span>
                  <span className="text-sm text-muted-foreground">Risk Score</span>
                </div>
              </div>
            </div>

            {/* Risk Badge */}
            <div className="animate-scale-in stagger-2 opacity-0 mb-8 flex justify-center">
              <div
                className={`flex items-center gap-3 rounded-full bg-gradient-to-r ${riskInfo.color} px-6 py-3 text-white shadow-lg`}
              >
                <RiskIcon className="h-6 w-6" />
                <span className="text-xl font-bold">{result.risk_category}</span>
              </div>
            </div>

            {/* Message */}
            <p className="animate-fade-in stagger-3 opacity-0 mb-8 text-center text-lg text-muted-foreground">
              {riskInfo.message}
            </p>

            {/* Breakdown */}
            <div className="animate-slide-in-right stagger-4 opacity-0 mb-8 grid gap-4 md:grid-cols-2">
              <div className="rounded-xl bg-muted/50 p-6 text-center transition-all duration-300 hover:scale-105 hover:bg-muted">
                <p className="mb-2 text-sm text-muted-foreground">Cognitive Risk</p>
                <p className="text-3xl font-bold text-primary">{result.cognitive_risk}%</p>
              </div>
              <div className="rounded-xl bg-muted/50 p-6 text-center transition-all duration-300 hover:scale-105 hover:bg-muted">
                <p className="mb-2 text-sm text-muted-foreground">Speech Analysis</p>
                <p className="text-3xl font-bold text-primary">
                  {result.speech_analyzed ? "Included" : "Not Provided"}
                </p>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="animate-fade-in stagger-5 opacity-0 mb-8 rounded-xl border-l-4 border-warning bg-warning/10 p-4">
              <p className="text-sm leading-relaxed text-amber-800">
                <strong>Disclaimer:</strong> This tool is for screening purposes only and does not provide a medical
                diagnosis. Please consult a healthcare professional for clinical evaluation.
              </p>
            </div>

            {/* Restart Button */}
            <div className="animate-scale-in stagger-6 opacity-0 flex justify-center">
              <button onClick={onRestart} className="btn btn-primary btn-lg group">
                <RefreshCw className="h-5 w-5 transition-transform duration-500 group-hover:rotate-180" />
                Restart Assessment
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
