import { Routes, Route, NavLink, Navigate } from 'react-router-dom';
import {
  LayoutDashboard, CalendarCheck, Swords, Target, Brain, Code2,
  BookOpen, MessageSquare, Search, BarChart3, FileText, Settings,
  Bug, RotateCcw, GraduationCap, BriefcaseBusiness, Timer
} from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Today from './pages/Today';
import Drills from './pages/Drills';
import MockInterview from './pages/MockInterview';
import LLDPractice from './pages/LLDPractice';
import Behavioral from './pages/Behavioral';
import JavaQA from './pages/JavaQA';
import LeetCode from './pages/LeetCode';
import Applications from './pages/Applications';
import SpacedRepetition from './pages/SpacedRepetition';
import Curriculum from './pages/Curriculum';
import Coach from './pages/Coach';
import Intelligence from './pages/Intelligence';
import BugJournal from './pages/BugJournal';
import Retros from './pages/Retros';
import SettingsPage from './pages/Settings';

const NAV = [
  { section: 'Overview', items: [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/today', icon: CalendarCheck, label: 'Today' },
  ]},
  { section: 'Practice', items: [
    { to: '/drills', icon: Swords, label: 'Drills' },
    { to: '/mock', icon: Timer, label: 'Mock Interview' },
    { to: '/lld', icon: Code2, label: 'LLD Practice' },
    { to: '/behavioral', icon: Brain, label: 'Behavioral' },
    { to: '/java', icon: GraduationCap, label: 'Java Q&A' },
  ]},
  { section: 'Track', items: [
    { to: '/leetcode', icon: Target, label: 'LeetCode' },
    { to: '/applications', icon: BriefcaseBusiness, label: 'Applications' },
    { to: '/sr', icon: RotateCcw, label: 'Spaced Repetition' },
    { to: '/bugs', icon: Bug, label: 'Bug Journal' },
    { to: '/retros', icon: FileText, label: 'Retros' },
  ]},
  { section: 'Learn', items: [
    { to: '/curriculum', icon: BookOpen, label: 'Curriculum' },
    { to: '/coach', icon: MessageSquare, label: 'AI Coach' },
    { to: '/intel', icon: Search, label: 'Intelligence' },
  ]},
  { section: 'System', items: [
    { to: '/settings', icon: Settings, label: 'Settings' },
  ]},
];

export default function App() {
  return (
    <div className="app-layout">
      <nav className="sidebar">
        <div className="sidebar-brand">
          <h1>PREPFORGE</h1>
          <div className="sub">INTELLIGENCE ENGINE</div>
        </div>
        {NAV.map((section) => (
          <div key={section.section} className="sidebar-section">
            <div className="sidebar-section-title">{section.section}</div>
            {section.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
              >
                <item.icon />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/today" element={<Today />} />
          <Route path="/drills" element={<Drills />} />
          <Route path="/mock" element={<MockInterview />} />
          <Route path="/lld" element={<LLDPractice />} />
          <Route path="/behavioral" element={<Behavioral />} />
          <Route path="/java" element={<JavaQA />} />
          <Route path="/leetcode" element={<LeetCode />} />
          <Route path="/applications" element={<Applications />} />
          <Route path="/sr" element={<SpacedRepetition />} />
          <Route path="/bugs" element={<BugJournal />} />
          <Route path="/retros" element={<Retros />} />
          <Route path="/curriculum" element={<Curriculum />} />
          <Route path="/coach" element={<Coach />} />
          <Route path="/intel" element={<Intelligence />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
