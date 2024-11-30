eel.get_video_data()(function (video_data) {
  const videoList = document.getElementById("video-list");
  const homeScreen = document.getElementById("home-screen");
  const videoScreen = document.getElementById("video-screen");
  const videoContainer = document.getElementById("video-container");
  const backBtn = document.getElementById("back-btn");

  let currentVideoPlayer = null; // To track the current video player

  // Loop through the dictionary and dynamically add items to the list
  for (let id in video_data) {
      let [channel, title, description] = video_data[id];
      let thumbnailUrl = `${id}.jpg`;
      let videoFileUrl = `${id}.mp4`;

      // Create the video item
      const videoItem = document.createElement("div");
      videoItem.className = "item";
      videoItem.dataset.videoUrl = videoFileUrl;

      videoItem.innerHTML = `
          <div class="dot"></div>
          <img src="${thumbnailUrl}" alt="Thumbnail" class="thumbnail">
          <div class="details">
              <h2 class="item-title">${title}</h2>
              <p class="creator-name">By ${channel}</p>
              <p class="description">${description}</p>
          </div>
          <div class="action">
              <button class="trash-btn">
                  <img src="icons/trash-icon.svg" alt="Trash" class="trash-icon">
              </button>
              <p class="time">4 Days</p>
          </div>
      `;

      // Click event to open the video
      videoItem.addEventListener("click", function () {
          let videoUrl = videoItem.dataset.videoUrl;

          // Smoothly hide the home screen and show the video screen
          homeScreen.style.opacity = 0;
          setTimeout(() => {
              homeScreen.style.display = "none";
              videoScreen.style.display = "block";
              videoScreen.style.opacity = 0;
              setTimeout(() => (videoScreen.style.opacity = 1), 50);
          }, 300); // Match transition duration

          // Add the video player
          currentVideoPlayer = document.createElement("video");
          currentVideoPlayer.controls = true;
          currentVideoPlayer.src = videoUrl;
          currentVideoPlayer.autoplay = true;

          videoContainer.innerHTML = ""; // Clear old content
          videoContainer.appendChild(currentVideoPlayer);
      });

      videoList.appendChild(videoItem);
  }

  // Back button functionality
  backBtn.addEventListener("click", function () {
      // Smoothly hide the video screen and show the home screen
      videoScreen.style.opacity = 0;
      setTimeout(() => {
          videoScreen.style.display = "none";
          homeScreen.style.display = "block";
          homeScreen.style.opacity = 0;
          setTimeout(() => (homeScreen.style.opacity = 1), 50);
      }, 300); // Match transition duration

      // Pause the video
      if (currentVideoPlayer) {
          currentVideoPlayer.pause();
      }
  });
});
