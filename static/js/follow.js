const form = document.querySelector('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const followerList = document.querySelector('#follower-list')

const addFollower = (e) => {
  const myName = e.target.dataset.myname
  const image = e.target.dataset.image

  const follower = document.createElement('div')
  follower.setAttribute('id', `${myName}`)
  follower.classList.add('m-2')

  const aTag = document.createElement('a')
  aTag.setAttribute('href', `/accounts/profile/${myName}`)
  aTag.classList.add('userinfo-txt')

  const divTag = document.createElement('div')
  divTag.classList.add('userinfo_box')
  
  const img = document.createElement('img')
  img.classList.add('userinfo_img')
  img.setAttribute('src', `${image}`)

  const pTag = document.createElement('p')
  pTag.textContent = myName
  pTag.classList.add('text-center')

  divTag.appendChild(img)

  aTag.appendChild(divTag)
  aTag.appendChild(pTag)

  follower.appendChild(aTag)

  followerList.appendChild(follower)
}

const deleteFollower = (e) => {
  const myName = e.target.dataset.myname
  const follower = document.querySelector(`#${myName}`)
  followerList.removeChild(follower)
}

const formEvent = (e) => {
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
        addFollower(e)
      } else {
        const i = followBtn.querySelector('i')
        i.classList.remove('bi', 'bi-person-dash')
        i.classList.add('bi', 'bi-person-add')
        deleteFollower(e)
      }

      const followingsCountTag = document.querySelector('#followings-count')
      const followersCountTag = document.querySelector('#followers-count')
      const followingsCountTagData = response.data.followings_count
      const followersCountTagData = response.data.followers_count
      followingsCountTag.textContent = followingsCountTagData
      followersCountTag.textContent = followersCountTagData
    })
}

form.addEventListener('submit', formEvent)