import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import pagination
from rest_framework.views import APIView
from rest_framework import status
from bs4 import BeautifulSoup

url ="https://www.thekashmirmonitor.net"

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10 

@api_view(['POST'])
def categories(request):
    try:
        url_categories  = f"{url}/wp-json/wp/v2/categories"
        response = requests.get(url_categories )
        response.raise_for_status()
        categories = response.json()
        results = []
        for category in categories:
            id = category["id"]
            description = category["description"]
            link = category["link"]
            slug = category["slug"]
            taxonomy = category["taxonomy"]
            result = {
                "id": id,
                "description": description,
                "link": link,
                "slug": slug,
                "taxonomy": taxonomy
            }
            results.append(result)
        return Response(results)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostListAPIView(APIView):
    pagination_class = CustomPagination

    def post(self,request, *args, **kwargs):
        url_posts  = f"{url}/wp-json/wp/v2/posts"
        try:
            response = requests.get(url_posts)
            response.raise_for_status()
            datas = response.json()
            results = []
            for data in datas:
                id = data["id"]
                date = data["date"]
                date_gmt = data["date_gmt"]
                slug = data["slug"]
                status = data["status"]
                type = data["type"]
                title = data["title"]["rendered"]
                soup = BeautifulSoup(title, 'html.parser')
                title = soup.get_text()
                content = data["content"]["rendered"]
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text()
                jetpack_featured_media_url = data["jetpack_featured_media_url"]
                # soup = BeautifulSoup(content, 'html.parser')
                # content = soup.get_text()
                result = {
                    "id": id,
                    "date": date,
                    "date_gmt": date_gmt,
                    "slug": slug,
                    "status": status,
                    "type": type,
                    "title": title,
                    "content": content,
                    "jetpack_featured_media_url": jetpack_featured_media_url,
                }
                results.append(result)
            return Response(results)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
        except json.decoder.JSONDecodeError as e:
            return Response({"error": str(e)}, status=500)
 
class PostListByIdAPIView(APIView):
    pagination_class = CustomPagination

    def post(self, request, pk, *args, **kwargs):
        id = pk
        url_posts = f"{url}/wp-json/wp/v2/posts/{id}"
        print(url_posts)

        try:
            response = requests.get(url_posts)
            response.raise_for_status()
            data = response.json()
            result = {
                "id": data["id"],
                "date": data["date"],
                "date_gmt": data["date_gmt"],
                "slug": data["slug"],
                "status": data["status"],
                "type": data["type"],
                "title": data["title"],
                "content": data["content"],
            }
            return Response(result)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
        except json.decoder.JSONDecodeError as e:
            return Response({"error": str(e)}, status=500)


class CategoriesByIdAPIView(APIView):
    pagination_class = CustomPagination

    def post(self,request,pk, *args, **kwargs):
        id = pk
        url_posts  = f"{url}/wp-json/wp/v2/posts?categories={id}"
        try:
            response = requests.get(url_posts)
            response.raise_for_status()
            datas = response.json()
            results = []
            for data in datas:
                id = data["id"]
                date = data["date"]
                date_gmt = data["date_gmt"]
                slug = data["slug"]
                status = data["status"]
                type = data["type"]
                title = data["title"]
                content = data["content"]
                jetpack_featured_media_url = data["jetpack_featured_media_url"]

                result = {
                    "id": id,
                    "date": date,
                    "date_gmt": date_gmt,
                    "slug": slug,
                    "status": status,
                    "type": type,
                    "title": title,
                    "content": content,
                    "jetpack_featured_media_url": jetpack_featured_media_url,

                }
                results.append(result)
            return Response(results)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
        except json.decoder.JSONDecodeError as e:
            return Response({"error": str(e)}, status=500)


# @api_view(['POST'])
# def create_form_widgets(request):
#     try:
#         form_widget_data = json.loads(request.body)
#         for widget_data in form_widget_data:
#             form_structure_data = widget_data.pop('form_structure')
#             decorative_structure_data = widget_data.pop('decorative_structure')
#             form_structure_serializer = FormStructureSerializer(data=form_structure_data)
#             decorative_structure_serializer = DecorativeStructureSerializer(data=decorative_structure_data)
#             if form_structure_serializer.is_valid() and decorative_structure_serializer.is_valid():
#                 form_structure = form_structure_serializer.save()
#                 decorative_structure = decorative_structure_serializer.save()
#                 FormWidgets.objects.create(
#                     form=form_structure_data['form'],
#                     form_structure=form_structure,
#                     decorative_structure=decorative_structure,
#                     input_type=int(widget_data['input_type']),
#                     input_name=widget_data['input_name'],
#                     is_required=bool(widget_data['is_required'])
#                 )
#             else:
#                 return Response(form_structure_serializer.errors or decorative_structure_serializer.errors, status=400)
#         return Response("Widgets created successfully", status=201)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)