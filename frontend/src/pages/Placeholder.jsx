import React from "react";
import { Link } from "react-router-dom";
export function Placeholder({ title, text, link, action }) { return <section className="panel placeholder"><span className="placeholder-icon">✦</span><p className="eyebrow">{title.toUpperCase()}</p><h2>{text}</h2><p className="muted">This workspace is connected to your existing backend data. Start with your profile and career goal to personalize it.</p>{link && <Link className="button primary" to={link}>{action} <span>→</span></Link>}</section>; }

