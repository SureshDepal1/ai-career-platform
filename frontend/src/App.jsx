import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { tokenStore } from "./api";
import { Landing } from "./pages/Landing";
import { AuthPage } from "./pages/AuthPage";
import { Protected, Layout } from "./components/Layout";
import { Dashboard, Profile } from "./pages/Dashboard";
import { Careers, CareerDetail, SkillGap, Roadmap } from "./pages/Careers";
import { JobAnalysis, AnalysisDetail, SavedAnalyses } from "./pages/Analysis";
import { AssessmentPage, AssessmentHistory, AssessmentResultPage } from "./pages/Assessments";
import { InterviewPage, InterviewHistory, InterviewResultPage } from "./pages/Interviews";

export function App() {
  return <Routes><Route path="/" element={<Landing />} /><Route path="/login" element={<AuthPage mode="login" />} /><Route path="/register" element={<AuthPage mode="register" />} /><Route element={<Protected />}><Route element={<Layout />}><Route path="/dashboard" element={<Dashboard />} /><Route path="/profile" element={<Profile />} /><Route path="/careers" element={<Careers />} /><Route path="/careers/:careerId" element={<CareerDetail />} /><Route path="/skill-gap" element={<SkillGap />} /><Route path="/roadmap" element={<Roadmap />} /><Route path="/job-analysis" element={<JobAnalysis />} /><Route path="/job-analysis/:jobId" element={<AnalysisDetail />} /><Route path="/saved-analyses" element={<SavedAnalyses />} /><Route path="/assessments" element={<AssessmentPage />} /><Route path="/assessments/history" element={<AssessmentHistory />} /><Route path="/assessments/:attemptId" element={<AssessmentResultPage />} /><Route path="/interviews" element={<InterviewPage />} /><Route path="/interviews/history" element={<InterviewHistory />} /><Route path="/interviews/:sessionId" element={<InterviewResultPage />} /></Route></Route><Route path="*" element={<Navigate to={tokenStore.access ? "/dashboard" : "/"} replace />} /></Routes>;
}
