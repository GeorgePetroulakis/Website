document.addEventListener("DOMContentLoaded", function() {
    // Get the profile name element
    const profileName = document.getElementById("profile-name");
    const friendButton = document.getElementById("friend-button");

    // Function to position the button
    function positionFriendButton() {
        const nameRect = profileName.getBoundingClientRect(); // Get the position of the profile name

        // Set the button's left position to the right of the last letter plus a certain offset (e.g., 10 pixels)
        const offset = 10; // Adjust this value as needed for spacing
        friendButton.style.left = `${nameRect.right + offset}px`; // Add offset to the right of the last letter

        // Set the button's top position to align with the top of the profile name
        friendButton.style.top = `${nameRect.top-130}px`; // Align vertically with the profile name
    }

    // Call the function to position the button
    positionFriendButton();

    // Optional: Reposition on window resize
    window.addEventListener('resize', positionFriendButton);
});
