import { Routes, Route } from 'react-router-dom'
import { Header, Footer } from './components/Layout'
import { HomePage } from './pages/HomePage'
import { DataExplorerPage } from './pages/DataExplorerPage'
import { MapsPage } from './pages/MapsPage'
import { BusinessPage } from './pages/BusinessPage'
import { ResidentsPage } from './pages/ResidentsPage'
import { TouristsPage } from './pages/TouristsPage'
import { LeadersPage } from './pages/LeadersPage'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/data" element={<DataExplorerPage />} />
          <Route path="/maps" element={<MapsPage />} />
          <Route path="/business" element={<BusinessPage />} />
          <Route path="/residents" element={<ResidentsPage />} />
          <Route path="/tourists" element={<TouristsPage />} />
          <Route path="/leaders" element={<LeadersPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}
