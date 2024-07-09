from instagram.models import Instaloader

a = Instaloader.objects.first()
# print(a.session_file)
# print(a.test_login())

# print('=========')

# print(a.get_profile_info('sydnaeiaaa').__dict__)
a.get_stories()