
"use client";

import { useState } from "react";
import {
  LayoutDashboard, Bot, Package, Tags, Users, Activity,
  Settings, Search, Bell, ArrowUpRight, ArrowDownRight,
  Sparkles, ShoppingCart, DollarSign, TrendingUp, Zap,
  ChevronDown, Plus, Clock3, CheckCircle2, Menu, X,
  MessageSquare, ChartNoAxesCombined
} from "lucide-react";

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from "recharts";

const salesData = [
  { day: "Mon", revenue: 420, orders: 8 },
  { day: "Tue", revenue: 680, orders: 12 },
  { day: "Wed", revenue: 510, orders: 10 },
  { day: "Thu", revenue: 890, orders: 17 },
  { day: "Fri", revenue: 720, orders: 14 },
  { day: "Sat", revenue: 1100, orders: 21 },
  { day: "Sun", revenue: 960, orders: 19 },
];

const agents = [
  { name: "Sales Intelligence", detail: "Analyzes revenue and trends", icon: ChartNoAxesCombined, status: "Ready", color: "purple" },
  { name: "Product Management", detail: "Manages product catalogue", icon: Package, status: "Ready", color: "blue" },
  { name: "Pricing & Discounts", detail: "Optimizes promotions", icon: Tags, status: "Coming soon", color: "orange" },
  { name: "Customer Behaviour", detail: "Investigates conversion", icon: Users, status: "Coming soon", color: "green" },
];

const navItems = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "AI Assistant", icon: Bot },
  { name: "Sales Intelligence", icon: ChartNoAxesCombined },
  { name: "Products", icon: Package },
  { name: "Pricing & Discounts", icon: Tags },
  { name: "Customer Intelligence", icon: Users },
  { name: "Activity Logs", icon: Activity },
];

export default function Home() {
  const [activeNav, setActiveNav] = useState("Overview");
  const [period, setPeriod] = useState("7 days");
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <main className="dashboard-shell">

      {mobileOpen && (
        <button className="mobile-overlay" onClick={() => setMobileOpen(false)} aria-label="Close navigation" />
      )}

      <aside className={`sidebar ${mobileOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon"><Sparkles size={21} /></div>
          <div>
            <h2>bharatlot<span>.ai</span></h2>
            <p>COMMERCE INTELLIGENCE</p>
          </div>
          <button className="mobile-close" onClick={() => setMobileOpen(false)}><X /></button>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="nav-list">
          {navItems.map((item) => (
            <button
              key={item.name}
              className={`nav-item ${activeNav === item.name ? "nav-active" : ""}`}
              onClick={() => {
                setActiveNav(item.name);
                setMobileOpen(false);
              }}
            >
              <item.icon size={18} />
              <span>{item.name}</span>
              {item.name === "AI Assistant" && <span className="nav-dot" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon"><Zap size={17} /></div>
            <h4>AI-powered commerce</h4>
            <p>Your intelligent business workspace.</p>
          </div>
          <button className="nav-item">
            <Settings size={18} /><span>Settings</span>
          </button>
          <div className="profile">
            <div className="avatar">B</div>
            <div className="profile-info">
              <strong>Bharatlot Admin</strong>
              <span>Workspace owner</span>
            </div>
            <ChevronDown size={16} />
          </div>
        </div>
      </aside>

      <section className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <button className="mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open navigation"><Menu /></button>
            <div className="breadcrumb">Workspace <span>/</span> <strong>{activeNav}</strong></div>
          </div>
          <div className="topbar-right">
            <div className="system-status"><span /> All systems operational</div>
            <button className="icon-button" aria-label="Search"><Search size={18} /></button>
            <button className="icon-button notification" aria-label="Notifications"><Bell size={18} /><i /></button>
            <div className="top-avatar">B</div>
          </div>
        </header>

        <div className="content">

          <div className="welcome-row">
            <div>
              <div className="eyebrow"><Sparkles size={14} /> INTELLIGENT COMMERCE PLATFORM</div>
              <h1>Good morning, <span>Bharatlot.</span></h1>
              <p>Here's what's happening with your business today.</p>
            </div>
            <button className="date-button"><Clock3 size={16} /> Last 7 days <ChevronDown size={15} /></button>
          </div>

          <div className="demo-notice">
            <span className="demo-indicator" />
            <span><strong>Preview environment</strong> — Displaying illustrative data. Connect Bharatlot's exports to load actual business metrics.</span>
          </div>

          <div className="section-heading">
            <div><h3>Business overview</h3><p>Your store performance at a glance</p></div>
            <span className="live-label"><span /> ANALYTICS PREVIEW</span>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-top"><span>Total revenue</span><div className="stat-icon purple"><DollarSign size={19} /></div></div>
              <h2>$5,280.00</h2>
              <div className="stat-bottom"><span className="positive"><ArrowUpRight size={15} /> 12.8%</span><span>vs previous period</span></div>
            </div>
            <div className="stat-card">
              <div className="stat-top"><span>Total orders</span><div className="stat-icon blue"><ShoppingCart size={19} /></div></div>
              <h2>104</h2>
              <div className="stat-bottom"><span className="positive"><ArrowUpRight size={15} /> 8.4%</span><span>vs previous period</span></div>
            </div>
            <div className="stat-card">
              <div className="stat-top"><span>Average order value</span><div className="stat-icon green"><TrendingUp size={19} /></div></div>
              <h2>$50.77</h2>
              <div className="stat-bottom"><span className="positive"><ArrowUpRight size={15} /> 4.2%</span><span>vs previous period</span></div>
            </div>
            <div className="stat-card">
              <div className="stat-top"><span>Products tracked</span><div className="stat-icon orange"><Package size={19} /></div></div>
              <h2>248</h2>
              <div className="stat-bottom"><span className="neutral">Catalogue</span><span>Illustrative count</span></div>
            </div>
          </div>

          <div className="middle-grid">
            <div className="panel revenue-panel">
              <div className="panel-header">
                <div><h3>Revenue overview</h3><p>Revenue performance over time</p></div>
                <select value={period} onChange={(e) => setPeriod(e.target.value)}>
                  <option>7 days</option><option>30 days</option><option>90 days</option>
                </select>
              </div>
              <div className="chart-summary"><h2>$5,280.00</h2><span className="positive"><ArrowUpRight size={15} /> 12.8%</span></div>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={salesData}>
                    <defs>
                      <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#9274FF" stopOpacity={0.28} />
                        <stop offset="95%" stopColor="#9274FF" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid stroke="#242638" strokeDasharray="4 4" vertical={false} />
                    <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fill: "#85869A", fontSize: 12 }} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fill: "#85869A", fontSize: 11 }} tickFormatter={(value) => `$${value}`} />
                    <Tooltip contentStyle={{ background: "#171927", border: "1px solid #34364b", borderRadius: 10, color: "#fff" }} formatter={(value) => [`$${value}`, "Revenue"]} />
                    <Area type="monotone" dataKey="revenue" stroke="#9274FF" strokeWidth={2.5} fill="url(#revenueGradient)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="panel activity-panel">
              <div className="panel-header"><div><h3>Agent activity</h3><p>AI workforce overview</p></div><button className="more-button">•••</button></div>
              <div className="activity-count"><strong>02</strong><span>Agents being prepared</span></div>
              <div className="activity-list">
                <div className="activity-item"><div className="activity-icon purple"><Bot size={18} /></div><div><strong>Sales Intelligence</strong><span>Analytics engine setup</span></div><span className="status-ready">READY</span></div>
                <div className="activity-item"><div className="activity-icon blue"><Package size={18} /></div><div><strong>Product Management</strong><span>Tool development</span></div><span className="status-ready">READY</span></div>
                <div className="activity-item"><div className="activity-icon orange"><Tags size={18} /></div><div><strong>Pricing Agent</strong><span>Planned capability</span></div><span className="status-planned">PLANNED</span></div>
                <div className="activity-item"><div className="activity-icon green"><Users size={18} /></div><div><strong>Customer Agent</strong><span>Planned capability</span></div><span className="status-planned">PLANNED</span></div>
              </div>
              <button className="text-link" onClick={() => setActiveNav("AI Assistant")}>Explore AI workspace <ArrowUpRight size={15} /></button>
            </div>
          </div>

          <div className="bottom-grid">
            <div className="panel agents-panel">
              <div className="panel-header">
                <div><h3>Your AI workforce</h3><p>Specialized agents for commerce operations</p></div>
                <button className="outline-button" onClick={() => setActiveNav("AI Assistant")}><Plus size={15} /> Explore agents</button>
              </div>
              <div className="agent-grid">
                {agents.map((agent) => (
                  <div className="agent-card" key={agent.name}>
                    <div className={`agent-card-icon ${agent.color}`}><agent.icon size={20} /></div>
                    <div className="agent-card-title">{agent.name}</div>
                    <p>{agent.detail}</p>
                    <div className="agent-card-bottom">
                      <span className={agent.status === "Ready" ? "agent-ready" : "agent-planned"}><span /> {agent.status}</span>
                      <ArrowUpRight size={16} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="assistant-banner">
            <div className="assistant-symbol"><Sparkles size={23} /></div>
            <div className="assistant-copy"><h3>Your business deserves an intelligent assistant.</h3><p>Ask questions, investigate performance and manage commerce operations using AI agents.</p></div>
            <button onClick={() => setActiveNav("AI Assistant")}>Open AI workspace <ArrowUpRight size={16} /></button>
          </div>

          <footer>BHARATLOT AI <span>•</span> COMMERCE INTELLIGENCE PLATFORM <span>•</span> DEVELOPMENT PREVIEW</footer>
        </div>
      </section>
    </main>
  );
}
