import { useState } from "react"
import Home from "./pages/home"
import Assessment from "./pages/assessment"
import Results from "./pages/results"
import "./styles.css"

export default function App() {
  const [currentPage, setCurrentPage] = useState("home")
  const [assessmentData, setAssessmentData] = useState({
    wordScore: 0,
    memoryScore: 0,
    reactionTime: 0,
    audioFile: null,
  })
  const [apiResult, setApiResult] = useState(null)

  const updateAssessmentData = (key, value) => {
    setAssessmentData((prev) => ({ ...prev, [key]: value }))
  }

  const handleRestart = () => {
    setCurrentPage("home")
    setAssessmentData({
      wordScore: 0,
      memoryScore: 0,
      reactionTime: 0,
      audioFile: null,
    })
    setApiResult(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-cyan-50/20">
      {currentPage === "home" && <Home onStart={() => setCurrentPage("assessment")} />}
      {currentPage === "assessment" && (
        <Assessment
          assessmentData={assessmentData}
          updateAssessmentData={updateAssessmentData}
          onComplete={(result) => {
            setApiResult(result)
            setCurrentPage("results")
          }}
        />
      )}
      {currentPage === "results" && apiResult && <Results result={apiResult} onRestart={handleRestart} />}
    </div>
  )
}