from item.models import *

import random
def check_profile(request):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    all_cat = Category.objects.all()
    all_towns = Town.objects.all()
    if request.user.is_authenticated:
        print('user')
        wl = UserFavorites.objects.filter(user=request.user)
        wishlist_ids = []
        for i in wl:
            wishlist_ids.append(i.item.id)
    return locals()

