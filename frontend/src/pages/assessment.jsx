"use client"

import { useState } from "react"
import JumbledWordTest from "../tests/JumbledWordTest"
import MemoryTest from "../tests/MemoryTest"
import ReactionTest from "../tests/ReactionTest"
import AudioUpload from "../tests/AudioUpload"

const testNames = ["Word Test", "Memory Test", "Reaction Test", "Audio Upload"]

export default function Assessment({ assessmentData, updateAssessmentData, onComplete }) {
  const [currentTest, setCurrentTest] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [isTransitioning, setIsTransitioning] = useState(false)

  const tests = ["jumbled", "memory", "reaction", "audio"]

  const handleTestComplete = (key, value) => {
    updateAssessmentData(key, value)
    if (currentTest < tests.length - 1) {
      setIsTransitioning(true)
      setTimeout(() => {
        setCurrentTest(currentTest + 1)
        setIsTransitioning(false)
      }, 300)
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError("")

    try {
      const formData = new FormData()
      
      // ✅ FIXED: Match backend field names exactly
      formData.append("word_score", String(assessmentData.wordScore))
      formData.append("memory_score", String(assessmentData.memoryScore))
      formData.append("reaction_time", String(assessmentData.reactionTime))

      // Add audio file if provided
      if (assessmentData.audioFile) {
        formData.append("audio_file", assessmentData.audioFile)
      }

      console.log("Submitting data:", {
        word_score: assessmentData.wordScore,
        memory_score: assessmentData.memoryScore,
        reaction_time: assessmentData.reactionTime,
        has_audio: !!assessmentData.audioFile
      })

      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
      })

      console.log("Response status:", response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error("Server error:", errorText)
        throw new Error(`API request failed: ${response.status}`)
      }

      const data = await response.json()
      console.log("Success! Result:", data)
      onComplete(data)
      
    } catch (err) {
      console.error("Submit error:", err)
      setError(`Failed to submit assessment: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const renderTest = () => {
    const className = `transition-all duration-300 ${isTransitioning ? "opacity-0 translate-x-10" : "opacity-100 translate-x-0"}`

    switch (tests[currentTest]) {
      case "jumbled":
        return (
          <div className={className}>
            <JumbledWordTest onComplete={(score) => handleTestComplete("wordScore", score)} />
          </div>
        )
      case "memory":
        return (
          <div className={className}>
            <MemoryTest onComplete={(score) => handleTestComplete("memoryScore", score)} />
          </div>
        )
      case "reaction":
        return (
          <div className={className}>
            <ReactionTest onComplete={(time) => handleTestComplete("reactionTime", time)} />
          </div>
        )
      case "audio":
        return (
          <div className={className}>
            <AudioUpload
              onComplete={(file) => updateAssessmentData("audioFile", file)}
              onSubmit={handleSubmit}
              loading={loading}
              error={error}
            />
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="mx-auto max-w-3xl">
        {/* Progress Card */}
        <div className="animate-slide-in-left mb-6 rounded-2xl bg-card p-6 shadow-lg">
          <div className="mb-4 flex items-center justify-between">
            <span className="text-sm font-semibold text-muted-foreground">Assessment Progress</span>
            <span className="text-sm font-bold text-primary">
              Step {currentTest + 1} of {tests.length}
            </span>
          </div>

          {/* Step indicators */}
          <div className="mb-4 flex gap-2">
            {tests.map((_, index) => (
              <div
                key={index}
                className={`h-2 flex-1 rounded-full transition-all duration-500 ${
                  index < currentTest
                    ? "bg-success"
                    : index === currentTest
                      ? "animate-pulse-slow bg-primary"
                      : "bg-muted"
                }`}
              />
            ))}
          </div>

          {/* Test labels */}
          <div className="flex justify-between text-xs">
            {testNames.map((name, index) => (
              <span
                key={index}
                className={`transition-colors duration-300 ${
                  index <= currentTest ? "font-medium text-primary" : "text-muted-foreground"
                }`}
              >
                {name}
              </span>
            ))}
          </div>
        </div>

        {/* Test Card */}
        <div className="animate-fade-in rounded-3xl bg-card p-6 shadow-2xl md:p-8">{renderTest()}</div>
      </div>
    </div>
  )
}