import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { BrowserRouter, Router, Routes, Route} from 'react-router-dom'
import { createRoot } from 'react-dom/client'
import './App.css'

import AuthContextProvider from './moduls/auth_provider.tsx'
import PrivateRoute from './routes/privateroute.jsx'


const domNode = document.getElementById('root');
const root = createRoot(domNode);
root.render(<React.StrictMode>
      <BrowserRouter>
          <App/>
      </BrowserRouter>
    </React.StrictMode>
)