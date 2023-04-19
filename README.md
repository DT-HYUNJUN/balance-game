# Balance Game

## 구상도

accounts
  - path
    - signup
    - login
    - logout

  - model
    - User
      - followings = ManyToMany('self', related_name='followers', symmetical=False)

posts
  - path
    - create

  - model
    - Post
      - user (F)
      - title : varchar, max_length=100
      - select1_user : ManyToMany(settings.AUTH_USER_MODEL, related_name='select1_post')
      - select1_content : varchar, max_length=100
      - select2_user : ManyToMany(settings.AUTH_USER_MODEL, related_name='select2_post')
      - select2_content : varchar, max_length=100
      - image1 : image
      - image2 : image
      - created_at
      - like_users = ManyToMany(settings.AUTH_USER_MODEL, related_name='like_posts')

    - Comment
      - user (F)
      - post (F)
      - content
      - created_at