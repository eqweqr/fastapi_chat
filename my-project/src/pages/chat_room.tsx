import React, { useRef, useState } from "react"
import { WebsocketContext } from "../moduls/websocket_provider";
import { useContext } from "react";
import AuthContextProvider, { useAuth } from "../moduls/auth_provider";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

export type Message = {
    message: string
    username: string
}

export type User = {
    username: string,
}
const ChatRoom = (props) => {
    const conn = props.conn
    const textarea = useRef<HTMLTextAreaElement>(null)
    const [messages, setMessage] = useState<Message[]>([])
    // const [users, setUser] = useState<User[]>([])
    const {user, logout} = useAuth()
    const pos = useRef()

    const route = useNavigate()
    const to_root = () => {
        route('/')
    }
    useEffect(() => {
        if (conn === null) {
            to_root()
            return
        }
    
        const roomId = conn.url.split('/')[4].split('?')[0]
        async function getMessges() {
          try {
            // console.log(conn)
            const res = await fetch(`http://localhost:8000/ws/getMessages/${roomId}`, {
              method: 'GET',
              headers: { 'Content-Type': 'application/json' },
            })
            const data = await res.json()

            console.log(data)
            setMessage(data)
          } catch(e){
            console.log(e)
          }
        }
        getMessges()
      }, [])

      useEffect(() => {    
        if (conn === null) {
          to_root()
          return
        }
    
        conn.onmessage = (message) => {
          const m: Message = JSON.parse(message.data)
          setMessage([...messages, m])
          document.getElementById('wrapper_Scrollbottom')?.scrollIntoView()
      }

        conn.onclose = () => {}
        conn.onerror = () => {}
        conn.onopen = () => {}
      }, [textarea, messages, conn])
    
      const sendMessage = () => {
        if (!textarea.current?.value) return
        if (conn === null) {
          to_root()
          return
        }
        console.log(textarea.current.value)
        conn.send(textarea.current.value)
        textarea.current.value = ''
      }

    
      return (
        <>
          <div className='flex flex-col  items-center'>
            <div id='Chat' className='fixed mt-10 items-center border-2 border-blue justify-end h-[90%] w-[80%]'>
              <div className="overflow-x-auto max-h-[100%] " id="containerScroll">
              {messages.map((message, id)=>{
                return(<div className={message.username==user.username?"text-right p-2":"text-left p-2"} id="messages"
                key={id}>
              <div className='text-sm'>send: {message.username}</div>
              <div>
                <div className='bg-blue text-black px-4 py-1 rounded-md inline-block mt-1'>
                  {message.message}
                </div>
              </div>
                </div>)
              })}
              <div className="h-[5px] w-[100%]" id='wrapper_Scrollbottom'></div>
              </div>
            </div>
            <div className='fixed bottom-0 mt-4 w-full'>
              <div className='flex md:flex-row px-4 py-2 bg-grey md:mx-4 rounded-md'>
                <div className='flex w-full mr-4 rounded-md border border-blue'>
                  <textarea
                    ref={textarea}
                    placeholder='type your message here'
                    className='w-full h-10 p-2 border-2 rounded-md focus:outline-none'
                    style={{ resize: 'none' }}
                  />
                </div>
                <div className='flex items-center'>
                  <button
                    className='p-2 rounded-md bg-blue-200 text-black'
                    onClick={sendMessage}
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </>
      )
    }

export default ChatRoom;