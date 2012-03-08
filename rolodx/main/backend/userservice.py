from main.models import UserProfile

class UserService:
	def GetUserProfile(self, user):
		return UserProfile.objects.get_or_create(user=user)[0]