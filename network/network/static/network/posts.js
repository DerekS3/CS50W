document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display posts when the page loads
    fetchPosts();

    // Handle form submission for new posts
    document.getElementById('new-post-form').onsubmit = submitPost;
});

function submitPost(event) {
    event.preventDefault();
    const content = document.querySelector('#post-content').value
    document.querySelector('#post-content').value = '';
    
    // Send a POST request to create a new post
    fetch('/api/posts/', {
        method: 'POST',
        body: JSON.stringify({ 
            content: content 
        })  
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        // Reload posts after submission
        fetchPosts();
    });
}

function fetchPosts() {
    fetch('/api/posts/')
        .then(response => response.json())
        .then(posts => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';  // Clear any existing posts
            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.classList.add('border', 'rounded', 'm-2', 'p-4');
                postDiv.innerHTML = `
                    <h5>${post.author}</h5>
                    <p>${post.content}</p>
                    <small>Posted on: ${post.created_at}</small>
                `;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });
}
