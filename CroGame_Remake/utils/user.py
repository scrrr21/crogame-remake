def user_link(user):
    if user.username:
        return f'<a href="https://t.me/{user.username}">{user.first_name}</a>'
    return f'<a href="tg://user?id={user.id}">{user.first_name}</a>'