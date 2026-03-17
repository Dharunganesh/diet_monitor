import "./register.css";
import {useState} from "react";
function Register(){
    const [email,setEmail]=useState("");
        const[password,setPassword]=useState("");
        const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
        async function Handle_Register(event){
            event.preventDefault();
            const response=await fetch(`${BACKEND_URL}/register`,{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({
                    username:email,
                    password:password
                })
            });
            const data=await response.json();
            window.alert(data.message);
        }
    return(
        <div className="register">
        <h2>REGISTER</h2>
        <form>
            <label>Email:</label>
            <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)}></input>
            <br></br>
            <br></br>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}></input>
            <br></br>
            <br></br>
            <button type="submit" onClick={Handle_Register}>Submit</button>
        </form>
        </div>
    );
}
export default Register;