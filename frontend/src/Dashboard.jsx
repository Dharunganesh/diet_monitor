function Dashboard(){
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    let submit_button=document.getElementById("submit_button");
    submit_button.onclick= async function(){
        let text_content=document.getElementById("text_content");
        text_content.textContent="Your response have been submitted";
    }
    return(
        <div>
            <h1>Welcome to Dashboard</h1>
            <br></br>
            <label>Enter your food record:</label>
            <input type="file" id="photo"></input>
            <br></br>
            <button type="submit" id="submit_button">Submit</button>
            <h2 id="text_content"></h2>
        </div>
    )
}
export default Dashboard;