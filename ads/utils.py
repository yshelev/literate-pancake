from rest_framework.pagination import PageNumberPagination


def get_paginated_data(page_size,
                       queryset,
                       request):
	paginator = PageNumberPagination()
	paginator.page_size = page_size

	page = paginator.paginate_queryset(queryset, request)

	if page is not None:
		return page

	return queryset

def get_filtered_data(queryset,
                      category,
                      description,
                      condition,
                      title):
	if title is not None:
		queryset = queryset.filter(title__icontains=title)  # icontains для игнорирования регистра

	if description is not None:
		queryset = queryset.filter(description__icontains=description)

	if category is not None:
		queryset = queryset.filter(category=category)

	if condition is not None:
		queryset = queryset.filter(condition=condition)

	queryset = queryset.order_by("-title")

	return queryset