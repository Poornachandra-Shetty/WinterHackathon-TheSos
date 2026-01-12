"use client"

import { Brain, ArrowRight, Shield, Clock, Mic } from "lucide-react"

export default function Home({ onStart }) {
  const features = [
    { icon: Brain, label: "Memory Tests", delay: "stagger-1" },
    { icon: Clock, label: "Reaction Time", delay: "stagger-2" },
    { icon: Mic, label: "Speech Analysis", delay: "stagger-3" },
  ]

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="animate-fade-in w-full max-w-2xl">
        <div className="group relative overflow-hidden rounded-3xl bg-card p-8 shadow-2xl transition-all duration-500 hover:shadow-indigo-500/20 md:p-12">
          {/* Background decoration */}
          <div className="absolute -right-20 -top-20 h-40 w-40 rounded-full bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 blur-3xl transition-all duration-700 group-hover:scale-150" />
          <div className="absolute -bottom-20 -left-20 h-40 w-40 rounded-full bg-gradient-to-br from-purple-500/20 to-pink-500/20 blur-3xl transition-all duration-700 group-hover:scale-150" />

          <div className="relative">
            {/* Icon */}
            <div className="mb-8 flex justify-center">
              <div className="animate-float relative">
                <div className="absolute inset-0 rounded-full bg-indigo-500/20 blur-xl" />
                <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/30">
                  <Brain className="h-12 w-12 text-white" />
                </div>
              </div>
            </div>

            {/* Title */}
            <h1 className="mb-4 text-center text-4xl font-bold tracking-tight md:text-5xl">
              <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                AI Dementia Screening
              </span>
            </h1>

            <p className="mx-auto mb-8 max-w-lg text-center text-lg leading-relaxed text-muted-foreground">
              Complete a series of cognitive assessments to evaluate your cognitive health with our AI-powered screening
              tool.
            </p>

            {/* Features */}
            <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className={`animate-scale-in opacity-0 ${feature.delay} flex items-center gap-3 rounded-xl bg-secondary/50 p-4 transition-all duration-300 hover:scale-105 hover:bg-secondary`}
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                    <feature.icon className="h-5 w-5 text-primary" />
                  </div>
                  <span className="font-medium text-foreground">{feature.label}</span>
                </div>
              ))}
            </div>

            {/* Info box */}
            <div className="animate-scale-in stagger-4 opacity-0 mb-8 rounded-xl border-l-4 border-primary bg-primary/5 p-4">
              <div className="flex items-start gap-3">
                <Shield className="mt-0.5 h-5 w-5 flex-shrink-0 text-primary" />
                <p className="text-sm leading-relaxed text-secondary-foreground">
                  <strong>Important:</strong> This is a screening tool only and not a medical diagnosis. Results should
                  be discussed with a healthcare professional.
                </p>
              </div>
            </div>

            {/* CTA Button */}
            <div className="animate-scale-in stagger-5 opacity-0 flex justify-center">
              <button onClick={onStart} className="btn btn-primary btn-lg group">
                <span className="flex items-center gap-2">
                  Start Assessment
                  <ArrowRight className="h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
