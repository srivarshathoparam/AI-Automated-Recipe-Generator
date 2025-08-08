const API_URL = "http://127.0.0.1:5000"; // Update if needed

// ✅ Register a new user
async function registerUser(username, password) {
    const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    console.log("Register:", data);
}

// ✅ Login user and get JWT token
async function loginUser(username, password) {
    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (data.token) {
        localStorage.setItem("token", data.token); // Store token
        console.log("Login Successful:", data);
    } else {
        console.log("Login Failed:", data);
    }
}

// ✅ Get user profile (Protected Route)
async function getProfile() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.log("No token found. Please log in.");
        return;
    }

    const response = await fetch(`${API_URL}/profile`, {
        method: "GET",
        headers: { "x-access-token": token },
    });
    const data = await response.json();
    console.log("Profile:", data);
}

// ✅ Update user password (Example Update operation)
async function updateUserPassword(newPassword) {
    const token = localStorage.getItem("token");
    if (!token) {
        console.log("No token found. Please log in.");
        return;
    }

    const response = await fetch(`${API_URL}/update-password`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "x-access-token": token,
        },
        body: JSON.stringify({ password: newPassword }),
    });

    const data = await response.json();
    console.log("Update Password:", data);
}

// ✅ Delete user account (Example Delete operation)
async function deleteUser() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.log("No token found. Please log in.");
        return;
    }

    const response = await fetch(`${API_URL}/delete-account`, {
        method: "DELETE",
        headers: { "x-access-token": token },
    });

    const data = await response.json();
    console.log("Delete Account:", data);
}

// ✅ Logout function (Clears token)
function logoutUser() {
    localStorage.removeItem("token");
    console.log("User logged out.");
}

// Example Usage
// Uncomment the function calls below to test them:

// registerUser("testuser", "password123");
// loginUser("testuser", "password123");
// getProfile();
// updateUserPassword("newpassword456");
// deleteUser();
// logoutUser();
