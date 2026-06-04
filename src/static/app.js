document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and dropdown options
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
          const activityCard = document.createElement("div");
          activityCard.className = "activity-card";

          const spotsLeft = details.max_participants - details.participants.length;

activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p class="availability"><strong>Availability:</strong> <span class="spots-left">${spotsLeft}</span> spots left</p>
          <div class="participants">
            <strong>Participants</strong>
            <div class="participants-list"></div>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Populate participants list and add delete handlers
        const participantsListContainer = activityCard.querySelector('.participants-list');
        if (details.participants && details.participants.length) {
          const ul = document.createElement('ul');
          details.participants.forEach(p => {
            const li = document.createElement('li');
            li.className = 'participant-item';
            const span = document.createElement('span');
            span.textContent = p;

            const btn = document.createElement('button');
            btn.className = 'participant-delete';
            btn.title = 'Unregister participant';
            btn.innerHTML = '✖';
            btn.addEventListener('click', async () => {
              try {
                const res = await fetch(
                  `/activities/${encodeURIComponent(name)}/participants?email=${encodeURIComponent(p)}`,
                  { method: 'DELETE' }
                );
                const json = await res.json();
                if (res.ok) {
                  li.remove();
                  // update spots left
                  const spotsEl = activityCard.querySelector('.spots-left');
                  const current = parseInt(spotsEl.textContent, 10) || 0;
                  spotsEl.textContent = current + 1;
                } else {
                  alert(json.detail || 'Failed to remove participant');
                }
              } catch (err) {
                console.error('Error removing participant', err);
                alert('Failed to remove participant');
              }
            });

            li.appendChild(span);
            li.appendChild(btn);
            ul.appendChild(li);
          });
          participantsListContainer.appendChild(ul);
        } else {
          participantsListContainer.innerHTML = '<p class="no-participants">No participants yet</p>';
        }

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
