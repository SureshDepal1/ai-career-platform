import React from "react";
export function Field({ label, ...props }) { return <label className="field"><span>{label}</span><input {...props} /></label>; }
export function TextArea({ label, ...props }) { return <label className="field"><span>{label}</span><textarea {...props} /></label>; }
export function Loading({ label = "Loading your workspace..." }) { return <div className="loading"><span className="spinner" />{label}</div>; }
export function ErrorState({ message }) { const friendly = message?.includes("401") || message?.toLowerCase().includes("unauthorized") ? "Your session has expired. Please sign in again." : "Something went wrong while loading this workspace. Please try again."; return <div className="error-box"><strong>{friendly}</strong></div>; }
export function Empty({ children }) { return <div className="empty">{children}</div>; }

