import Header from "./Header.jsx";
import Login from "./Login.jsx";
import Register from "./Register.jsx";
import { useState } from "react";
import "./app.css";
function App(){
  const [page,setPage] = useState("login");
  return(
    <div className="app">
    <Header/>
    <nav>
      <button onClick={() => setPage("login")}>LOGIN</button>
      <button onClick={()=>setPage("register")}>REGISTER</button>
    </nav>
    {
      page === "login"
      ? <Login />
      : null
    }

    {
      page ==="register" ? <Register/> : null
    }
    </div>
  );
}
export default App;