import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch, tokenStore } from "../api";
import { ErrorState, Field } from "../components/common";
export function AuthPage({ mode }) {
  const register = mode === "register";
  const [form, setForm] = useState({ username: "", email: "", password: "", confirm: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();
  const update = (key) => (event) => setForm({ ...form, [key]: event.target.value });
  async function submit(event) {
    event.preventDefault(); setError("");
    if (!form.username || !form.password || (register && !form.email)) return setError("Please complete all required fields.");
    if (register && form.password !== form.confirm) return setError("Passwords do not match.");
    setBusy(true);
    try {
      if (register) {
        await apiFetch("/register/", { method: "POST", body: JSON.stringify({ username: form.username, email: form.email, password: form.password }) });
        const tokens = await apiFetch("/token/", { method: "POST", body: JSON.stringify({ username: form.username, password: form.password }) });
        tokenStore.set(tokens); navigate("/dashboard");
      } else {
        const tokens = await apiFetch("/token/", { method: "POST", body: JSON.stringify({ username: form.username, password: form.password }) });
        tokenStore.set(tokens); navigate("/dashboard");
      }
    } catch (err) { setError(err.message); } finally { setBusy(false); }
  }
  return <main className="auth-shell"><section className="auth-brand"><div className="brand-mark">✦</div><p className="eyebrow">CAREERPATH AI</p><h1>Build the career<br /><em>you’re ready for.</em></h1><p>Turn your skills into a clear, confident next step.</p></section>
    <section className="auth-card"><p className="eyebrow">WELCOME {register ? "ABOARD" : "BACK"}</p><h2>{register ? "Create your account" : "Sign in to your workspace"}</h2><p className="muted">{register ? "Start closing your skill gaps today." : "Your personalized career plan is waiting."}</p>
      <form onSubmit={submit}>{<Field label="Username" value={form.username} onChange={update("username")} autoComplete="username" required />}{register && <Field label="Email" type="email" value={form.email} onChange={update("email")} autoComplete="email" required />}<Field label="Password" type="password" value={form.password} onChange={update("password")} autoComplete={register ? "new-password" : "current-password"} required />{register && <Field label="Confirm password" type="password" value={form.confirm} onChange={update("confirm")} autoComplete="new-password" required />}{error && <ErrorState message={error} />}<button className="button primary full" disabled={busy}>{busy ? "Please wait..." : register ? "Create account" : "Sign in"} <span>→</span></button></form>
      <p className="auth-switch">{register ? "Already have an account?" : "New to CareerPath AI?"} <Link to={register ? "/login" : "/register"}>{register ? "Sign in" : "Create an account"}</Link></p>
    </section></main>;
}

