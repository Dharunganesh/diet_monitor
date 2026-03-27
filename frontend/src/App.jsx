import Header from "./Header.jsx";
import Login from "./Login.jsx";
import Register from "./Register.jsx";
import Dashboard from "./Dashboard.jsx";
import { useState } from "react";
import "./app.css";
function App(){
  const [page,setPage] = useState("login");
  const token=localStorage.getItem("token");
  return(
    <div className="app">
    <Header/>
    {
        token && token != "undefined"? (
          <Dashboard />
        ) : (
          <>
            <nav>
              <button onClick={() => setPage("login")}>LOGIN</button>
              <button onClick={() => setPage("register")}>REGISTER</button>
            </nav>

            {
              page === "login"
              ? <Login />
              : <Register />
            }
          </>
        )
      }
    </div>
  );
}
export default App;