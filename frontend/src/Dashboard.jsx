function Dashboard(){
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const handleSubmit = () => {
        setMessage("Your response has been submitted");
    };
    return(
        <div>
            <h1>Welcome to Dashboard</h1>
            <br></br>
            <label>Enter your food record:</label>
            <input type="file" id="photo"></input>
            <br></br>
            <button onClick={handleSubmit}>Submit</button>
            <h2>{message}</h2>
        </div>
    )
}
export default Dashboard;
