import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom/client'
// import App from './App.jsx'
// import './index.css'
import Login from './pages/login.tsx'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import SignUp from './pages/signup.tsx'
// import App from './pages/main_page.tsx'
import AuthContextProvider from './moduls/auth_provider.tsx'
import PrivateRoute from './routes/privateroute.jsx'
import WebSocketProvider from './moduls/websocket_provider.tsx'
import ChatRoom from './pages/chat_room.tsx'
import RootPage from './pages/main_page.tsx'

const App = () => {

  const [conn, setConn] = useState(null)
  return (
    <div className="app">
               <AuthContextProvider>
              <Routes>
                <Route exact path={`chat/:id`} element={<ChatRoom conn={conn}/>}/>              
                {/* <Route path='/chat/:id' element={<PrivateRoute/>}>
                    <Route path='/chat/:id' element={<ChatRoom/>}/>
                </Route> */}
                <Route path='/' element={<PrivateRoute/>}>
                <Route path='/' element={<RootPage setConn = {setConn}/>}/>
                </Route>
                <Route path='/login' element={<Login/>}/>
                <Route path='/signup' element={<SignUp/>}/>
              </Routes>
             </AuthContextProvider>
            </div>
  )
}

export default App;