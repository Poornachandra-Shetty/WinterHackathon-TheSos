"use client"

import { useState, useRef } from "react"
import { Upload, FileAudio, Check, AlertCircle, Loader, Send, Mic } from "../components/Icons"

export default function AudioUpload({ onComplete, onSubmit, loading, error }) {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef(null)

  const handleChange = (e) => {
    const selected = e.target.files?.[0]
    if (selected && selected.name.endsWith(".wav")) {
      setFile(selected)
      onComplete(selected)
    } else {
      alert("Please upload a WAV file only")
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped && dropped.name.endsWith(".wav")) {
      setFile(dropped)
      onComplete(dropped)
    } else {
      alert("Please upload a WAV file only")
    }
  }

  return (
    <div className="text-center">
      <div className="mb-2 flex items-center justify-center gap-2">
        <Mic className="h-6 w-6 text-primary animate-pulse-slow" />
        <h2 className="text-2xl font-bold text-foreground md:text-3xl">Speech Sample</h2>
      </div>
      <p className="mb-8 text-muted-foreground">Upload a WAV audio file (optional)</p>

      {/* Upload Area */}
      <div
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`animate-fade-in mb-8 cursor-pointer rounded-2xl border-2 border-dashed p-12 transition-all duration-300 ${
          isDragging
            ? "scale-105 border-primary bg-primary/10"
            : file
              ? "border-success bg-success/5"
              : "border-muted-foreground/30 bg-muted/30 hover:border-primary hover:bg-primary/5"
        }`}
      >
        <input ref={inputRef} type="file" accept=".wav" onChange={handleChange} className="hidden" />

        {file ? (
          <div className="animate-scale-in space-y-4">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-success/20">
              <Check className="h-8 w-8 text-success" />
            </div>
            <div>
              <div className="flex items-center justify-center gap-2">
                <FileAudio className="h-5 w-5 text-success" />
                <p className="font-semibold text-foreground">{file.name}</p>
              </div>
              <p className="mt-1 text-sm text-muted-foreground">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
            <p className="text-sm text-success">Click to change file</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="animate-float mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <Upload className="h-8 w-8 text-primary" />
            </div>
            <div>
              <p className="font-semibold text-foreground">Drop your WAV file here</p>
              <p className="mt-1 text-sm text-muted-foreground">or click to browse</p>
            </div>
          </div>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="animate-shake mb-6 flex items-center justify-center gap-2 rounded-xl border-l-4 border-destructive bg-destructive/10 p-4">
          <AlertCircle className="h-5 w-5 text-destructive" />
          <p className="font-semibold text-destructive">{error}</p>
        </div>
      )}

      {/* Submit Button */}
      <button onClick={onSubmit} disabled={loading} className="btn btn-success btn-lg group">
        {loading ? (
          <>
            <Loader className="h-5 w-5 animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Send className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            Submit Assessment
          </>
        )}
      </button>

      {/* Info */}
      <p className="animate-fade-in mt-6 text-sm text-muted-foreground">
        Audio analysis helps improve screening accuracy but is not required
      </p>
    </div>
  )
}
