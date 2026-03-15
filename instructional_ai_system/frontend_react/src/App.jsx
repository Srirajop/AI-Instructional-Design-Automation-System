import React, { useState, useEffect } from 'react';
import { api } from './api';
import Sidebar from './components/Sidebar';
import ProjectList from './components/ProjectList';
import FolderManager from './components/FolderManager';
import ProjectUpload from './components/ProjectUpload';
import Dashboard from './components/Dashboard';
import Auth from './components/Auth';
import IntakeForm from './components/IntakeForm';
import ProjectView from './components/ProjectView';
import LandingPage from './components/LandingPage';
import ResetPassword from './components/ResetPassword';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

export default function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard'); // dashboard, projects, folders, intake, project, upload
  const [activeProjectId, setActiveProjectId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // login, register

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await api.request('/auth/me');
          setUser(userData);
        } catch {
          localStorage.removeItem('token');
          setUser(null);
        }
      }
      setLoading(false);
    };

    verifyToken();

    const handleUnauthorized = () => {
      setUser(null);
      setCurrentView('dashboard');
    };

    window.addEventListener('unauthorized', handleUnauthorized);
    return () => window.removeEventListener('unauthorized', handleUnauthorized);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentView('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentView('dashboard');
  };

  const handleOpenProject = (id) => {
    setActiveProjectId(id);
    setCurrentView('project');
  };

  const handleUploadProject = () => {
    setCurrentView('upload');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <span className="spinner" style={{ borderColor: 'var(--primary)', borderTopColor: 'transparent', width: '40px', height: '40px' }}></span>
      </div>
    );
  }


  return (
    <BrowserRouter>
      <Routes>
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="*" element={
          !user ? (
            showAuth ? (
              <Auth
                onLogin={handleLogin}
                onBack={() => setShowAuth(false)}
                initialIsLogin={authMode === 'login'}
              />
            ) : (
              <LandingPage 
                onGetStarted={() => { setAuthMode('register'); setShowAuth(true); }}
                onSignIn={() => { setAuthMode('login'); setShowAuth(true); }}
              />
            )
          ) : (
            <div className="flex min-h-screen">
              <Sidebar
                currentView={currentView}
                setCurrentView={setCurrentView}
                onLogout={handleLogout}
              />

              <main className="flex-1 h-screen overflow-y-auto bg-white">
                {currentView === 'dashboard' && (
                  <Dashboard
                    onNewProject={() => setCurrentView('intake')}
                    onUploadProject={handleUploadProject}
                  />
                )}
                {currentView === 'projects' && (
                  <ProjectList
                    onUploadProject={handleUploadProject}
                    onNewProject={() => setCurrentView('intake')}
                    onOpenProject={handleOpenProject}
                  />
                )}
                {currentView === 'folders' && (
                  <FolderManager />
                )}
                {currentView === 'upload' && (
                  <ProjectUpload
                    onBack={() => setCurrentView('dashboard')}
                    onComplete={handleOpenProject}
                  />
                )}
                {currentView === 'intake' && (
                  <IntakeForm
                    onBack={() => setCurrentView('dashboard')}
                    onComplete={handleOpenProject}
                  />
                )}
                {currentView === 'project' && activeProjectId && (
                  <ProjectView
                    projectId={activeProjectId}
                    onBack={() => setCurrentView('projects')}
                  />
                )}
              </main>
            </div>
          )
        } />
      </Routes>
    </BrowserRouter>
  );
}
