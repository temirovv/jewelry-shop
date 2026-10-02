import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Shrift o'zimizdan: Google Fonts ikki qo'shimcha tashqi ulanish (DNS+TLS)
// talab qilardi va CSS'i sahifa chizilishini to'sardi
import '@fontsource-variable/inter'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
