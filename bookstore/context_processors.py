from django.db.models import Sum

from catalog.models import Book, Category


def categories(request):
    categories = Category.objects.all()
    parents = {}

    for row in categories:
        if row.parent_id not in parents:
            parents[row.parent_id] = []

        parents[row.parent_id].append(row)

    def find_children_recoursive(pid, depth=0):
        if pid not in parents or depth > 1:
            return None

        children = []
        for row in parents[pid]:
            children.append({
                "category": row,
                "children": find_children_recoursive(row.id, depth + 1)
            })
        return children

    result = find_children_recoursive(None)
    return {
        "categories": result
    }


def cart(request):
    try:
        if request.session["items"]:
            items_list = request.session["items"]
            cart_items_count = len(request.session["items"])
            cart_item = Book.objects.annotate(total_price=Sum("price")).filter(id__in=items_list)
            cart_items_total_price = Book.objects.filter(id__in=items_list).aggregate(Sum("price"))
        else:
            cart_items_total_price = None
            cart_items_count = None
            cart_item = None
    except KeyError:
        cart_items_total_price = None
        cart_items_count = None
        cart_item = None
    return {"cart_item": cart_item,
            "cart_items_count": cart_items_count,
            "cart_items_total_price": cart_items_total_price}


def url_name(request):
    return {
        "action_path": "{}:{}".format(request.resolver_match.app_name, request.resolver_match.url_name),
        "url_name": "{}/{}".format(request.resolver_match.app_name, request.resolver_match.url_name)
    }
