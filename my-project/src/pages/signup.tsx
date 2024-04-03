import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import React from "react";
import { useAuth } from "../moduls/auth_provider";
import { Tokens } from "../moduls/auth_provider";

const SignUp = () => {
    const {setUser} = useAuth()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [email, setEmail] = useState('')

    const route = useNavigate()

    // useEffect(() => {
    //     if (authenticated){
    //         const redirect_to_root = () => route('/')
    //         redirect_to_root()
    //         return
    //     }
    // }, [authenticated])

    const submitHandler = async (e: React.SyntheticEvent) => {
        e.preventDefault();
        try{

            let registerForm = new FormData();
            registerForm.append('username', username);
            registerForm.append('email', email);
            registerForm.append('password', password)


            const res = await fetch('http://localhost:8000/register',{
                method: 'POST',
                // headers: { 'Content-Type': 'application/json' },
                body: registerForm,
            })

            // const data = await res.text()
            // console.log(data)
            if (res.ok) {

              let loginForm = new FormData();
              loginForm.append('username', username);
              loginForm.append('password', password)

              const res_log = await fetch('http://localhost:8000/login',{
                method: 'POST',
                // headers: { 'Content-Type': 'application/json' },
                body: loginForm,
            })
              let data = await res_log.json()

              if (res_log.ok){
                const token: Tokens = {
                  access_token: data.access_token,
                  refresh_token: data.refresh_token,
                }
                const new_tokens = JSON.stringify(token)
                localStorage.setItem('tokens', new_tokens)
                setUser({username: username })

                const redirect_to_root = () => route('/')
                redirect_to_root()
                return
              }
            }
        }catch (err){
            console.log(err)
        }
        setEmail('')
        setPassword('')
        setUsername('')
        document.getElementById('error')!.className += 'text-sm p-1 mt-4 text-red-300 ml-2 mr-2 '
        document.getElementById('error')!.innerHTML='Unawailable email or username';
    }
    let navigate = useNavigate(); 
    const routeChange = () =>{ 
      let path = `/login`; 
      navigate(path);
    }

    return (
        <div className='size flex items-center justify-center min-w-full min-h-screen bg-sky-500/100'>
          <form className='border-2 border-black flex flex-col md:w-1/4 bg-white'>
            <div className='mt-3 text-3xl font-bold text-center'>
              <div className='text-blue'>welcome!</div>
              <div id="error"></div>
            </div>
            <input
              type='username'
              placeholder='username'
              className='p-3 mt-4 ml-2 mr-2 rounded-md border-2 border-grey
              focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              placeholder='email'
              className='p-3 mt-4 ml-2 mr-2 rounded-md border-2 border-grey
              focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type='password'
              placeholder='password'
              className='p-3 mt-4 ml-2 mr-2 rounded-md border-2 border-grey
              focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              className='mt-4 ml-2 mr-2 p-3 rounded-md bg-red font-bold text-black
              hover :outline-none hover:border-sky-500 focus:ring-1 hover:ring-sky-500
              mb-4 bg-gray-300'
              type='submit'
              onClick={submitHandler}
            >sign up
            </button>
            <button
              className='mt-1 ml-2 mr-2 p-3 rounded-md bg-red font-bold text-black
              hover :outline-none hover:border-sky-500 focus:ring-1 hover:ring-sky-500
              mb-4 bg-gray-300'
              onClick={routeChange}
            >login</button>

          </form>
        </div>
      )
    
    }
    
export default SignUp