const form = document.querySelector('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

form.addEventListener('submit', (e) => {
  e.preventDefault()
  const username = e.target.dataset.username
  axios({
    method: 'post',
    url: `/accounts/follow/${username}/`,
    headers: {'X-CSRFToken': csrftoken}
  })
    .then((response) => {
      const isFollowed = response.data.is_followed
      const followBtn = document.querySelector('#follow-form > button[type=submit]')
      if (isFollowed === true) {
        const i = followBtn.querySelector('i')
        i.classList.remove('bi', 'bi-person-add')
        i.classList.add('bi', 'bi-person-dash')

      } else {
        const i = followBtn.querySelector('i')
        i.classList.remove('bi', 'bi-person-dash')
        i.classList.add('bi', 'bi-person-add')
      }

      const followingsCountTag = document.querySelector('#followings-count')
      const followersCountTag = document.querySelector('#followers-count')
      const followingsCountTagData = response.data.followings_count
      const followersCountTagData = response.data.followers_count
      followingsCountTag.textContent = followingsCountTagData
      followersCountTag.textContent = followersCountTagData
    })
})