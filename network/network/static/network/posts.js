document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    //document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    //document.querySelector('#post-content').style.display = 'none';
  
    // By default, load the inbox
    //load_posts('inbox');
    fetch('/posts/')
        .then(response => {
            // Check if the response is JSON
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();  // Attempt to parse the response as JSON
        })
        .then(posts => {
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = '';  // Clear the posts container before adding new posts
            posts.forEach(post => {
                // Create a div for each post
                const postDiv = document.createElement('div');
                postDiv.classList.add('post', 'border', 'rounded', 'm-2', 'p-4');
                postDiv.innerHTML = `
                    <h5>${post.author}</h5>
                    <p>${post.content}</p>
                    <small>Posted on: ${post.created_at}</small>
                `;
                postsContainer.appendChild(postDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });

  });


  /*function fetch_posts(mailbox) {

    // Retrieve posts from server
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);
  
      emails.forEach(email => {
        preview_email(email, mailbox)
      });
    });
  }*/