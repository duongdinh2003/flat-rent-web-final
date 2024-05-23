from django.db import connections
from .models import UserAccount, UserInformation
from listing.models import ListingReview

def get_reviews_of_realtor(realtor):
    # Bước 1: Truy vấn Listing để lấy tất cả các listing của realtor đó từ database listings
    with connections['listings'].cursor() as cursor:
        cursor.execute("SELECT id FROM listing_listing WHERE realtor = %s", [realtor.email])
        listing_ids = [row[0] for row in cursor.fetchall()]

    # Bước 2: Truy vấn ListingReview để lấy tất cả các review liên quan đến các listing đó
    reviews = ListingReview.objects.using('listings').filter(listing_id__in=listing_ids).values(
        'id', 'customer', 'listing_id', 'review', 'vote'
    )

    # Lấy danh sách email của các customer
    customer_emails = list(set(review['customer'] for review in reviews))

    # Bước 3: Truy vấn UserAccount và UserInformation để lấy thông tin người dùng và avatar từ database users
    user_accounts = UserAccount.objects.using('users').filter(email__in=customer_emails).values('email', 'name')
    user_information = UserInformation.objects.using('users').filter(user__email__in=customer_emails).values('user__email', 'avatar')

    # Tạo từ điển để dễ dàng truy cập thông tin
    user_info_dict = {user['email']: {'name': user['name']} for user in user_accounts}
    for info in user_information:
        if info['user__email'] in user_info_dict:
            user_info_dict[info['user__email']]['avatar'] = info['avatar']

    # Bước 4: Kết hợp dữ liệu
    listing_reviews = []
    for review in reviews:
        customer_info = user_info_dict.get(review['customer'], {'name': None, 'avatar': None})
        review_data = {
            'id': review['id'],
            'customer': review['customer'],
            'listing_id': review['listing_id'],
            'review': review['review'],
            'vote': review['vote'],
            'customer_name': customer_info['name'],
            'customer_avatar': customer_info['avatar'],
        }
        listing_reviews.append(review_data)
    
    return listing_reviews
