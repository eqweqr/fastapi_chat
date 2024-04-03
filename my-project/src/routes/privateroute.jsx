import React from "react"
import { ReactDOM } from "react-dom"
import { Navigate, Outlet } from "react-router-dom"
import { useAuth } from "../moduls/auth_provider"


const PrivateRoute = ({component: Component, ...rest}) => {
    const {user} = useAuth()
    return user ? <Outlet/> : <Navigate to='/login'/>
}

export default PrivateRoute;