import React, { useEffect } from "react";
import { useAuth } from "../moduls/auth_provider";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const RootPage = (props) => {
    const {user, logout} = useAuth()
    const [rooms, setRooms] = useState<{owner: string, room: string, id: number}[]>([])
    const [roomName, setName] = useState('')
    const [roomPass, setPass] = useState('')
    
    const route = useNavigate()
    const redirectChat = (id: number) => route(`/chat/`+id)
    const connChat = (id: number) => {
        redirectChat(id)
        return
    }
    const getRooms = async() => {
        const tokens = localStorage.getItem('tokens')
        const json_tokens = JSON.parse(tokens || '{}')
        console.log(['Bearer', json_tokens.access_token].join(' '))
        try{
            const res = await fetch('http://localhost:8000/chat/get?limit=10&page=0',{
                method: 'GET',
                headers: {
                'Authorization': ['Bearer', json_tokens.access_token].join(' ')},
            }
            )
            const data = await res.json()
            if (res.ok){
                setRooms(data)
            }
        } catch(exp){
            console.log(exp)
        }
    }
    const submitHandler = async() => {
        let roomForm = new FormData();
        roomForm.append('chatname', roomName);
        roomForm.append('password', roomPass)
        const tokens = localStorage.getItem('tokens')
        const json_tokens = JSON.parse(tokens || '{}')
        console.log(['Bearer', json_tokens.access_token].join(' '))
        try{
            const res = await fetch('http://localhost:8000/chat/new', {
                method: 'POST',
                headers: {
                    'Authorization': ['Bearer', json_tokens.access_token].join(' ')
                },
                body: roomForm,
            })
            const chat_id = await res.text()
            console.log(chat_id)
            if (res.ok){
                joinRoom(chat_id)
            }
        }catch(exp){
            console.log(exp)
        }
    }

    const joinRoom = (roomId) => {
      const tokens = localStorage.getItem('tokens')
      const json_tokens = JSON.parse(tokens || '{}')
      const access_token = json_tokens.access_token
      console.log(access_token)
      const ws = new WebSocket(
        `ws://localhost:8000/ws/${roomId}?token=${access_token}`
      )
      if (ws.OPEN) {
        props.setConn(ws)
        const redirect_to_root = (id) => route('/chat/'+id)
        console.log('reached')
        redirect_to_root(roomId)
        return
      }
        return
    }
    useEffect(()=>{getRooms()}, []) 
    return (
        <>
          <div className='my-8 px-4  w-full h-full'>
            {/* <div className="flex"> */}
            <div className="flex">
            <div className=""></div>
            <div className="text-xl flex w-full justify-center col-span-2"> Hello, {user.username}</div>
            <div className="flex items-center">
            <button className='text-lg bg-red-500 border rounded-md p-2 md:ml-4' onClick={logout}>logout</button>
            </div>
            <div className=""></div>
            {/* </div> */}
            </div>
            <div className='flex justify-center mt-3 p-5'>
              <input
                type='text'
                className='border border-grey p-2 rounded-md focus:outline-none focus:border-blue'
                placeholder='room name'
                value={roomName}
                onChange={(e) => setName(e.target.value)}
              />
              <input
                type='text'
                className='border border-grey p-2 ml-3 rounded-md focus:outline-none focus:border-blue'
                placeholder='room password'
                value={roomPass}
                onChange={(e) => setPass(e.target.value)}
              />
              <button
                className='bg-blue-200 border text-black rounded-md p-2 md:ml-4 '
                onClick={submitHandler}
              >
                create room
              </button>
            </div>
            <div className='mt-6'>
              <div className='font-bold'>Available Rooms</div>
              <div className='grid grid-cols-1 md:grid-cols-5 gap-4 mt-6 '>
                {rooms.map((room, index) => (
                  <div
                    key={index}
                    className='border border-blue p-4 flex items-center rounded-md w-full'
                  >
                    <div className='w-full'>

          <div className='text-sm'>room</div>
                      <div className='text-blue font-bold text-lg'>{room.room}</div>
                    </div>
                    <div className=''>
                      <button
                        className='px-4 text-black bg-red-300 rounded-md'
                        onClick={() => joinRoom(room.id)}
                      >
                        join
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )
}
export default RootPage;