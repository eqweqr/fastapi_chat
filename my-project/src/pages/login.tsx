import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import React from "react";
import { useAuth } from "../moduls/auth_provider";

const Login = () => {
    const {login} = useAuth()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const route = useNavigate()
    const rootChange = () =>{ 
      let path = `/`; 
      route(path);
    }

    const submitHandler = async (e: React.SyntheticEvent) => {
        e.preventDefault();

        try{
            await login(username, password)
        }catch (err){
            console.log(err)
            setPassword('')
            setUsername('')
            document.getElementById('error')!.className += 'text-sm p-1 mt-4 text-red-300 ml-2 mr-2 '
            document.getElementById('error')!.innerHTML='Incorrect username or password';
            return
        }
        rootChange()
      }

    const signupChange = () =>{ 
      let path = `/signup`; 
      route(path);
    }

    return (
        <div className='size flex items-center justify-center min-w-full min-h-screen bg-sky-500/100'>
          <form className='border-2 border-black flex flex-col md:w-1/4 bg-white'>
            <div className='mt-3 text-3xl font-bold text-center'>
              <div className='text-blue'>welcome!</div>
              <div id="error"></div>
            </div>
            <input
              placeholder='username'
              className='p-3 mt-4 ml-2 mr-2 rounded-md border-2 border-grey
              focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
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
            >
              login
            </button>
            <button
              className='mt-1 ml-2 mr-2 p-3 rounded-md bg-red font-bold text-black
              hover :outline-none hover:border-sky-500 focus:ring-1 hover:ring-sky-500
              mb-4 bg-gray-300'
              onClick={signupChange}
            >signup</button>
          </form>
        </div>
      )
    
    }
    
export default Login