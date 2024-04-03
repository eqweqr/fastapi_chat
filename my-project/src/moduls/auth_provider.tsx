import { useState, createContext, useEffect, useContext } from 'react'
import React from 'react'
import { useNavigate } from 'react-router-dom'


export type Tokens = {
    access_token: string
    refresh_token: string
  }

export type User = {
  username: string
}
  
  // export const AuthContext = createContext<{
  //   authenticated: boolean
  //   setAuthenticated: (auth: boolean) => void
  //   user: User
  //   setUser: (token: User) => void
  //   loaded: boolean
  // }>({
  //   authenticated: false,
  //   setAuthenticated: () => {},
  //   user: { username: ''},
  //   setUser: () => {},
  //   loaded: false,
  // })

const AuthContext = createContext<{
  user: User
  setUser: (username) => void
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}>({
  user: {username: ''},
  setUser: () => {},
  login: async () => {},
  logout: async () => {}
})
  
  const AuthContextProvider = ({ children }: { children: React.ReactNode }) => {
    const [authenticated, setAuthenticated] = useState(false)
    const [user, setUser] = useState<User>({ username: ''})
    const [loaded, setLoaded] = useState(false)
  
    let navigate = useNavigate(); 
    const routeChange = () =>{ 
      let path = `/login`; 
      navigate(path);
    }
  
    useEffect(() => {
        const stored_tokens = localStorage.getItem('tokens')
        const cur_token: Tokens = JSON.parse(stored_tokens || '{}')


        const fetch_from_access = async (tokens: Tokens) => {
          const refreshRes = await fetch('http://localhost:8000/validate',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json',
            'Authorization': ['Bearer', cur_token.access_token].join(' ')},
          })
          const data = await refreshRes.json()
          const username = data.username
          return [username, refreshRes.ok]
        }


        const fetch_from_refresh = async (tokens: Tokens) => {
          const grant_type = 'refresh_token'
          const refresh_token = tokens.refresh_token
          const refreshRes = await fetch('http://localhost:8000/refresh',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({ grant_type, refresh_token }),
          })
          const data = await refreshRes.json()
          const username = data.username
          const access_token = data.refresh_token
          return [username, access_token, refreshRes.ok]
        }
        const index = async(token: Tokens) => {
          if (!stored_tokens) {
            if (window.location.pathname != '/signup') {
              routeChange()
              return
            }
          } else {
            try {
              const [username, statusOk] = await fetch_from_access(cur_token)
              if (statusOk){
                setUser({username: username})
                setAuthenticated(true)
              } else {
                const [username, new_access, statusOk] = await fetch_from_refresh(cur_token)
                if (statusOk) {
                  setUser({
                    username: username
                  })
                  setAuthenticated(true)
                  localStorage.setItem('access_token', new_access)
                } else {
                  if (window.location.pathname != '/signup') {
                    routeChange()
                    return
                  }
                }
              }
            }
            catch (err){
              routeChange()
              return
            }finally{
              setLoaded(true)
            }
          }
        }
        index(cur_token)
      }, [])


      const logout = async() => {
        const grant_type = 'refresh_token'
        const stored_tokens = localStorage.getItem('tokens')
        const cur_token: Tokens = JSON.parse(stored_tokens || '{}')
        const refresh_token = cur_token.refresh_token
        let logoutForm = new FormData()
        logoutForm.append('grant_type', grant_type)
        logoutForm.append('refresh_token', refresh_token)
        const req = await fetch('http://localhost:8000/logout',{
          method: 'POST',
          body: logoutForm,
        })
        localStorage.clear()
        setUser({username: ''})
        routeChange()

      }


      const login = async(username: string, password: string) => {  
        let loginForm = new FormData();
        loginForm.append('username', username);
        loginForm.append('password', password)

        const res_log = await fetch('http://localhost:8000/login',{
          method: 'POST',
          body: loginForm,
        })
        const data = await res_log.json()
        if (res_log.ok){
          const token: Tokens = {
            access_token: data.access_token,
            refresh_token: data.refresh_token,
          }
          const new_tokens = JSON.stringify(token)
          // console.log(new_tokens)
          localStorage.setItem('tokens', new_tokens)
          setUser({username: username})
        }else {
        localStorage.clear()
          throw 'Invalid data'
        }
      }

  const contextValue = {
    user: user,
    setUser: setUser,
    login: login,
    logout: logout,
  };

    
      return (
        <AuthContext.Provider
          value={
            contextValue
          }
        >
          {children}
        </AuthContext.Provider>
      )
    }
    
    export const useAuth = () => {
      return useContext(AuthContext)
    }
  export default AuthContextProvider;