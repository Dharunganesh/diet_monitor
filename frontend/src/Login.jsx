import "./login.css";
import {useState} from "react";
function Login(){
    const [email,setEmail]=useState("");
    const[password,setPassword]=useState("");
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    async function Handle_Login(event){
        event.preventDefault();
        const formData = new URLSearchParams();
        formData.append("grant_type", "password");
        formData.append("username", email);
        formData.append("password", password);

        const response=await fetch(`${BACKEND_URL}/login`,{
            method:"POST",
            headers:{"Content-Type":"application/x-www-form-urlencoded"},
            body: formData.toString()
        });
        const data=await response.json();
        localStorage.setItem("token",data.access_token)
        window.location.reload();
    }
    return(
        <div className="login">
        <h2>LOGIN</h2>
        <form>
            <label>Email:</label>
            <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)}></input>
            <br></br>
            <br></br>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}></input>
            <br></br>
            <br></br>
            <button type="submit" onClick={Handle_Login}>Submit</button>
        </form>
        </div>
    );
}
export default Login;