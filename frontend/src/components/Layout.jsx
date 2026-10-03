import React, { useState } from "react";
import { Link, NavLink, Navigate, Outlet, useLocation, useNavigate } from "react-router-dom";
import { tokenStore } from "../api";
import { navItems } from "./navigation";
export function Protected() { return tokenStore.access ? <Outlet /> : <Navigate to="/login" replace />; }
export function Layout() {
  const navigate = useNavigate(); const location = useLocation(); const [open, setOpen] = useState(false);
  const title = navItems.find((item) => location.pathname.startsWith(item[1]))?.[0] || "Dashboard";
  function logout() { tokenStore.clear(); navigate("/login"); }
  return <div className="app-shell"><aside className={open ? "sidebar open" : "sidebar"}><div className="sidebar-top"><Link to="/dashboard" className="logo"><span className="logo-icon">✦</span><span>CareerPath <b>AI</b></span></Link><button className="close-menu" onClick={() => setOpen(false)}>×</button></div><p className="nav-label">WORKSPACE</p><nav>{navItems.map(([label, path, icon]) => <NavLink key={path} to={path} onClick={() => setOpen(false)} className={({ isActive }) => isActive ? "active" : ""}><span>{icon}</span>{label}</NavLink>)}</nav><button className="logout" onClick={logout}>↪ <span>Log out</span></button></aside><div className="content"><header><button className="menu-button" onClick={() => setOpen(true)}>☰</button><div><p className="eyebrow">WORKSPACE</p><h1>{title}</h1></div><div className="header-user"><span className="avatar">{(localStorage.getItem("career_username") || "U")[0].toUpperCase()}</span><span>{localStorage.getItem("career_username") || "Your account"}</span></div></header><div className="page"><Outlet /></div></div></div>;
}

