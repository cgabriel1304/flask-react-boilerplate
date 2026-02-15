import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import BackendStatus from './pages/BackendStatus'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/status" element={<BackendStatus />} />
    </Routes>
  )
}

export default App
