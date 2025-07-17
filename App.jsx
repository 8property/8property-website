import { useState } from 'react'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import Properties from './components/Properties'
import Leads from './components/Leads'
import Analytics from './components/Analytics'
import Settings from './components/Settings'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'properties':
        return <Properties />
      case 'leads':
        return <Leads />
      case 'analytics':
        return <Analytics />
      case 'settings':
        return <Settings />
      default:
        return <Dashboard />
    }
  }

  return (
    <Layout currentPage={currentPage} onPageChange={setCurrentPage}>
      {renderPage()}
    </Layout>
  )
}

export default App
