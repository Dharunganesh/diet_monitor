import "./login.css";
import { useState } from "react";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    async function Handle_Login(event) {
        event.preventDefault();

        try {
            const response = await fetch(`${BACKEND_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store the token
                localStorage.setItem("token", data.access_token);

                // Show success
                window.alert(data.message);

                // Redirect to dashboard
                window.location.href = "/dashboard";

            } else {
                // Show error message
                window.alert(data.detail || "Login failed!");
            }

        } catch (error) {
            window.alert("Something went wrong. Please try again!");
            console.error(error);
        }
    }

    return (
        <div className="login">
            <h2>LOGIN</h2>
            <form>
                <label>Email:</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <br /><br />
                <label>Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <br /><br />
                <button type="submit" onClick={Handle_Login}>
                    Submit
                </button>
            </form>
        </div>
    );
}

export default Login;
