# REST API imports
from rest_framework.views import APIView
from rest_framework.response import Response
from gatsby_blog.models import BlogLike, BlogSubscriber
from django.forms.models import model_to_dict
from datetime import datetime
from gatsby_blog.email import actions


class setLike(APIView):
    def get(self, request):
        slug = request.query_params.get('slug', None)
        if slug:
            obj, created = BlogLike.objects.get_or_create(slug=slug)

            # Get user IP from request
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            now = datetime.now()
            if created:
                obj.individualLikes.append({
                    "userIp": ip,
                    "likes": 1,
                    "time": now.strftime("%-d %b, %Y, %-I:%M:%S %p")
                })
                obj.ipList.append(ip)

            else:
                if ip in obj.ipList:
                    for item in obj.individualLikes:
                        if ip in item['userIp']:
                            item['likes'] += 1
                            item['time'] = now.strftime("%-d %b, %Y, %-I:%M:%S %p")
                else:
                    obj.individualLikes.append({
                        "userIp": ip,
                        "likes": 1,
                        "time": now.strftime("%-d %b, %Y, %-I:%M:%S %p")
                    })
                    obj.ipList.append(ip)
            obj.totalLikes += 1
            obj.save()

            return Response({
                # 'Object': model_to_dict(obj)
                'success': True
            })
        return Response({'error': 'No Slug Provided'})


class getLike(APIView):
    def get(self, request):
        slug = request.query_params.get('slug', None)
        if slug:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            obj, created = BlogLike.objects.get_or_create(slug=slug)
            userLikes = 0
            if ip in obj.ipList:
                for item in obj.individualLikes:
                    userLikes = item['likes']
            return Response({'totalLikes': obj.totalLikes, 'userLikes': userLikes})
        return Response({'error': 'No Slug Provided'})


class newSubscriber(APIView):
    def get(self, request):
        email = request.query_params.get("email", None)
        name = request.query_params.get("name", None)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if email and name:
            if BlogSubscriber.objects.filter(email=email).exists():
                return Response({'error': 'Email already subscribed'})
            else:
                blogSubObj = BlogSubscriber.objects.create(email=email, name=name, ip=ip)
                actions(blogSubObj, "NEW_SUBSCRIBER")
                return Response({'success': True})
        else:
            return Response({'error': 'Data was not provided'})